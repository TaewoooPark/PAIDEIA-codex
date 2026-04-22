---
name: paideia-twin
description: Generate a twin variant of a known HW or example problem — same pattern, new surface. User solves on paper and runs $paideia-grade, or describes the strategy in prose.
---

# paideia-twin

A **twin** preserves the solution technique while varying surface features. Changing $x \to y$ alone is a re-skin, not a twin. See `references/twin-recipe.md` for full invariance rules.

## Arguments

`<problem-id>` — e.g. `hw4-p3`, `example-5.2`.

## Prerequisites

Read `course-index/patterns.md` and `references/twin-recipe.md` (under this skill). If `course-index/` is empty, tell the user to run `$paideia-analyze` first.

## Procedure

1. **Locate original.** Search `converted/homework/` and `converted/solutions/` for the problem-id. If not found, check `converted/lectures/*.md` and `converted/textbook/*.md` for worked examples.

2. **Identify pattern(s) used.** Cross-reference with `course-index/patterns.md`.

3. **Apply `references/twin-recipe.md` rules.** Hold pattern, topic, and step count invariant. Vary system, numbers, names, direction of the ask.

4. **Save two files:**
   - Problem → `twins/<id>_<ts>.md`
   - Solution → `twins/<id>_<ts>_sol.md` (hidden)

5. **Print to chat:**
   - The twin problem statement (do **NOT** reference the original problem ID in the output).
   - Instruction: "종이로 풀고 `answers/twin_<id>_<ts>.pdf`에 올린 뒤 `$paideia-grade`. 또는 전략만 3-5줄로 말해도 됨."

6. **If user responds with strategy text** (not PDF):
   - Match 3 axes: pattern / variable-choice / end-form.
   - If all ✅: confirm; optionally copy the `_sol.md` content into `derivations/twin-<id>.md`.
   - If any ❌: flag specifically, ask for revision.

7. **Quality check before presenting:**
   - ✅ Pattern genuinely required (no shortcut).
   - ✅ Answer differs from original (literal or symbolic).
   - ✅ Origin problem ID not leaked anywhere in the prompt.
   - ✅ Well-posed; final answer exists.
   - ✅ If the original had part (a), (b), (c) scaffolding, twin preserves it.

## Conventions

- Korean prose, LaTeX math (`$...$`, `$$...$$`).
- Keep chat output ≤ 40 lines.
- See `references/twin-recipe.md` for invariance rules and worked twin / re-skin examples.
