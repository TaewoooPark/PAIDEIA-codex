"""OCR engine dispatch for paideia-mcp.

Exposes ``run_ocr(engine, png_paths, *, project_root=None) -> list[str]`` which
routes to the requested engine module and returns markdown per page.

The ``codex-native`` engine is a special case: the MCP tool only rasterizes
PDFs to PNG and hands the manifest back to the calling skill, which then asks
Codex CLI to read the page images directly using its bundled vision (the same
vision ChatGPT Plus/Pro/Business subscribers already pay for). Calling
``run_ocr('codex-native', ...)`` therefore raises — there is no in-process OCR
step for that engine.
"""

from __future__ import annotations

from pathlib import Path

_SUPPORTED = ("codex-native", "qwen3-vl", "tesseract")
_IN_PROCESS = ("qwen3-vl", "tesseract")


def run_ocr(
    engine: str,
    png_paths: list[Path] | list[str],
    *,
    project_root: str | None = None,
) -> list[str]:
    """Dispatch OCR for a list of PNG paths.

    Args:
        engine: One of ``codex-native``, ``qwen3-vl``, ``tesseract``.
        png_paths: Absolute paths (or strings) pointing at rendered PNG pages.
        project_root: Optional project root hint; currently unused but kept
            for symmetry with the other public tools.

    Returns:
        One markdown string per input page, in the same order.

    Raises:
        ValueError: when ``engine`` is unknown.
        NotImplementedError: when ``engine == 'codex-native'`` — that engine is
            handled by the skill, not the MCP, because Codex CLI reads page
            images via its built-in vision rather than a separate OCR call.
    """

    if engine not in _SUPPORTED:
        raise ValueError(
            f"unknown OCR engine '{engine}'. Supported: {', '.join(_SUPPORTED)}"
        )
    if engine == "codex-native":
        raise NotImplementedError(
            "codex-native OCR is performed by the calling skill via Codex's "
            "bundled vision; the MCP only rasterizes pages. Skills should "
            "branch on the tool's mode='rasterize-only' response."
        )

    paths = [Path(p) for p in png_paths]
    _ = project_root  # noted but not plumbed; engines work on absolute paths

    if engine == "qwen3-vl":
        from . import qwen3vl

        return qwen3vl.transcribe_pages(paths)
    # tesseract
    from . import tesseract

    return tesseract.transcribe_pages(paths)


__all__ = ["run_ocr", "_SUPPORTED", "_IN_PROCESS"]
