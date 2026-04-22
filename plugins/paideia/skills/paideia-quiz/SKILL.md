---
name: paideia-quiz
description: Generate N practice problems on a topic, section, or the latest weakmap — writes problem MD + hidden answer MD sibling. User solves on paper and runs $paideia-grade.
---

# paideia-quiz

Generate N practice problems weighted by HW density (for broad queries) or by the user's latest weakness report (for `weakmap` mode).

## Arguments

- First token: topic name, `§<n>`, `all`, or the literal `weakmap`.
- Second token (optional): number of problems, default 5.

## Prerequisites

Read `course-index/summary.md`, `course-index/patterns.md`, `course-index/coverage.md`. If `course-index/` is empty, tell the user to run `$paideia-analyze` first — problems generated without the index will be unfocused.

## Procedure

### 0. Weakmap mode (first arg = `weakmap`)

- Find the latest `weakmap/weakmap_*.md` (by mtime). If none, tell the user to run `$paideia-weakmap` first and abort.
- Parse its "Top 5 weaknesses" and "User-declared weaknesses" sections to collect a target set of (§, Pk) pairs.
- Design the N-problem mix so every top weakness is covered at least once; user-declared items take priority. Spread remaining slots over top-ranked error patterns.
- Filename override: save to `quizzes/weakmap_<ts>.md` (+ `_answers.md`). Cite which weakness entry each problem targets in the footer.
- Skip step 1. Continue from step 2 with this weakness-driven mix.

### 1. Resolve topic

Map the argument to a specific set of sections and patterns via `coverage.md` and `patterns.md`. If ambiguous, ask the user to pick.

- **Special case `all`** (broad diagnostic): weight section selection by HW density — ~70% 🔥🔥, ~25% 🔥, ≤5% 🟡, 0% ⚪. Never sample ⚪ unless the user explicitly names one — the professor's HW signals what's off the exam.
- **Specific § or topic:** if the user names a ⚪ low-risk section, comply but warn once: "HW에 없는 §라 출제 확률은 낮아. 그래도 돌릴까?"

### 2. Design the problem mix (N problems)

- 1 warmup (definition recall, fastest pattern application)
- N-3 standard (single-pattern derivation or computation) — prefer patterns recurring across multiple HW problems in the target sections
- 1 applied (pattern used in a specific system / numerical case)
- 1 conceptual trap (tests a common student error — sign, wrong variable held fixed, wrong pattern chosen)

### 3. Save

- Problems → `quizzes/<topic>_<ts>.md`
- Answers → `quizzes/<topic>_<ts>_answers.md` (do not display).
- Each problem cites the § and pattern being tested **at the end** of the problem (not in the title — no spoilers).

### 4. Print to chat

- Filename of the quiz.
- All N problem statements, numbered.
- Closing: "종이로 풀고, 스캔해서 `answers/<topic>_<ts>.pdf`에 올린 뒤 `$paideia-grade`"

### 5. Do NOT accept typed answers

If the user starts typing an answer in chat, redirect them to the PDF-upload workflow.

## Problem format

```markdown
## P<n>  (<points if applicable>)

<problem statement, including any figures referenced>

<blank line for working>

---
*(문제 설정: §<section>, 테스트 패턴: P<k>)*  ← at very bottom, small
```

## Conventions

- Korean prose, LaTeX math (`$...$`, `$$...$$`).
- Keep chat output ≤ 40 lines.
