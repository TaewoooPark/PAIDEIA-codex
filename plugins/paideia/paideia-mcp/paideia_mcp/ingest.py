"""``ingest_pdfs`` MCP tool.

Two modes, picked by the requested engine:

* ``codex-native`` (default) — render every ``materials/**/*.pdf`` to PNGs in
  ``.paideia-cache/pages/<category>/<relative-path>/p01.png`` and return a
  *pending* manifest. The calling skill then asks Codex CLI to read those page
  images directly with its bundled vision and writes the converted markdown
  itself.
* ``qwen3-vl`` / ``tesseract`` — render to a scratch directory, OCR in-process
  via :mod:`paideia_mcp.ocr`, and write ``converted/<category>/<relative>.md``
  with a provenance header.

Additionally, ``materials/**/*.md`` is copied straight through to
``converted/**`` with provenance metadata so mixed-source courses work without a
PDF-only workflow.
"""

from __future__ import annotations

import datetime
import os
import shutil
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from PIL import Image
from pdf2image import convert_from_path

from .ocr import _IN_PROCESS

_CATEGORIES = ("lectures", "textbook", "homework", "solutions")
_DPI = 160
_MAX_LONG_EDGE = 1800
_PAGE_SEPARATOR = "\n\n---\n\n"
_DEFAULT_ENGINE = "codex-native"
_CACHE_DIRNAME = ".paideia-cache"
_COPY_THROUGH_ENGINE = "copy-through"


