"""OpenAI Responses-API vision OCR engine.

Used as the default engine when ``OPENAI_API_KEY`` is set. Uploads each page as
a base64-encoded PNG and expects the model to return clean GitHub-flavored
markdown with LaTeX-preserved equations.
"""

from __future__ import annotations

import base64
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx

TRANSCRIPTION_PROMPT = (
    "Transcribe this page of a math/physics course PDF to clean "
    "GitHub-flavored Markdown. Preserve all equations as LaTeX ($...$ inline, "
    "$$...$$ display). Preserve section headings, lists, figure captions. "
    "Do not summarize. Do not add commentary. Output only the markdown "
    "content of the page."
)

_DEFAULT_MODEL = "gpt-5.4"
_RESPONSES_URL = "https://api.openai.com/v1/responses"
_REQUEST_TIMEOUT = 120.0


def _require_api_key() -> str:
    """Fetch OPENAI_API_KEY or raise an actionable RuntimeError."""

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY not set; cannot use openai-vision engine. "
            "Pick qwen3-vl or tesseract, or export OPENAI_API_KEY."
        )
    return api_key


def _extract_text(payload: dict) -> str:
    """Best-effort text extraction from a Responses-API JSON payload."""

    # Happy path — documented shape: output[0].content[0].text
    try:
        output = payload["output"]
        if output:
            content = output[0].get("content", [])
            for block in content:
                text = block.get("text") or block.get("content")
                if isinstance(text, str) and text.strip():
                    return text
    except (KeyError, IndexError, AttributeError, TypeError):
        pass
    # Fallback: aggregated output_text
    output_text = payload.get("output_text")
    if isinstance(output_text, str) and output_text.strip():
        return output_text
    return ""


def transcribe_page(png_path: Path, *, model: str = _DEFAULT_MODEL) -> str:
    """Transcribe a single PNG via the OpenAI Responses API.

    Args:
        png_path: Absolute path to the rendered page PNG.
        model: OpenAI model id; defaults to ``gpt-5.4``.

    Returns:
        Markdown transcription of the page. Empty string if the model
        returned no text content.
    """

    api_key = _require_api_key()
    b64 = base64.b64encode(Path(png_path).read_bytes()).decode()
    payload = {
        "model": model,
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{b64}",
                    },
                    {
                        "type": "input_text",
                        "text": TRANSCRIPTION_PROMPT,
                    },
                ],
            }
        ],
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = httpx.post(
        _RESPONSES_URL,
        json=payload,
        headers=headers,
        timeout=_REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return _extract_text(response.json())


def transcribe_pages(
    png_paths: list[Path],
    *,
    max_workers: int = 4,
    model: str = _DEFAULT_MODEL,
) -> list[str]:
    """Transcribe pages concurrently.

    Args:
        png_paths: Absolute paths to page PNGs.
        max_workers: Thread pool size; defaults to 4 (rate-limit friendly).
        model: OpenAI model id.

    Returns:
        Markdown per page, in the same order as ``png_paths``.
    """

    if not png_paths:
        return []
    # Fail fast before we spin up the pool if OPENAI_API_KEY is unset.
    _require_api_key()
    results: list[str] = [""] * len(png_paths)
    with ThreadPoolExecutor(max_workers=max(1, max_workers)) as pool:
        future_to_idx = {
            pool.submit(transcribe_page, Path(p), model=model): i
            for i, p in enumerate(png_paths)
        }
        for fut in future_to_idx:
            idx = future_to_idx[fut]
            results[idx] = fut.result()
    return results


__all__ = ["TRANSCRIPTION_PROMPT", "transcribe_page", "transcribe_pages"]
