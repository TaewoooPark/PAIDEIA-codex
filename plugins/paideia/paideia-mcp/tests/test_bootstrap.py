"""Regression tests for the PAIDEIA bootstrap script."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest


def _bootstrap_script() -> Path:
    return (
        Path(__file__).resolve().parents[2]
        / "skills"
        / "paideia-init-course"
        / "scripts"
        / "bootstrap.py"
    )


@pytest.mark.skipif(shutil.which("git") is None, reason="git not installed")
def test_bootstrap_merges_gitignore_into_existing_repo(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("existing-entry\n", encoding="utf-8")

    subprocess.run(
        [
            sys.executable,
            str(_bootstrap_script()),
            "--course-name",
            "Bootstrap Smoke",
            "--exam-date",
            "2099-01-01",
            "--exam-type",
            "final",
            "--weak-zones",
            "unknown",
            "--ocr-engine",
            "codex-native",
            "--root",
            str(tmp_path),
        ],
        check=True,
    )

    body = gitignore.read_text(encoding="utf-8")
    assert "existing-entry" in body
    assert "answers/*.pdf" in body
    assert "errors/log.md" not in body
    assert "answers/converted/*.md" not in body
