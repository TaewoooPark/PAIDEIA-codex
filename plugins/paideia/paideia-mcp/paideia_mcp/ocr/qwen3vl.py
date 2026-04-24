"""Local Qwen3-VL 8B vision OCR via Ollama's HTTP API.

Ports the behavior of ``scripts/vision_ocr.py::_ollama_ocr`` from the Claude
Code plugin. Keeps the 15-minute ``keep_alive`` + warmup semantics so the
model stays resident between pages.

The transcription prompt is parameterized on the course name so a Complex
Analysis folder is no longer transcribed under a "math/physics course"
framing. The VLM occasionally drifts into hedging prefaces and trailing
n-gram loops; ``_dedupe_loops`` strips both Korean and English hedge
sentences, and ``_strip_ngram_tail`` trims repeating n-grams at the tail
that escape sentence-level dedup.
"""

from __future__ import annotations

import base64
import io
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx
from PIL import Image

OLLAMA_MODEL = "qwen3-vl:8b"
_GENERATE_URL = "http://localhost:11434/api/generate"
_KEEP_ALIVE = "15m"
_WARMUP_TIMEOUT = 60.0
_PER_PAGE_TIMEOUT = 1800.0
_MAX_TOKENS = 6000
_MAX_IMG_WIDTH = 1200
_DEFAULT_COURSE = "math / physics"

PROMPT_TEMPLATE = (
    "You are transcribing a page from a {course} course PDF.\n"
    "\n"
    "Rules:\n"
    "- Korean prose stays Korean; English stays English.\n"
    "- Math expressions must become LaTeX: $...$ inline, $$...$$ display.\n"
    "- Preserve problem numbering (P1, P2, (1), (2), (a), (b), etc.).\n"
    "- Preserve section headings, lists, figure captions.\n"
    "- Do NOT summarize. Do NOT add commentary. Do NOT grade.\n"
    "- If a symbol is ambiguous, write [?] instead of guessing.\n"
    "- If a page has crossed-out work, ignore the strikethrough content.\n"
    "- Return ONLY markdown, no <think> blocks.\n"
)


def build_prompt(course_name: str | None) -> str:
    """Fill :data:`PROMPT_TEMPLATE` with the course name.

    Args:
        course_name: Human-readable course name, e.g. ``Complex Analysis``.
            Blank / ``None`` falls back to ``math / physics``.

    Returns:
        The fully rendered prompt string.
    """

    course = (course_name or "").strip() or _DEFAULT_COURSE
    return PROMPT_TEMPLATE.format(course=course)


def _image_to_b64(png_path: Path) -> str:
    """Load a PNG, resize to a sane width, and return a base64 JPEG payload."""

    with Image.open(png_path) as img:
        img = img.convert("RGB")
        if img.width > _MAX_IMG_WIDTH:
            ratio = _MAX_IMG_WIDTH / img.width
            img = img.resize(
                (_MAX_IMG_WIDTH, int(img.height * ratio)),
                Image.LANCZOS,
            )
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode()


_HEDGE_PREFIXES = (
    # English
    "wait,",
    "wait.",
    "hmm,",
    "hmm.",
    "actually,",
    "but the hand-written",
    "the image shows",
    "the image has",
    "got it",
    "let's check",
    "let's look",
    "let me check",
    "let me look",
    # Korean (Qwen3-VL thinking-mode drift also surfaces in Korean)
    "잠깐,",
    "잠깐.",
    "음,",
    "음.",
    "아,",
    "어,",
    "그러니까",
    "근데",
    "사실,",
    "보자",
)


def _is_noise_sentence(sentence: str) -> bool:
    """True if ``sentence`` is hedge-only VLM self-doubt noise.

    The match is case-insensitive on the ASCII prefixes; Korean prefixes
    are left unnormalized because casefold is a no-op for Hangul.
    """

    trimmed = sentence.strip()
    if not trimmed:
        return True
    lower = trimmed.lower()
    for prefix in _HEDGE_PREFIXES:
        if lower.startswith(prefix) or trimmed.startswith(prefix):
            return True
    return False


def _dedupe_loops(text: str) -> str:
    """Strip Qwen3 'thinking mode' sentence loops and hedging prefaces."""

    sentences = re.split(r"(?<=[.?!])\s+", text)
    kept: list[str] = []
    seen: set[str] = set()
    for sentence in sentences:
        sentence = sentence.strip()
        if _is_noise_sentence(sentence):
            continue
        key = re.sub(r"\s+", " ", sentence[:100])
        if key in seen:
            continue
        seen.add(key)
        kept.append(sentence)
    return " ".join(kept)


