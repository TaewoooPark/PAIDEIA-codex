"""Smoke tests for ``paideia_mcp.phase``.

Builds tiny fake course roots and asserts that ``detect_phase`` follows the
setup -> diag -> drill -> mock -> cram -> cool ladder, plus covers meta
parsing and top-miss extraction.
"""

from __future__ import annotations

from pathlib import Path

from paideia_mcp import phase


def _write(path: Path, body: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def test_detect_phase_setup(tmp_path: Path) -> None:
    assert phase.detect_phase(tmp_path, None) == "setup"


def test_detect_phase_diag(tmp_path: Path) -> None:
    _write(tmp_path / "course-index" / "patterns.md", "# patterns")
    assert phase.detect_phase(tmp_path, None) == "diag"


def test_detect_phase_drill(tmp_path: Path) -> None:
    _write(tmp_path / "course-index" / "patterns.md", "# patterns")
    _write(tmp_path / "quizzes" / "q1.md", "# quiz")
    assert phase.detect_phase(tmp_path, None) == "drill"


def test_detect_phase_mock_takes_priority_over_drill(tmp_path: Path) -> None:
    _write(tmp_path / "course-index" / "patterns.md", "# patterns")
    _write(tmp_path / "quizzes" / "q1.md", "# quiz")
    _write(tmp_path / "mock" / "mock_90.md", "# mock")
    assert phase.detect_phase(tmp_path, None) == "mock"


def test_detect_phase_cram(tmp_path: Path) -> None:
    _write(tmp_path / "cheatsheet" / "final.md", "# cheat")
    assert phase.detect_phase(tmp_path, None) == "cram"


def test_detect_phase_cool_overrides_everything(tmp_path: Path) -> None:
    _write(tmp_path / "cheatsheet" / "final.md", "# cheat")
    assert phase.detect_phase(tmp_path, 0) == "cool"


def test_parse_meta_parses_known_keys(tmp_path: Path) -> None:
    _write(
        tmp_path / ".course-meta",
        "COURSE_NAME: DM MAS.20075\nEXAM_DATE: 2026-04-21\nOCR_ENGINE: qwen3-vl\n",
    )
    meta = phase.parse_meta(tmp_path)
    assert meta["COURSE_NAME"] == "DM MAS.20075"
    assert meta["EXAM_DATE"] == "2026-04-21"
    assert meta["OCR_ENGINE"] == "qwen3-vl"


def test_parse_meta_missing_returns_empty(tmp_path: Path) -> None:
    assert phase.parse_meta(tmp_path) == {}


def test_days_until_invalid_returns_none() -> None:
    assert phase.days_until("") is None
    assert phase.days_until("not-a-date") is None


def test_top_miss_from_weakmap(tmp_path: Path) -> None:
    _write(
        tmp_path / "weakmap" / "weakmap_2026-04-22.md",
        "# weakmap\n\nTop: P7 appears repeatedly.",
    )
    assert phase.top_miss(tmp_path) == "P7"


def test_top_miss_from_error_log(tmp_path: Path) -> None:
    _write(
        tmp_path / "errors" / "log.md",
        "- pattern: P3\n- pattern: P3\n- pattern: P5\n",
    )
    assert phase.top_miss(tmp_path) == "P3"


def test_top_miss_no_signal(tmp_path: Path) -> None:
    assert phase.top_miss(tmp_path) is None


def test_course_phase_returns_snapshot(tmp_path: Path) -> None:
    _write(
        tmp_path / ".course-meta",
        "COURSE_NAME: DM\nEXAM_DATE: 2099-01-01\n",
    )
    _write(tmp_path / "course-index" / "patterns.md", "# patterns")
    snapshot = phase.course_phase(project_root=str(tmp_path))
    assert snapshot["course_name"] == "DM"
    assert snapshot["phase"] == "diag"
    assert isinstance(snapshot["days_until_exam"], int)
