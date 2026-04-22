---
name: paideia-phase
description: Show the artifact-derived course phase snapshot from paideia-mcp.course_phase() — setup/diag/drill/mock/cram/cool, plus D-day and top-miss pattern.
---

# paideia-phase

Thin wrapper over `paideia-mcp.course_phase()`. Use it when the user wants a fast read of where the course folder currently sits in the PAIDEIA cycle.

## Procedure

1. Call MCP tool `paideia-mcp.course_phase()`.
2. Print a compact snapshot:

   ```
   phase: <phase>
   exam:  D-<days>   # or `date unknown`
   miss:  <Pk or none>
   ```

3. Add exactly one closing recommendation keyed by the phase:
   - `setup` → `$paideia-ingest` then `$paideia-analyze`
   - `diag` → `$paideia-quiz all 5`
   - `drill` → `$paideia-blind <hw-id>` or `$paideia-twin <hw-id>`
   - `mock` → `$paideia-grade answers/mock_<ts>.pdf`
   - `cram` → `$paideia-cheatsheet --pdf`
   - `cool` → keep the folder archived; no further drill recommendation

## Output discipline

- Keep output ≤ 6 lines.
- Do not explain the whole pipeline unless the user asks.
- Korean prose, but keep phase tokens in Latin (`setup`, `diag`, `drill`, `mock`, `cram`, `cool`).
