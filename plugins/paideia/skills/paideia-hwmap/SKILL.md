---
name: paideia-hwmap
description: Surface HW-density exam tiers from course-index/coverage.md — HW coverage = exam probability, so this ranks the 🔥🔥 / 🔥 zones where the exam points actually live.
---

# paideia-hwmap

Pure text op over `course-index/coverage.md`. HW coverage is an exam-probability signal, not a completeness metric: sections the professor drilled into HW are where the exam points live. "No HW coverage" is **not** a red flag — it's a low-risk zone the professor chose to omit.

## Arguments

- `hot` (or `primary`, `exam`, `risk`, `blind` for backward compat) — list 🔥🔥 Exam-primary + 🔥 Exam-likely sections ranked by HW density
- `all` (or empty) — full exam-tier distribution table
- `§<n>` or section name — focused view on that section and neighbors (§±1)

## Prerequisites

Read `course-index/coverage.md`. If missing, tell the user to run `$paideia-analyze` first.

You may call MCP tool `paideia-mcp.course_phase()` to include the current phase in the header (e.g. if the user is in `drill` phase, bias the closing recommendation toward `$paideia-blind` / `$paideia-twin`).

## Procedure

### If query is a § number or section name

Show problems covering that section plus adjacent sections (§±1) for context. List the patterns involved. State the exam tier (🔥🔥 / 🔥 / 🟡 / ⚪) and the drill recommendation that follows.

### If query is `hot`

Return 🔥🔥 Exam-primary and 🔥 Exam-likely sections, ranked by HW density (highest first). For each:
- List the HW problems that target it (these are your drill anchors).
- One-line drill recommendation:
  - Many HW, pattern fluent → `$paideia-twin <hw-id>` (build surface variance)
  - Many HW, strategy shaky → `$paideia-blind <hw-id>` (strategy-check on the real HW)
  - User has solved HW but forgets the pattern → `$paideia-pattern <Pk>` then `$paideia-quiz §<n> 3`

Do **not** recommend `$paideia-derive` as a default — derivations are for reading gaps, not for drilling exam-likely zones.

### If query is `all` or empty

Render an exam-tier distribution table:

| Exam tier | Count | Sections |
|---|---|---|
| 🔥🔥 Exam-primary (3+ HW) | n | list |
| 🔥 Exam-likely (2 HW) | n | list |
| 🟡 Exam-possible (1 HW) | n | list |
| ⚪ Low-risk (no HW) | n | list |

Plus the "Recommended drill priority" section from `coverage.md` (ordered by HW density, not by absence).

### Low-risk section handling

If the user insists on drilling a ⚪ section, warn once:
"HW에 한 번도 안 나온 구간은 시험 출제 확률이 낮아. 시간 없으면 🔥🔥부터." Then comply.

## Closing line

Always end with:
"🔥🔥 중에서 지금 당장 드릴 걸 1개만 고른다면? 시간 몇 분 남았어?"

Output goal: exam-point maximization. Steer time toward HW-dense zones.

## Conventions

- Korean prose. Keep output ≤ 40 lines.