def _default_workers(engine: str) -> int:
    """Pick a conservative worker count per engine."""

    if engine == "codex-native":
        return max(1, (os.cpu_count() or 4) // 2)
    if engine == "qwen3-vl":
        return 1
    return max(1, (os.cpu_count() or 4) // 2)


def _enumerate_materials(
    root: Path,
    categories: list[str] | None,
) -> list[dict[str, str]]:
    """Return every source file under ``materials/`` with its category metadata."""

    materials = root / "materials"
    if not materials.exists():
        return []
    wanted = set(categories) if categories else set(_CATEGORIES)
    out: list[dict[str, str]] = []
    for category in sorted(wanted):
        category_dir = materials / category
        if not category_dir.exists():
            continue
        for ext, kind in (("md", "markdown"), ("pdf", "pdf")):
            for source in sorted(category_dir.rglob(f"*.{ext}")):
                rel = source.relative_to(category_dir)
                out.append(
                    {
                        "path": str(source),
                        "category": category,
                        "kind": kind,
                        "relative": str(rel),
                    }
                )
    return out


def _destination_for(
    root: Path,
    category: str,
    relative_inside_category: str,
) -> Path:
    """Map a source path under ``materials/<category>`` to ``converted/**``."""

    rel = Path(relative_inside_category)
    return root / "converted" / category / rel.with_suffix(".md")


def _cache_dir_for(
    root: Path,
    category: str,
    relative_inside_category: str,
) -> Path:
    """Return the per-source raster cache directory."""

    rel = Path(relative_inside_category)
    return root / _CACHE_DIRNAME / "pages" / category / rel.with_suffix("")


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
    """Render ``pdf_path`` to ``p01.png``..``pNN.png`` inside ``scratch_dir``."""

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


def _copy_markdown_source(task: dict[str, str]) -> dict:
    """Copy ``materials/**/*.md`` into ``converted/**`` with provenance."""

    source = Path(task["path"])
    destination = Path(task["destination"])
    source_rel = task["source_rel"]
    ingested_at = task["ingested_at"]

    try:
        body = source.read_text(encoding="utf-8")
        header = _provenance_header(
            source_rel=source_rel,
            engine=_COPY_THROUGH_ENGINE,
            pages=0,
            ingested_at=ingested_at,
        )
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(header + body.rstrip() + "\n", encoding="utf-8")
        return {
            "status": "converted",
            "pdf": source_rel,
            "destination": str(destination),
            "pages": 0,
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "status": "failed",
            "pdf": source_rel,
            "destination": str(destination),
            "pages": 0,
            "error": f"{type(exc).__name__}: {exc}",
        }


def _process_one_pdf_inproc(task: dict) -> dict:
    """Worker entry point for in-process engines (qwen3-vl / tesseract)."""

    from .ocr import run_ocr

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
        except Exception as exc:  # noqa: BLE001
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
        body = _PAGE_SEPARATOR.join((page_md or "").strip() for page_md in pages_md)
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
        shutil.rmtree(scratch_root, ignore_errors=True)


def _process_one_pdf_rasterize(task: dict) -> dict:
    """Worker entry point for the codex-native engine: rasterize to a cache."""

    pdf_path = Path(task["pdf_path"])
    destination = Path(task["destination"])
    source_rel = task["source_rel"]
    cache_dir = Path(task["cache_dir"])

    try:
        if cache_dir.exists():
            shutil.rmtree(cache_dir, ignore_errors=True)
        page_paths = _render_pdf(pdf_path, cache_dir)
        return {
            "status": "pending",
            "pdf": source_rel,
            "destination": str(destination),
            "pages": len(page_paths),
            "page_paths": [str(p) for p in page_paths],
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "status": "failed",
            "pdf": source_rel,
            "destination": str(destination),
            "pages": 0,
            "error": f"{type(exc).__name__}: {exc}",
        }


def ingest_pdfs(
    engine: str = _DEFAULT_ENGINE,
    force: bool = False,
    categories: list[str] | None = None,
    project_root: str | None = None,
) -> dict:
    """Render and/or copy every supported file under ``materials/``."""

    root = Path(project_root or os.getcwd()).resolve()
    sources = _enumerate_materials(root, categories)
    ingested_at = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )

    is_inproc = engine in _IN_PROCESS

    tasks: list[dict] = []
    skipped: list[str] = []
    pending_categories: dict[str, str] = {}
    converted: list[dict] = []
    pending: list[dict] = []
    failed: list[dict] = []
    claimed_destinations: dict[str, str] = {}

    for source in sources:
        source_path = Path(source["path"])
        category = source["category"]
        relative = source["relative"]
        destination = _destination_for(root, category, relative)
        source_rel = str(source_path.relative_to(root))
        destination_key = str(destination.relative_to(root))

        previous = claimed_destinations.get(destination_key)
        if previous is not None and previous != source_rel:
            failed.append(
                {
                    "path": source_rel,
                    "destination": str(destination),
                    "error": f"destination collision with {previous}",
                }
            )
            continue
        claimed_destinations[destination_key] = source_rel

        if destination.exists() and not force:
            skipped.append(source_rel)
            continue

        if source["kind"] == "markdown":
            _collect(
                _copy_markdown_source(
                    {
                        "path": str(source_path),
                        "destination": str(destination),
                        "source_rel": source_rel,
                        "ingested_at": ingested_at,
                    }
                ),
                converted,
                pending,
                failed,
                pending_categories,
            )
            continue

        if is_inproc:
            tasks.append(
                {
                    "pdf_path": str(source_path),
                    "category": category,
                    "destination": str(destination),
                    "engine": engine,
                    "source_rel": source_rel,
                    "root": str(root),
                    "ingested_at": ingested_at,
                }
            )
            continue

        cache_dir = _cache_dir_for(root, category, relative)
        tasks.append(
            {
                "pdf_path": str(source_path),
                "category": category,
                "destination": str(destination),
                "source_rel": source_rel,
                "cache_dir": str(cache_dir),
                "ingested_at": ingested_at,
            }
        )
        pending_categories[source_rel] = category

    if tasks:
        worker_fn = _process_one_pdf_inproc if is_inproc else _process_one_pdf_rasterize
        workers = max(1, _default_workers(engine))
        workers = min(workers, len(tasks))
        if workers == 1:
            for task in tasks:
                _collect(
                    worker_fn(task),
                    converted,
                    pending,
                    failed,
                    pending_categories,
                )
        else:
            with ProcessPoolExecutor(max_workers=workers) as pool:
                futures = [pool.submit(worker_fn, task) for task in tasks]
                for fut in as_completed(futures):
                    _collect(
                        fut.result(),
                        converted,
                        pending,
                        failed,
                        pending_categories,
                    )

    if is_inproc:
        return {
            "mode": "ocr-complete",
            "engine": engine,
            "project_root": str(root),
            "converted": converted,
            "skipped": skipped,
            "failed": failed,
        }
    return {
        "mode": "rasterize-only",
        "engine": engine,
        "project_root": str(root),
        "converted": converted,
        "pending": pending,
        "skipped": skipped,
        "failed": failed,
        "ingested_at": ingested_at,
    }


def _collect(
    result: dict,
    converted: list[dict],
    pending: list[dict],
    failed: list[dict],
    pending_categories: dict[str, str],
) -> None:
    """Route a worker result into the converted/pending/failed bucket."""

    status = result.get("status")
    if status == "converted":
        converted.append(
            {
                "path": result["pdf"],
                "destination": result["destination"],
                "pages": result["pages"],
            }
        )
    elif status == "pending":
        pending.append(
            {
                "path": result["pdf"],
                "destination": result["destination"],
                "pages": result["pages"],
                "page_paths": result["page_paths"],
                "category": pending_categories.get(result["pdf"], ""),
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
