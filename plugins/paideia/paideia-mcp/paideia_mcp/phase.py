"""Artifact-derived course phase detection.

Ports ``detect_phase``, ``top_miss``, ``days_until``, ``parse_meta`` from the
Claude Code plugin's ``scripts/statusline.py`` and exposes the ``course_phase``
MCP tool.

Phase detection is activity-based: a seeded ``patterns.md`` or an empty
``mock/`` file does not advance the phase on its own. The student must have
at least one graded entry in ``errors/log.md`` before the phase moves past
``diag``, and a mock-sourced entry before ``mock`` fires.
"""

from __future__ import annotations

import datetime
import glob
import re
from pathlib import Path

_PATTERN_ENTRY_RX = re.compile(r"^\s*pattern:\s*P\d+", re.MULTILINE)
_SOURCE_RX = re.compile(r"^\s*source:\s*(.+?)\s*$", re.MULTILINE)


def parse_meta(cwd: Path) -> dict[str, str]:
    """Parse ``<cwd>/.course-meta`` into a dict of KEY: VALUE lines.

    Args:
        cwd: Project root.

    Returns:
        Empty dict when the file is absent or unreadable.
    """

    meta: dict[str, str] = {}
    path = cwd / ".course-meta"
    if not path.exists():
        return meta
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return meta
    for line in text.splitlines():
        match = re.match(r"^\s*([A-Z_][A-Z0-9_]*)\s*:\s*(.+?)\s*$", line)
        if match:
            meta[match.group(1)] = match.group(2)
    return meta


def days_until(exam_date: str) -> int | None:
    """Whole-day delta until ``exam_date`` (YYYY-MM-DD).

    Args:
        exam_date: ISO-format date string.

    Returns:
        ``None`` if ``exam_date`` is malformed or missing.
    """

    try:
        target = datetime.datetime.strptime(
            (exam_date or "").strip(), "%Y-%m-%d"
        ).date()
    except (ValueError, AttributeError):
        return None
    return (target - datetime.date.today()).days


def _has_error_entries(cwd: Path) -> bool:
    """True if ``errors/log.md`` has at least one graded ``pattern: P<k>`` entry."""

    log = cwd / "errors" / "log.md"
    if not log.exists():
        return False
    try:
        text = log.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    return bool(_PATTERN_ENTRY_RX.search(text))


def _mock_was_graded(cwd: Path) -> bool:
    """True if any ``errors/log.md`` entry's ``source:`` points to a mock."""

    log = cwd / "errors" / "log.md"
    if not log.exists():
        return False
    try:
        text = log.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    for match in _SOURCE_RX.finditer(text):
        source = match.group(1).lower()
        if "mock" in source:
            return True
    return False


def detect_phase(cwd: Path, days: int | None) -> str:
    """Derive a workflow phase from the artifacts in ``cwd``.

    The ladder is activity-based. Creating an empty ``patterns.md`` or a
    seeded ``mock/<name>.md`` does not advance the phase — the student must
    have actually graded something. This prevents the display from racing
    ahead of the user's real progress.

    Args:
        cwd: Project root.
        days: Output of :func:`days_until` (``None`` if unknown).

    Returns:
        One of ``setup``, ``diag``, ``drill``, ``mock``, ``cram``, ``cool``.
    """

    if days == 0:
        return "cool"
    cheatsheet = cwd / "cheatsheet"
    if (cheatsheet / "final.pdf").exists() or (cheatsheet / "final.md").exists():
        return "cram"
    if _mock_was_graded(cwd):
        return "mock"
    if not (cwd / "course-index" / "patterns.md").exists():
        return "setup"
    if _has_error_entries(cwd):
        return "drill"
    return "diag"


def top_miss(cwd: Path) -> str | None:
    """Return the most-referenced ``P<k>`` label from weakmap or error log.

    Args:
        cwd: Project root.

    Returns:
        A string like ``P3`` or ``None`` if no signal exists.
    """

    weakmaps = sorted(
        glob.glob(str(cwd / "weakmap" / "weakmap_*.md")),
        reverse=True,
    )
    if weakmaps:
        try:
            text = Path(weakmaps[0]).read_text(encoding="utf-8", errors="replace")
            match = re.search(r"\bP(\d+)\b", text)
            if match:
                return f"P{match.group(1)}"
        except OSError:
            pass
    log = cwd / "errors" / "log.md"
    if log.exists():
        try:
            text = log.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return None
        counts: dict[str, int] = {}
        for match in re.finditer(r"pattern:\s*(P\d+)", text):
            counts[match.group(1)] = counts.get(match.group(1), 0) + 1
        if counts:
            return max(counts, key=counts.get)
    return None


def course_phase(project_root: str | None = None) -> dict:
    """Return the current phase snapshot for ``project_root``.

    Args:
        project_root: Project root path; defaults to ``os.getcwd()`` when
            ``None``.

    Returns:
        A dict with ``phase``, ``days_until_exam``, ``top_miss_pattern``,
        and ``course_name``.
    """

    import os

    root = Path(project_root or os.getcwd()).resolve()
    meta = parse_meta(root)
    days = days_until(meta.get("EXAM_DATE", "")) if meta else None
    phase = detect_phase(root, days)
    return {
        "phase": phase,
        "days_until_exam": days,
        "top_miss_pattern": top_miss(root),
        "course_name": meta.get("COURSE_NAME") if meta else None,
    }


__all__ = [
    "parse_meta",
    "days_until",
    "detect_phase",
    "top_miss",
    "course_phase",
]
