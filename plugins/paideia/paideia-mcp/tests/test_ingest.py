"""Regression tests for ``paideia_mcp.ingest``."""

from __future__ import annotations

from pathlib import Path

from reportlab.pdfgen import canvas

from paideia_mcp import ingest


def _make_pdf(path: Path, *lines: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(path))
    y = 720
    for line in lines:
        pdf.drawString(72, y, line)
        y -= 24
    pdf.save()


def test_markdown_copy_through_keeps_provenance(tmp_path: Path) -> None:
    source = tmp_path / "materials" / "lectures" / "intro.md"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text("# Intro\n\nEuler identity.\n", encoding="utf-8")

    result = ingest.ingest_pdfs(project_root=str(tmp_path))

    converted = tmp_path / "converted" / "lectures" / "intro.md"
    assert converted.exists()
    body = converted.read_text(encoding="utf-8")
    assert "<!-- source: materials/lectures/intro.md -->" in body
    assert "<!-- engine: copy-through -->" in body
    assert "# Intro" in body
    assert result["converted"][0]["path"] == "materials/lectures/intro.md"


def test_duplicate_stems_in_nested_directories_do_not_collide(tmp_path: Path, monkeypatch) -> None:
    _make_pdf(
        tmp_path / "materials" / "homework" / "setA" / "problem.pdf",
        "Set A problem",
    )
    _make_pdf(
        tmp_path / "materials" / "homework" / "setB" / "problem.pdf",
        "Set B problem",
    )
    monkeypatch.setattr(ingest, "_default_workers", lambda engine: 1)

    result = ingest.ingest_pdfs(project_root=str(tmp_path))

    pending = {Path(item["destination"]).relative_to(tmp_path) for item in result["pending"]}
    assert pending == {
        Path("converted/homework/setA/problem.md"),
        Path("converted/homework/setB/problem.md"),
    }
    cache_dirs = {
        Path(item["page_paths"][0]).relative_to(tmp_path).parent for item in result["pending"]
    }
    assert cache_dirs == {
        Path(".paideia-cache/pages/homework/setA/problem"),
        Path(".paideia-cache/pages/homework/setB/problem"),
    }
    assert result["failed"] == []
