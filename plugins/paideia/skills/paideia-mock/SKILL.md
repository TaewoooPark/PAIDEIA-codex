---
name: paideia-mock
description: Generate a full mock exam at requested length, HW-density weighted across the course. Writes problem MD + hidden solution MD; user solves on paper, uploads PDF, runs $paideia-grade.
---

# paideia-mock

Full mock exam inferred from `course-index/`. Problems are drawn **in proportion to HW density** of each section — HW density = exam probability.

## Arguments

- First token: `<minutes>` (default 90)
- Optional: `emphasize=§X,§Y` — bias problems toward specific sections (overrides HW weighting only when user explicitly requests it)

## Prerequisites

Read `course-index/summary.md`, `course-index/patterns.md`, `course-index/coverage.md`. If any is missing, tell the user to run `$paideia-analyze` first.

## Procedure

### 1. Infer exam structure from `coverage.md` and past HW

- Typical mid/final: 4-6 problems over 90-120 minutes.
- **HW-weighted mix.** Problems are drawn in proportion to HW density. Target distribution:
  - ≥70% of points from 🔥🔥 Exam-primary sections (3+ HW)
  - ~25% from 🔥 Exam-likely (2 HW)
  - ≤5% from 🟡 Exam-possible (1 HW)
  - **0%** from ⚪ Low-risk — do not invent problems in sections the professor never tested.
- If user passed `emphasize=§X,§Y`, bias toward those.
- Difficulty distribution: 1 warmup / N-2 standard / 1 hard (multi-pattern).

### 2. Design the exam

- For each problem, pick: target §, target pattern(s), point value, estimated time.
- Ensure patterns from ≥3 different parts of the course appear (tests integration).
- Last problem should require chaining ≥2 patterns.

### 3. Save

- Problems → `mock/exam_<ts>.md`
- Solutions → `mock/exam_<ts>_sol.md` (do not display).

### 4. Print to chat

- The full exam (problem statements with point values and time suggestions).
- Total points summing to 100 (or inferred weighting).
- Closing line: "타이머 <minutes>분. 종이로 풀고 `answers/mock_<ts>.pdf`에 올린 뒤 `$paideia-grade`."

### 5. Do NOT reveal which patterns are being tested

The user should identify patterns during solving. Pattern recognition is half the exam skill.

## Exam format

```markdown
# Mock Exam — <date>

**Duration**: <minutes> min  **Total**: 100 pts

---

## P1 (<pts>, ~<min> min)

<problem>

## P2 (<pts>, ~<min> min)

<problem>

...
```

The `_sol.md` sibling has the full reference solution + pattern labels + typical point distribution. Only opens via `$paideia-grade`.

## Conventions

- Korean prose, LaTeX math (`$...$`, `$$...$$`).
- Problems stay neutral — no pattern spoilers in the problem text.
