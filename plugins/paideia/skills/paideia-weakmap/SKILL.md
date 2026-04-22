---
name: paideia-weakmap
description: Produce a priority-ranked weakness report in weakmap/weakmap_<ts>.md. No arg = fresh snapshot from the latest error per pattern; with concept arg = patch the latest report by accumulating that concept.
---

# paideia-weakmap

The user says "나 이 포인트 약한 것 같아" and can immediately patch the weakmap with `$paideia-weakmap <개념>`. No arg = fresh snapshot from `errors/log.md`.

## Storage rules

- Directory: `weakmap/`
- Filename: `weakmap/weakmap_<YYYY-MM-DD_HHmm>.md`
- Top-of-file title: `# Weakmap — <YYYY-MM-DD HH:mm>`
- **Never overwrite.** Always save a new timestamped file (append-only history).
- "Latest report" = file with the most recent mtime under `weakmap/`.

## Prerequisites

Read `errors/log.md`, `course-index/coverage.md`, `course-index/patterns.md`, `course-index/summary.md`.

Optional: call MCP tool `paideia-mcp.course_phase()` to embed the current phase (`setup / diag / drill / mock / cram / cool`) in the report header.

## Branches

### Case A — no argument (fresh snapshot)

1. Read `errors/log.md`. Group YAML entries by `pattern`.
2. **Per pattern, keep only the entry with the latest `date`.** (Older errors may already be corrected; the current weakness is the freshest miss per pattern.)
3. Cross-reference with `course-index/coverage.md` for context.
4. If a prior weakmap exists, **do NOT carry over** its "User-declared weaknesses" — fresh snapshot leaves that section empty in this mode.
5. Save in the format below; print a compact summary to chat.

### Case B — with argument (concept patch)

Flow: read latest report → append new concept to user-declared list → rewrite the full report from both error log + accumulated user-declared items → save as a new timestamp.

1. Read the latest `weakmap_*.md`. If none, treat as empty and start from Case A.
2. Extract the existing "User-declared weaknesses" list → `[A, B, ...]`.
3. Treat the entire argument string as new concept `C`. Dedupe. Final list `[A, B, C]`.
4. Map each concept to `course-index/patterns.md` + `summary.md` → identify related §, Pk, recommended drill.
5. Run the Case A steps 1-3 as well, so the new report reflects both the current error log **and** the user-declared concepts.
6. Save to a new `weakmap/weakmap_<ts>.md`.

## Report format

```markdown
# Weakmap — <YYYY-MM-DD HH:mm>

## Error histogram (latest per pattern)

| Pattern/topic | Latest error type | Date | § |
|---|---|---|---|
...one row per pattern, sorted by recency.

## Top 5 weaknesses (priority ranked)

1. **<pattern or topic>** — <one-line summary>
   → 추천: `$<skill> <target>`

(Recommendation rules by `error_type`:)
- `pattern-missed` / `wrong-variable` → `$paideia-blind <problem>` or `$paideia-derive <concept>`
- `algebraic` / `sign` → `$paideia-quiz <topic> 3`
- `definition` → re-read the relevant § in `converted/lectures/` for 5 min
- `wrong-end-form` → `$paideia-pattern <Pk>` recognition drill

## User-declared weaknesses

(Populated only in Case B. Empty in Case A.)

- **<concept A>** — related §<x>, P<k>. 추천: `$<skill>`
- **<concept B>** — ...
- **<concept C (newly added)>** — ...

## Exam-hot zones not yet drilled

Sections marked 🔥🔥 / 🔥 in `coverage.md` that have no entries in `errors/log.md`:
- §X, §Y

→ 에러 로그에 안 찍혔다는 건 (a) 잘하거나 (b) 아직 안 풀어본 것. `$paideia-blind <hw-id>`로 빠르게 확인.

(⚪ Low-risk sections are excluded. HW-absence signals low exam probability, so weakmap de-prioritizes them too.)

## One-line verdict

<the single drill to run right now>
```

## Chat output discipline

- One line with the saved file path.
- Do **not** paste the full report — summarize only **Top 5 + one-line verdict** (≤ 30 lines).
- End with: "추가 약점이 생기면 `$paideia-weakmap <개념>`으로 패치, `$paideia-quiz weakmap`으로 이 보고서 기반 문제 생성."
