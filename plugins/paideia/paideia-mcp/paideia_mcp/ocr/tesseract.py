"""Local pytesseract OCR engine (eng+kor).

Fastest and lowest fidelity of the three engines; primarily a fallback when
neither OpenAI nor a local VLM is available.
"""

from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Union

from PIL import Image

_LANGS = "eng+kor"


def _default_workers() -> int:
    """Pick a reasonable worker count, falling back to 4 when unknown."""

    return max(1, (os.cpu_count() or 4))


def transcribe_page(png_path: "Union[Path, str, Image.Image]") -> str:
    """Transcribe a single page with pytesseract (eng+kor).

    Args:
        png_path: Path to a PNG, or an already-opened ``PIL.Image``.

    Returns:
        Plain-text transcription (Tesseract produces no LaTeX).
    """

    import pytesseract  # lazy import — pytesseract requires the system binary

    if isinstance(png_path, Image.Image):
        return pytesseract.image_to_string(png_path, lang=_LANGS)
    with Image.open(Path(png_path)) as img:
        return pytesseract.image_to_string(img, lang=_LANGS)


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
