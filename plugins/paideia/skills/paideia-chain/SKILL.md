---
name: paideia-chain
description: Generate an exam-style integration problem that chains N patterns from different parts of the course — tests pattern decomposition and sequencing that single-pattern drills miss.
---

# paideia-chain

Multi-pattern integration problem. Real exam problems rarely test one pattern in isolation. Chaining tests two skills that `$paideia-quiz`, `$paideia-twin`, `$paideia-blind` cannot:

1. **Pattern decomposition** — breaking a complex problem into pattern-sized pieces.
2. **Pattern sequencing** — recognizing that pattern A's output is pattern B's input.

## Arguments

`<N>` — number of patterns to chain. Default 2, max 4.

## Prerequisites

Read `course-index/patterns.md` and `course-index/coverage.md`. If absent, tell the user to run `$paideia-analyze` first.

## Procedure

1. **Select N patterns** with constraints:
   - From ≥ N different source problems (span HW/example origins; don't pick 2 patterns both from HW1).
   - At least one pattern from the user's weak zone (per `coverage.md` weak-declaration marker or latest `weakmap/`).
   - At least one pattern marked ✅✅ / 🔥🔥 (user has machinery).
   - Patterns must be composable (pattern A's output = pattern B's input).
   - Draw patterns from 🔥🔥 / 🔥 sections. Avoid patterns pulled from ⚪ low-risk sections unless the user explicitly asks.

2. **Design the problem** as a multi-part question:
   - Part (a): establishes context, requires pattern 1.
   - Part (b): uses result from (a), requires pattern 2.
   - Part (c): ties together, requires pattern 3 (if N=3).
   - Final answer should synthesize.

3. **Save:**
   - Problem → `chain/exam_<ts>.md`
   - Solution → `chain/exam_<ts>_sol.md` (hidden)

4. **Print:**
   - Full problem
   - Estimated time (N × 6 min + 5 min setup)
   - Do NOT reveal which patterns are used.
   - Closing: "종이로 풀고 `answers/chain_<ts>.pdf`에 올린 뒤 `$paideia-grade`. 풀이 끝에 '어느 pattern 썼는지'도 답에 적어줘 — 인식 드릴의 핵심."

5. **When user submits:**
   - `$paideia-grade` converts PDF → MD → checks:
     - Did they identify all N patterns?
     - Did they use them in the correct order?
     - Does the final synthesis match?
   - Log pattern-identification errors to `errors/log.md` with field `chain_problem`.

## Conventions

- Korean prose, LaTeX math (`$...$`, `$$...$$`).
- Keep chat output ≤ 40 lines.
- See `AGENTS.md` for per-course conventions.
