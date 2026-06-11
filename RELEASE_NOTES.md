# Release Notes

## 2026-06-11 — Live UX hardening pass

This release batch was driven by a real end-to-end PAIDEIA Codex run in a fresh desktop demo course: install, course bootstrap, ingest, analyze, phase, hwmap, pattern lookup, quiz generation, and weakmap generation. Each note below maps to one commit in this batch.

### `6cf852b` — `test: align phase tests with graded activity`

- Updated phase regression tests to match PAIDEIA's documented activity-based phase model.
- A course now moves past `diag` only after a real graded error entry exists, not merely because a quiz or mock file exists.
- User impact: tests now protect the intended workflow signal instead of encouraging file-existence shortcuts.

### `a479ef5` — `docs: update Codex plugin install commands`

- Replaced stale `/plugins ...` install examples with the current Codex CLI commands:
  - `codex plugin marketplace add https://github.com/OPTIMETA/PAIDEIA-codex.git`
  - `codex plugin add paideia@paideia-marketplace`
- Fixed the Korean README's stale "15 verbs" wording to the current 16-verb plugin surface.
- User impact: first-time terminal installs now follow commands that work on current `codex-cli`.

### `ddd6a2a` — `fix: infer sections from OCR plaintext headings`

- Improved `paideia-mcp.build_course_index()` so OCR/plain-text lines like `Lecture 1: ...`, `Section 1.1 ...`, and `Chapter 1 ...` become real course sections.
- Avoided promoting generated file-stem headings like `# lecture_residues` into ugly section names.
- Stopped solution/homework filenames from becoming primary topic sections when lecture/textbook headings are available.
- User impact: `summary.md` and `coverage.md` now produce readable topic trees after low-fidelity OCR.

### `b29b508` — `fix: ignore seeded schema comments in phase detection`

- Fixed phase detection so the seeded schema example inside `errors/log.md` is ignored.
- Prevented the example `source: ... mock/<ts>.md` comment from falsely advancing a fresh course to `mock`.
- Also prevents `top_miss` from counting placeholder `pattern: Pk` entries in comments.
- User impact: a newly initialized/analyzed course correctly reports `diag` until the student actually grades work.

### `b245224` — `fix: handle empty hot hwmap results`

- Updated `$paideia-hwmap hot` guidance for courses with no 🔥🔥 / 🔥 sections yet.
- The skill now falls back to the highest-ranked 🟡 section and avoids asking the user to choose from nonexistent hot zones.
- User impact: sparse or early demo courses now get a sensible next step instead of a confusing prompt.

### `8b825c6` — `fix: prevent quiz answer transcript leaks`

- Added quiz-skill guidance that `_answers.md` files must not be created through visible patch/diff/output paths.
- Instructed agents to verify hidden answer files only by filename, size, or line count.
- User impact: generated quiz answers are much less likely to be accidentally exposed while the student is still solving.

### `085e667` — `fix: block visible quiz answer writes`

- Tightened the hidden-answer rule further: the answer body must not appear in visible tool input either, including here-doc or inline script bodies.
- If no non-echoing write path is available, the skill must create only the problem file and stop rather than leaking answers.
- User impact: hidden quiz answers stay hidden even from terminal transcripts, not just final chat output.

### `558bb02` — `fix: avoid verbose report diffs`

- Added write-output discipline for `$paideia-weakmap` and `$paideia-cheatsheet`.
- Long generated reports should be saved quietly and verified with path/count summaries rather than full visible diffs.
- User impact: weakmap and cheatsheet runs stay readable in chat while preserving the full artifacts on disk.

## Verification

- `python3 -m pytest -q` from `plugins/paideia/paideia-mcp`
- Result: `26 passed`
