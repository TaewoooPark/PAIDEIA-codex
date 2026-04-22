"""``ingest_pdfs`` MCP tool.

Renders every ``materials/**/*.pdf`` to PNG at dpi=160, resizes to <=1800 px on
the long edge, runs the selected OCR engine per page, and writes a clean
GitHub-flavored markdown file to ``converted/<category>/<stem>.md`` with a
provenance header.

Parallelism strategy: one worker process per PDF (bounded by
``max_workers``); OCR pages sequentially inside the worker. This matches the
"one agent per PDF, sequential pages" contract from VISION.md.
"""

from __future__ import annotations

import datetime
import os
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from PIL import Image
from pdf2image import convert_from_path

_CATEGORIES = ("lectures", "textbook", "homework", "solutions")
_DPI = 160
_MAX_LONG_EDGE = 1800
_PAGE_SEPARATOR = "\n\n---\n\n"


def _default_workers(engine: str) -> int:
    """Pick a conservative worker count per engine."""

    if engine == "openai-vision":
        return 4
    if engine == "qwen3-vl":
        return 1  # GPU-bound locally
    # tesseract
    return max(1, (os.cpu_count() or 4) // 2)


def _enumerate_pdfs(
    root: Path,
    categories: list[str] | None,
) -> list[tuple[Path, str]]:
    """Return ``(pdf_path, category)`` for every materials PDF under filter."""

    materials = root / "materials"
    if not materials.exists():
        return []
    wanted = set(categories) if categories else set(_CATEGORIES)
    out: list[tuple[Path, str]] = []
    for cat in sorted(wanted):
        cat_dir = materials / cat
        if not cat_dir.exists():
            continue
        for pdf in sorted(cat_dir.rglob("*.pdf")):
            out.append((pdf, cat))
    return out


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
    """Render ``pdf_path`` to ``p01.png``..``pNN.png`` inside ``scratch_dir``.

    Returns the sorted list of PNG paths.
    """

    scratch_dir.mkdir(parents=True, exist_ok=True)
    images = convert_from_path(str(pdf_path), dpi=_DPI)
    page_paths: list[Path] = []
    for i, img in enumerate(images, 1):
        out = scratch_dir / f"p{i:02d}.png"
        img.save(out, "PNG", optimize=True)
        _resize_in_place(out)
        page_paths.append(out)
    return page_paths


def _provenance_header(
    source_rel: str,
    engine: str,
    pages: int,
    ingested_at: str,
) -> str:
    """Build the HTML-comment provenance block for a converted markdown."""

    return (
        f"<!-- source: {source_rel} -->\n"
        f"<!-- engine: {engine} -->\n"
        f"<!-- pages: {pages} -->\n"
        f"<!-- ingested: {ingested_at} -->\n\n"
    )


def _process_one_pdf(task: dict) -> dict:
    """Worker entry point: OCR one PDF and write its markdown.

    Args:
        task: ``{pdf_path, category, destination, engine, source_rel, root}``.

    Returns:
        ``{status, pdf, destination, pages, error?}``.
    """

    from .ocr import run_ocr  # lazy to keep worker startup light

    pdf_path = Path(task["pdf_path"])
    destination = Path(task["destination"])
    engine = task["engine"]
    source_rel = task["source_rel"]
    root = Path(task["root"])
    ingested_at = task["ingested_at"]

    scratch_root = Path(tempfile.mkdtemp(prefix="paideia-ingest-"))
    try:
        page_paths = _render_pdf(pdf_path, scratch_root)
        try:
            pages_md = run_ocr(
                engine,
                page_paths,
                project_root=str(root),
            )
        except Exception as exc:  # noqa: BLE001 — propagate as structured error
            return {
                "status": "failed",
                "pdf": source_rel,
                "destination": str(destination),
                "pages": len(page_paths),
                "error": f"{type(exc).__name__}: {exc}",
            }

        header = _provenance_header(
            source_rel=source_rel,
            engine=engine,
            pages=len(page_paths),
            ingested_at=ingested_at,
        )
        title = f"# {pdf_path.stem}\n\n"
        body = _PAGE_SEPARATOR.join(
            (page_md or "").strip() for page_md in pages_md
        )
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(header + title + body + "\n", encoding="utf-8")
        return {
            "status": "converted",
            "pdf": source_rel,
            "destination": str(destination),
            "pages": len(page_paths),
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "status": "failed",
            "pdf": source_rel,
            "destination": str(destination),
            "pages": 0,
            "error": f"{type(exc).__name__}: {exc}",
        }
    finally:
        # Best-effort cleanup of the scratch directory.
        try:
            for child in scratch_root.glob("*"):
                try:
                    child.unlink()
                except OSError:
                    pass
            scratch_root.rmdir()
        except OSError:
            pass


def ingest_pdfs(
    engine: str = "openai-vision",
    force: bool = False,
    categories: list[str] | None = None,
    project_root: str | None = None,
) -> dict:
    """Render and OCR every materials PDF, writing converted markdown.

    Args:
        engine: ``openai-vision``, ``qwen3-vl``, or ``tesseract``.
        force: Reconvert even if the destination already exists.
        categories: Restrict to a subset of
            ``lectures|textbook|homework|solutions``.
        project_root: Project root; defaults to ``os.getcwd()``.

    Returns:
        ``{converted: [...], skipped: [...], failed: [{path, error}], engine,
        project_root}``.
    """

    root = Path(project_root or os.getcwd()).resolve()
    pdfs = _enumerate_pdfs(root, categories)
    ingested_at = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )

    tasks: list[dict] = []
    skipped: list[str] = []
    for pdf_path, category in pdfs:
        destination = root / "converted" / category / f"{pdf_path.stem}.md"
        source_rel = str(pdf_path.relative_to(root))
        if destination.exists() and not force:
            skipped.append(source_rel)
            continue
        tasks.append(
            {
                "pdf_path": str(pdf_path),
                "category": category,
                "destination": str(destination),
                "engine": engine,
                "source_rel": source_rel,
                "root": str(root),
                "ingested_at": ingested_at,
            }
        )

    converted: list[dict] = []
    failed: list[dict] = []

    if tasks:
        workers = max(1, _default_workers(engine))
        workers = min(workers, len(tasks))
        if workers == 1:
            for task in tasks:
                result = _process_one_pdf(task)
                _collect(result, converted, failed)
        else:
            with ProcessPoolExecutor(max_workers=workers) as pool:
                futures = [pool.submit(_process_one_pdf, t) for t in tasks]
                for fut in as_completed(futures):
                    _collect(fut.result(), converted, failed)

    return {
        "engine": engine,
        "project_root": str(root),
        "converted": converted,
        "skipped": skipped,
        "failed": failed,
    }


def _collect(
    result: dict,
    converted: list[dict],
    failed: list[dict],
) -> None:
    """Route a worker result into the converted/failed bucket."""

    if result.get("status") == "converted":
        converted.append(
            {
                "path": result["pdf"],
                "destination": result["destination"],
                "pages": result["pages"],
            }
        )
    else:
        failed.append(
            {
                "path": result.get("pdf"),
                "destination": result.get("destination"),
                "error": result.get("error", "unknown error"),
            }
        )


__all__ = ["ingest_pdfs"]
