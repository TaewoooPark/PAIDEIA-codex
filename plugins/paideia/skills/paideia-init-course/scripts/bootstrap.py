#!/usr/bin/env python3
"""Scaffold a PAIDEIA course folder in the current working directory.

Called by the `$paideia-init-course` skill after the user has answered the
metadata prompts. Creates the directory skeleton, writes `.course-meta`, writes
`AGENTS.md` from the template, seeds `errors/log.md`, and runs `git init`.

Idempotent: existing files are never overwritten; directories are `mkdir -p`'d.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


DIRS = [
    "materials/lectures",
    "materials/textbook",
    "materials/homework",
    "materials/solutions",
    "converted/lectures",
    "converted/textbook",
    "converted/homework",
    "converted/solutions",
    "course-index",
    "quizzes",
    "mock",
    "twins",
    "chain",
    "derivations",
    "cheatsheet",
    "weakmap",
    "answers/converted",
    "errors",
]


ERRORS_LOG_SEED = """# Error log

<!-- Append-only YAML entries. Schema:
- problem_id: <id>
  pattern:    <Pk>
  error_type: pattern-missed | wrong-variable | wrong-end-form | algebraic | sign | definition
  summary:    "<1 line>"
  date:       <ISO8601>
-->
"""


GITIGNORE = """.codex/cache/
answers/*.pdf
answers/converted/*.md
answers/converted/.tmp-*/
errors/log.md
quizzes/*_answers.md
mock/*_sol.md
twins/*_sol.md
chain/*_sol.md
cheatsheet/final.pdf
.DS_Store
*.pyc
__pycache__/
"""


VALID_ENGINES = {"openai-vision", "qwen3-vl", "tesseract"}


def _log(tag: str, path: Path) -> None:
    print(f"{tag}: {path}")


def make_dirs(root: Path) -> None:
    for d in DIRS:
        (root / d).mkdir(parents=True, exist_ok=True)
    _log("dirs", root)


def seed_file(path: Path, content: str) -> None:
    if path.exists():
        _log("skip", path)
        return
    path.write_text(content, encoding="utf-8")
    _log("write", path)


def write_course_meta(root: Path, args: argparse.Namespace) -> None:
    body = (
        f"COURSE_NAME: {args.course_name}\n"
        f"EXAM_DATE: {args.exam_date}\n"
        f"EXAM_TYPE: {args.exam_type}\n"
        f"USER_WEAK_ZONES: {args.weak_zones}\n"
        f"OCR_ENGINE: {args.ocr_engine}\n"
    )
    path = root / ".course-meta"
    path.write_text(body, encoding="utf-8")
    _log("write", path)


def write_agents_md(root: Path, args: argparse.Namespace, template: Path) -> None:
    target = root / "AGENTS.md"
    if target.exists():
        _log("skip", target)
        return
    if not template.exists():
        print(f"error: template missing at {template}", file=sys.stderr)
        sys.exit(2)
    body = template.read_text(encoding="utf-8")
    body = (
        body.replace("$COURSE_NAME", args.course_name)
        .replace("$EXAM_DATE", args.exam_date)
        .replace("$EXAM_TYPE", args.exam_type)
        .replace("$WEAK_ZONES", args.weak_zones)
        .replace("$OCR_ENGINE", args.ocr_engine)
    )
    target.write_text(body, encoding="utf-8")
    _log("write", target)


def git_init(root: Path) -> None:
    if (root / ".git").exists():
        _log("skip", root / ".git")
        return
    if shutil.which("git") is None:
        print("skip: git not on PATH — leaving uninitialized", file=sys.stderr)
        return
    subprocess.run(["git", "init", "-q"], cwd=root, check=False)
    seed_file(root / ".gitignore", GITIGNORE)
    _log("init", root / ".git")


def resolve_template(override: str | None) -> Path:
    if override:
        return Path(override).expanduser().resolve()
    here = Path(__file__).resolve().parent
    return here.parent / "assets" / "AGENTS.md.template"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Scaffold a PAIDEIA course folder.")
    p.add_argument("--course-name", required=True)
    p.add_argument("--exam-date", required=True)
    p.add_argument("--exam-type", required=True)
    p.add_argument("--weak-zones", default="unknown")
    p.add_argument("--ocr-engine", default="openai-vision")
    p.add_argument("--template", default=None, help="Override AGENTS.md.template path.")
    p.add_argument(
        "--root",
        default=None,
        help="Target directory (default: $PWD).",
    )
    args = p.parse_args()
    if args.ocr_engine not in VALID_ENGINES:
        print(
            f"error: --ocr-engine must be one of {sorted(VALID_ENGINES)}, "
            f"got {args.ocr_engine!r}",
            file=sys.stderr,
        )
        sys.exit(2)
    return args


def main() -> None:
    args = parse_args()
    root = Path(args.root).expanduser().resolve() if args.root else Path.cwd()
    root.mkdir(parents=True, exist_ok=True)

    make_dirs(root)
    seed_file(root / "errors" / "log.md", ERRORS_LOG_SEED)
    write_course_meta(root, args)
    write_agents_md(root, args, resolve_template(args.template))
    git_init(root)

    print(f"\nok: {args.course_name} @ {root} (engine={args.ocr_engine})")


if __name__ == "__main__":
    main()
