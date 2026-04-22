---
name: paideia-pattern
description: Show solution pattern cards from course-index/patterns.md filtered by §, Pk, or keyword — compact recognition tool, not a tutorial.
---

# paideia-pattern

Read-only filter over `course-index/patterns.md`. Surfaces pattern recognition cards so the user can scan them before a drill.

## Arguments

`<query>` — one of:
- `§<n>` or `Ch<n>` — patterns whose Topic field includes that section
- `P<k>` (e.g. `P7`) — single pattern plus cross-references
- keyword (e.g. `residue`, `fourier`, `induction`) — match name / recognition / move text, case-insensitive
- `all` or empty — full list, grouped by topic

## Prerequisites

Read `course-index/patterns.md`. If missing, tell the user to run `$paideia-analyze` first.

## Procedure

1. **Filter** patterns per the argument.

2. **Render each matching pattern as a compact card:**

   ```
   [Pk] <name>
   Recognition: <signal>
   Move: <operation, 1-2 lines>
   Seen in: <problem IDs>
   Topic: <§ numbers>
   ```

3. **Close with a prompt:**
   "처음 보면 바로 알아채기 어려울 것 같은 pattern 있어? 번호 말해 — 그것만 `$paideia-blind <problem>`으로 드릴."

## Output discipline

- Total output ≤ 40 lines.
- This is a recognition tool, not a tutorial. If the user wants depth on one pattern, they will ask.
- Korean prose; pattern IDs stay Latin (`P1`, `P2`, ...).
