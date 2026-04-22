"""``build_course_index`` MCP tool.

Intentionally low-value for v1: the actual pattern/coverage extraction happens
in the ``paideia-analyze`` skill, which reasons over markdown (possibly via
subagent fan-out). This tool just validates ``converted/`` exists, enumerates
what's there, and passes ``weak_zones`` through to the skill for context.
"""

from __future__ import annotations

import os
from pathlib import Path

_CATEGORIES = ("lectures", "textbook", "homework", "solutions")


def _list_category(converted: Path, category: str) -> list[str]:
    """Return sorted relative paths for every ``.md`` in a category dir."""

    cat_dir = converted / category
    if not cat_dir.exists():
        return []
    return sorted(
        str(p.relative_to(converted))
        for p in cat_dir.rglob("*.md")
    )


def build_course_index(
    weak_zones: str | None = None,
    project_root: str | None = None,
) -> dict:
    """Return an inventory of ``converted/`` for the analyze skill to reason over.

    Args:
        weak_zones: Free-form user hints passed through to the skill.
        project_root: Project root; defaults to ``os.getcwd()``.

    Returns:
        ``{project_root, converted_root, inventory, totals, weak_zones,
        ready}``. ``ready`` is False if ``converted/`` is missing or empty —
        the skill should direct the user to ``$paideia-ingest`` first.
    """

    root = Path(project_root or os.getcwd()).resolve()
    converted = root / "converted"
    if not converted.exists():
        return {
            "project_root": str(root),
            "converted_root": str(converted),
            "inventory": {cat: [] for cat in _CATEGORIES},
            "totals": {cat: 0 for cat in _CATEGORIES},
            "weak_zones": weak_zones,
            "ready": False,
            "message": (
                "converted/ is missing. Run ingest_pdfs (or the "
                "paideia-ingest skill) first."
            ),
        }

    inventory = {cat: _list_category(converted, cat) for cat in _CATEGORIES}
    totals = {cat: len(files) for cat, files in inventory.items()}
    ready = any(totals.values())
    return {
        "project_root": str(root),
        "converted_root": str(converted),
        "inventory": inventory,
        "totals": totals,
        "weak_zones": weak_zones,
        "ready": ready,
    }


__all__ = ["build_course_index"]
