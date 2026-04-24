---
name: paideia-blind
description: Strategy-check drill on a known HW or example problem — user describes approach in 3-5 lines of Korean prose, then verify against the reference solution without revealing it first.
---

# paideia-blind

Strategy-level drill on a known problem. The user does not re-solve — they describe the approach in prose. Pattern recognition is the exam bottleneck; if the user can articulate the correct strategy in 30 seconds, they will execute it in 10 minutes on the exam.

## Arguments

`<problem-id>` — e.g. `hw4-p3`, `example-5.2`. Required.

## Prerequisites

Read `course-index/patterns.md`. If absent, tell the user to run `$paideia-analyze` first.

## Procedure

1. **Load problem statement ONLY** from `converted/homework/<n>.md` or `converted/textbook/<ch>.md` (for textbook examples). Do NOT open the solution yet.

2. **Present the problem verbatim** to the user.

3. **Request strategy** (3-5 lines Korean, no math typing):

   ```
   전략만 말해줘 — 수식은 쓸 필요 없음.
   1) 어느 pattern 쓸 건지 (course-index/patterns.md 의 Pk 번호)
   2) 어떤 변수 고정, 어떤 변수로 전개할지
   3) 최종 답이 어떤 형태일 거라 예상하는지
   ```

4. **Wait for response.** Do NOT proceed until the user answers.

5. **Load solution** from `converted/solutions/<n>.md` (or `converted/textbook/...` for example). Compare 3 axes:

   a. **Pattern identification** — correct Pk(s)?
   b. **Variable choice** — correct hold-fixed set?
   c. **End-form prediction** — matches actual answer structure?

6. **Feedback protocol:**
   - ✅ all three → confirm, then copy the relevant part of the solution into `derivations/blind-<id>.md` for permanent reference.
   - ❌ on any axis → point out specifically which axis failed, **without** revealing the correct answer. Ask for revision.
   - After 2 failed attempts on the same axis → give a one-line hint referencing the relevant pattern name.

7. **Log errors** if the user needed revision. Use the **canonical schema from `paideia-grade` §6** — same keys `$paideia-grade` writes, so `$paideia-weakmap`, `$paideia-phase`, and `paideia-mcp.course_phase` see `/blind` errors too. Append to `errors/log.md`:

   ```yaml
   - problem_id: <id>
     pattern:    <Pk>
     error_type: pattern-missed | wrong-variable | wrong-end-form
     summary:    "<1 line>"
     source:     blind/<id>
     date:       <ISO>
   ```

   Map the strategy axis to `error_type`: pattern axis → `pattern-missed`, variable axis → `wrong-variable`, end-form axis → `wrong-end-form`. The `source:` field lets `phase.py::_mock_was_graded` and downstream consumers distinguish entries from `/grade` (answers/converted/…) vs `/blind` (blind/…) vs `/mock` (any source containing `mock`).

8. **Close:**
   "같은 유형 retention 확인하려면 `$paideia-twin <id>`로 변형 하나 풀어봐."

## Why strategy-based, not full derivation

The strategy check IS the drill. Execution is practiced via paper + `$paideia-grade`. Typing math in the chat is slow and error-prone; pattern recognition is the actual bottleneck.

## Conventions

- Korean prose, LaTeX math (`$...$`, `$$...$$`).
- Pattern IDs stay Latin (`P1`, `P2`, ...).
- Keep output ≤ 40 lines.
