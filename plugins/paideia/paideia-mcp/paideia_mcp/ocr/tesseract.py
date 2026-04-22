"""Local pytesseract OCR engine.

Fastest and lowest fidelity of the three engines; primarily a fallback when
neither OpenAI nor a local VLM is available. Prefers ``eng+kor`` when both
traineddata sets are installed, falls back gracefully to whichever single
language is available so English-only courses work without ``kor.traineddata``
and Korean-only installs work without ``eng``.
"""

from __future__ import annotations

import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Union

from PIL import Image

_PREFERRED_LANGS: tuple[str, ...] = ("eng", "kor")
_resolved_langs: str | None = None


def _resolve_langs() -> str:
    """Detect which preferred traineddata sets are installed and cache the result.

    Returns a ``+``-joined lang string in the preference order. Prints one
    stderr warning the first time a preferred language is missing so the user
    knows why Korean (or English) text may come out garbled, but keeps going
    instead of crashing — a partial lang set still OCR's the matching glyphs.

    Raises ``RuntimeError`` only when *none* of the preferred languages is
    installed, because at that point there's nothing to transcribe with.
    """

    global _resolved_langs
    if _resolved_langs is not None:
        return _resolved_langs

    import pytesseract

    try:
        available = set(pytesseract.get_languages(config=""))
    except Exception:
        available = set()

    chosen = [lang for lang in _PREFERRED_LANGS if lang in available]
    if not chosen:
        raise RuntimeError(
            "tesseract: neither eng nor kor traineddata is installed. "
            "Run `brew install tesseract-lang` on macOS or "
            "`apt-get install tesseract-ocr-eng tesseract-ocr-kor` on Ubuntu, "
            "then retry."
        )

    missing = [lang for lang in _PREFERRED_LANGS if lang not in available]
    if missing:
        sys.stderr.write(
            f"paideia-mcp: tesseract falling back to lang={'+'.join(chosen)} "
            f"(missing traineddata: {', '.join(missing)}). "
            "Install `tesseract-lang` (macOS) or `tesseract-ocr-<lang>` "
            "(Ubuntu) for full coverage.\n"
        )

    _resolved_langs = "+".join(chosen)
    return _resolved_langs


def _default_workers() -> int:
    """Pick a reasonable worker count, falling back to 4 when unknown."""

    return max(1, (os.cpu_count() or 4))


def transcribe_page(png_path: "Union[Path, str, Image.Image]") -> str:
    """Transcribe a single page with pytesseract.

    Args:
        png_path: Path to a PNG, or an already-opened ``PIL.Image``.

    Returns:
        Plain-text transcription (Tesseract produces no LaTeX).
    """

    import pytesseract  # lazy import — pytesseract requires the system binary

    langs = _resolve_langs()
    if isinstance(png_path, Image.Image):
        return pytesseract.image_to_string(png_path, lang=langs)
    with Image.open(Path(png_path)) as img:
        return pytesseract.image_to_string(img, lang=langs)


def transcribe_pages(
    png_paths: list[Path],
    *,
    max_workers: int | None = None,
) -> list[str]:
    """Transcribe pages in parallel with a CPU-sized pool.

    Args:
        png_paths: Absolute paths to page PNGs.
        max_workers: Override the default ``os.cpu_count()`` worker count.

    Returns:
        Plain-text transcription per page, preserving input order.
    """

    if not png_paths:
        return []
    workers = max_workers if max_workers is not None else _default_workers()
    workers = max(1, workers)
    results: list[str] = [""] * len(png_paths)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        future_to_idx = {
            pool.submit(transcribe_page, Path(p)): i
            for i, p in enumerate(png_paths)
        }
        for fut in future_to_idx:
            idx = future_to_idx[fut]
            results[idx] = fut.result()
    return results


__all__ = ["transcribe_page", "transcribe_pages"]
