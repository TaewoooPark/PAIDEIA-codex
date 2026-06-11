"""Regression tests for ``paideia_mcp.analyze``."""

from __future__ import annotations

from pathlib import Path

from paideia_mcp.analyze import build_course_index


def _write(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def test_build_course_index_writes_draft_files(tmp_path: Path) -> None:
    _write(
        tmp_path / "converted" / "lectures" / "lec1.md",
        "# Lecture 1\n\n## Residue theorem\n\nResidue theorem overview.\n",
    )
    _write(
        tmp_path / "converted" / "textbook" / "ch1.md",
        "# Chapter 1\n\n## Contour integrals\n\nResidue theorem and contour methods.\n",
    )
    _write(
        tmp_path / "converted" / "solutions" / "hw1_sol.md",
        "# Solution 1\n\nUse the residue at the pole to evaluate the contour integral.\n",
    )
    _write(
        tmp_path / "converted" / "solutions" / "hw2_sol.md",
        "# Solution 2\n\nA second residue computation at the pole closes the contour.\n",
    )
    _write(
        tmp_path / "converted" / "homework" / "hw1.md",
        "# Homework 1\n\nResidue theorem practice on contour integrals.\n",
    )

    result = build_course_index(project_root=str(tmp_path), weak_zones="residue")

    assert result["ready"] is True
    assert result["wrote_index"] is True
    summary = (tmp_path / "course-index" / "summary.md").read_text(encoding="utf-8")
    patterns = (tmp_path / "course-index" / "patterns.md").read_text(encoding="utf-8")
    coverage = (tmp_path / "course-index" / "coverage.md").read_text(encoding="utf-8")
    assert "# Summary" in summary
    assert "### P1. Residue evaluation" in patterns
    assert "converted/homework/hw1.md" in coverage


def test_build_course_index_respects_existing_files_without_force(tmp_path: Path) -> None:
    _write(tmp_path / "converted" / "lectures" / "lec1.md", "# Lecture 1\n\n## Fourier series\n")

    first = build_course_index(project_root=str(tmp_path))
    assert first["wrote_index"] is True

    summary_path = tmp_path / "course-index" / "summary.md"
    summary_path.write_text("manual summary\n", encoding="utf-8")

    second = build_course_index(project_root=str(tmp_path))
    assert second["wrote_index"] is False
    assert summary_path.read_text(encoding="utf-8") == "manual summary\n"

    third = build_course_index(project_root=str(tmp_path), force=True)
    assert third["wrote_index"] is True
    assert "manual summary" not in summary_path.read_text(encoding="utf-8")


def test_build_course_index_promotes_ocr_plaintext_headings(tmp_path: Path) -> None:
    _write(
        tmp_path / "converted" / "lectures" / "lecture_residues.md",
        "\n".join(
            [
                "<!-- source: materials/lectures/lecture_residues.pdf -->",
                "<!-- engine: tesseract -->",
                "",
                "# lecture_residues",
                "",
                "Lecture 1: Residues and Laurent Series",
                "Section 1.1 Singularities and Laurent series",
                "Section 1.2 Residue theorem",
                "Integral over closed contour C of f(z) dz = 2 pi i sum residues.",
            ]
        ),
    )
    _write(
        tmp_path / "converted" / "textbook" / "chapter_residue_basics.md",
        "# chapter_residue_basics\n\nChapter 1 Residue Calculus\n",
    )
    _write(
        tmp_path / "converted" / "solutions" / "hw1_solutions.md",
        "# hw1_solutions\n\nSolution HW1-P1. Compute residues at the poles.\n",
    )
    _write(
        tmp_path / "converted" / "homework" / "hw1.md",
        "# hw1\n\nHomework 1\nProblem HW1-P1. Residue theorem practice.\n",
    )

    result = build_course_index(project_root=str(tmp_path), weak_zones="residue")

    assert result["ready"] is True
    summary = (tmp_path / "course-index" / "summary.md").read_text(encoding="utf-8")
    coverage = (tmp_path / "course-index" / "coverage.md").read_text(encoding="utf-8")
    assert "Lecture 1. Residues and Laurent Series" in summary
    assert "§1.2. Residue theorem" in summary
    assert "lectureresidues" not in summary
    assert "`converted/homework/hw1.md`" in coverage
    assert "| §1.2 | Residue theorem * | 1 |" in coverage
    assert "hw1 solutions" not in summary.lower()