def _strip_ngram_tail(text: str, n: int = 5, min_repeats: int = 3) -> str:
    """Trim trailing n-gram loops.

    When Qwen3-VL's thinking mode drifts, it sometimes re-emits the same
    5-token window three or more times at the tail of a sentence. This
    function detects such loops and keeps only the first occurrence.

    Args:
        text: The raw transcription.
        n: Window size in whitespace-separated tokens.
        min_repeats: Loop is trimmed only if the tail n-gram repeats at
            least this many times consecutively.

    Returns:
        ``text`` with the looping tail removed, or the original ``text``
        when no loop is detected.
    """

    tokens = text.split()
    if len(tokens) < n * min_repeats:
        return text
    tail = tokens[-n:]
    repeats = 1
    j = len(tokens) - n
    while j >= n and tokens[j - n : j] == tail:
        repeats += 1
        j -= n
    if repeats >= min_repeats:
        return " ".join(tokens[: j + n])
    return text


def warmup() -> None:
    """Pre-load the model into VRAM with a tiny request.

    Uses :data:`_WARMUP_TIMEOUT` (60 s) rather than the per-page ceiling so
    a hung daemon at startup surfaces quickly instead of hiding behind the
    long per-page budget.
    """

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": "ping",
        "stream": False,
        "keep_alive": _KEEP_ALIVE,
        "options": {"num_predict": 1},
    }
    response = httpx.post(
        _GENERATE_URL,
        json=payload,
        timeout=_WARMUP_TIMEOUT,
    )
    response.raise_for_status()


def transcribe_page(png_path: Path, *, course_name: str | None = None) -> str:
    """Transcribe a single page via local Qwen3-VL.

    Args:
        png_path: Absolute path to the rendered page PNG.
        course_name: Course name for the prompt; falls back to the generic
            ``math / physics`` default when ``None`` / blank.

    Returns:
        Markdown transcription; empty string if the model returned nothing.
    """

    b64 = _image_to_b64(Path(png_path))
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": build_prompt(course_name),
        "images": [b64],
        "stream": False,
        "think": False,
        "keep_alive": _KEEP_ALIVE,
        "options": {
            "temperature": 0.1,
            "num_ctx": 4096,
            "num_predict": _MAX_TOKENS,
            "repeat_penalty": 1.3,
            "repeat_last_n": 256,
        },
    }
    response = httpx.post(
        _GENERATE_URL,
        json=payload,
        timeout=_PER_PAGE_TIMEOUT,
    )
    response.raise_for_status()
    body = response.json() if response.headers.get("content-type", "").startswith(
        "application/json"
    ) else json.loads(response.text)
    text = body.get("response", "") or body.get("thinking", "")
    text = text.replace("<think>", "").replace("</think>", "").strip()
    return _strip_ngram_tail(_dedupe_loops(text))


def transcribe_pages(
    png_paths: list[Path],
    *,
    course_name: str | None = None,
    max_workers: int = 2,
) -> list[str]:
    """Transcribe pages with a warmup + bounded concurrency.

    Args:
        png_paths: Absolute paths to page PNGs.
        course_name: Course name forwarded to :func:`build_prompt`.
        max_workers: Thread pool size; keep small because Ollama is GPU-bound.

    Returns:
        Markdown per page, preserving input order.
    """

    if not png_paths:
        return []
    try:
        warmup()
    except httpx.HTTPError:
        # Continue without warmup — the first real call will pay the cold
        # start, which is acceptable. Don't swallow the failure on real pages.
        pass
    results: list[str] = [""] * len(png_paths)
    with ThreadPoolExecutor(max_workers=max(1, max_workers)) as pool:
        future_to_idx = {
            pool.submit(transcribe_page, Path(p), course_name=course_name): i
            for i, p in enumerate(png_paths)
        }
        for fut in future_to_idx:
            idx = future_to_idx[fut]
            results[idx] = fut.result()
    return results


__all__ = [
    "OLLAMA_MODEL",
    "PROMPT_TEMPLATE",
    "build_prompt",
    "warmup",
    "transcribe_page",
    "transcribe_pages",
]
