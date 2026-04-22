"""OCR engine dispatch for paideia-mcp.

Exposes ``run_ocr(engine, png_paths, *, project_root=None) -> list[str]`` which
routes to the requested engine module and returns markdown per page.
"""

from __future__ import annotations

import os
from pathlib import Path

_SUPPORTED = ("openai-vision", "qwen3-vl", "tesseract")


def run_ocr(
    engine: str,
    png_paths: list[Path] | list[str],
    *,
    project_root: str | None = None,
) -> list[str]:
    """Dispatch OCR for a list of PNG paths.

    Args:
        engine: One of ``openai-vision``, ``qwen3-vl``, ``tesseract``.
        png_paths: Absolute paths (or strings) pointing at rendered PNG pages.
        project_root: Optional project root hint; currently unused but kept
            for symmetry with the other public tools.

    Returns:
        One markdown string per input page, in the same order.
    """

    if engine not in _SUPPORTED:
        raise ValueError(
            f"unknown OCR engine '{engine}'. Supported: {', '.join(_SUPPORTED)}"
        )
    paths = [Path(p) for p in png_paths]
    # The presence of project_root is noted but intentionally not plumbed into
    # the engine modules — they operate on absolute PNG paths only.
    _ = project_root
    _ = os.environ  # touch to show we respect env (OPENAI_API_KEY etc.)

    if engine == "openai-vision":
        from . import openai_vision

        return openai_vision.transcribe_pages(paths)
    if engine == "qwen3-vl":
        from . import qwen3vl

        return qwen3vl.transcribe_pages(paths)
    # tesseract
    from . import tesseract

    return tesseract.transcribe_pages(paths)


__all__ = ["run_ocr"]
