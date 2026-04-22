"""``grade_pdf`` MCP tool.

OCRs a single hand-written answer PDF and writes the transcription to
``answers/converted/<stem>.md`` with a provenance + confidence-tier header.
The grading itself (strategy matching against reference solutions) is the
skill's responsibility — this tool is strictly the OCR step.
"""

from __future__ import annotations

import datetime
import os
import tempfile
from pathlib import Path

from PIL import Image
from pdf2image import convert_from_path

from .ocr import run_ocr
from .phase import parse_meta

_DPI = 200
_MAX_LONG_EDGE = 1800

_TIER_BY_ENGINE = {
    "openai-vision": "high",
    "qwen3-vl": "medium",
    "tesseract": "low",
}


def _read_course_meta_engine(root: Path) -> str | None:
    """Return the ``OCR_ENGINE`` key from ``.course-meta``, if any."""

    meta = parse_meta(root)
    value = meta.get("OCR_ENGINE")
    if not value:
        return None
    normalized = value.strip().lower()
    # Accept legacy aliases from the Claude plugin.
    if normalized == "ollama":
        return "qwen3-vl"
    if normalized == "claude":
        return "openai-vision"
    if normalized in _TIER_BY_ENGINE:
        return normalized
    return None


def _resize_in_place(png_path: Path) -> None:
    """Downscale ``png_path`` if its long edge exceeds the ceiling."""

    with Image.open(png_path) as img:
        width, height = img.size
        if max(width, height) <= _MAX_LONG_EDGE:
            return
        scale = _MAX_LONG_EDGE / max(width, height)
        new_size = (int(width * scale), int(height * scale))
        resized = img.resize(new_size, Image.LANCZOS)
    resized.save(png_path, "PNG", optimize=True)


def _render_pdf(pdf_path: Path, scratch_dir: Path) -> list[Path]:
    """Render the PDF to page PNGs, resized to the long-edge ceiling."""

    scratch_dir.mkdir(parents=True, exist_ok=True)
    images = convert_from_path(str(pdf_path), dpi=_DPI)
    paths: list[Path] = []
    for i, img in enumerate(images, 1):
        out = scratch_dir / f"p{i:02d}.png"
        img.save(out, "PNG", optimize=True)
        _resize_in_place(out)
        paths.append(out)
    return paths


def _resolve_pdf(raw_path: str, root: Path) -> Path:
    """Resolve ``raw_path`` to an absolute PDF under ``root`` or absolute."""

    candidate = Path(raw_path)
    if candidate.is_absolute():
        return candidate.resolve()
    return (root / candidate).resolve()


def grade_pdf(
    path: str,
    engine: str | None = None,
    project_root: str | None = None,
) -> dict:
    """OCR an answer PDF and write ``answers/converted/<stem>.md``.

    Args:
        path: Answer PDF path (absolute or relative to ``project_root``).
        engine: Override the OCR engine; defaults to ``.course-meta``
            ``OCR_ENGINE`` or ``openai-vision`` when absent.
        project_root: Project root; defaults to ``os.getcwd()``.

    Returns:
        ``{markdown_path, tier, engine, pages_processed, source}``.
    """

    root = Path(project_root or os.getcwd()).resolve()
    pdf = _resolve_pdf(path, root)
    if not pdf.exists():
        raise FileNotFoundError(f"answer PDF not found: {pdf}")

    selected_engine = engine or _read_course_meta_engine(root) or "openai-vision"
    if selected_engine not in _TIER_BY_ENGINE:
        raise ValueError(
            f"unknown OCR engine '{selected_engine}'. "
            f"Supported: {', '.join(_TIER_BY_ENGINE)}"
        )
    tier = _TIER_BY_ENGINE[selected_engine]

    destination = root / "answers" / "converted" / f"{pdf.stem}.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix="paideia-grade-"))
    try:
        png_paths = _render_pdf(pdf, scratch)
        pages_md = run_ocr(
            selected_engine,
            png_paths,
            project_root=str(root),
        )
    finally:
        for child in scratch.glob("*"):
            try:
                child.unlink()
            except OSError:
                pass
        try:
            scratch.rmdir()
        except OSError:
            pass

    try:
        source_rel = str(pdf.relative_to(root))
    except ValueError:
        source_rel = str(pdf)
    ingested_at = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    header = (
        "# Vision-OCR transcription\n\n"
        f"<!-- source: {source_rel} -->\n"
        f"<!-- engine: {selected_engine} -->\n"
        f"<!-- tier: {tier} -->\n"
        f"<!-- pages: {len(png_paths)} -->\n"
        f"<!-- ingested: {ingested_at} -->\n\n"
    )
    body_parts: list[str] = []
    for i, page_md in enumerate(pages_md, 1):
        body_parts.append(f"## Page {i}\n\n{(page_md or '').strip()}\n")
    destination.write_text(header + "\n".join(body_parts), encoding="utf-8")

    return {
        "markdown_path": str(destination),
        "tier": tier,
        "engine": selected_engine,
        "pages_processed": len(png_paths),
        "source": source_rel,
    }


__all__ = ["grade_pdf"]
