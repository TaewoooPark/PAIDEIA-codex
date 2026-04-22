---
name: paideia-analyze
description: Build the per-course knowledge base — extract recurring patterns from solutions, map HW coverage, and produce summary/patterns/coverage index files that all drill commands read from.
---

# paideia-analyze

Analyze the converted course materials and build `course-index/{summary,patterns,coverage}.md`. Downstream drill skills (`$paideia-twin`, `$paideia-blind`, `$paideia-quiz`, `$paideia-mock`, `$paideia-chain`, `$paideia-pattern`, `$paideia-hwmap`, `$paideia-weakmap`, `$paideia-cheatsheet`) read from these three index files.

## Arguments (free-form)

Optional comma-separated weak-zone hints, e.g. `residues, Laplace transforms`. These get flagged during coverage to help surface user-declared blind spots.

## Prerequisite check

Verify that `converted/` in the CWD contains files. If empty, tell the user to run `$paideia-ingest` first. If `course-index/*.md` already exists, warn "기존 인덱스를 덮어쓸게. 수동 편집한 내용 있으면 백업." and wait for confirmation unless `--force` is passed.

If the ingest inventory is very large, you may call MCP tool `paideia-mcp.build_course_index()` to get a machine-readable file manifest; otherwise scan `converted/` directly.

## Step 1 — `course-index/summary.md`

Parse section headers from `converted/lectures/*.md` in file order. Build a topic tree; cross-reference with `converted/textbook/*.md` (textbooks often use different numbering).

Use the course's own section numbering (§ X.Y, Ch N.M, Lecture N) if present; otherwise auto-number by order of appearance.

Include:

- One-paragraph scope statement inferred from all lecture notes combined
- Topic tree with cross-references to source files under `converted/`
- Difficulty ordering based on lecture progression (early = foundations, late = applications)

## Step 2 — `course-index/patterns.md`

Scan `converted/solutions/*.md` and worked examples in lecture notes. Identify recurring solution moves. **A pattern must appear in ≥2 distinct problems.** One-off techniques go in a final section of `patterns.md`, not as numbered patterns.

Target 15–30 patterns. Too few (<10) → re-scan; too many (>40) → merge similar.

For bulk extraction on large solution sets, you may spawn a subagent per solution file (max_threads=6) and merge their findings. Each subagent returns a list of `{name, recognition, move, appears_in, topic}` records.

Each pattern card:

```markdown
### Pk. <short name>
**Recognition.** <1-2 line trigger signal>
**Move.** <1-3 line operation>
**Appears in.** <problem IDs>
**Topic.** <§ numbers>
```

## Step 3 — `course-index/coverage.md`

Build forward map (problem → §) and reverse map (§ → problems).

Assign exam tier by HW density on the section:

- 🔥🔥 **Exam-primary** — 3+ HW instances. Drill hardest.
- 🔥 **Exam-likely** — 2 HW instances.
- 🟡 **Exam-possible** — 1 HW instance. Warm-pass review.
- ⚪ **Low-risk** — no HW. Reference only.

**Do not invert this.** Sections with zero HW are not "hidden traps" — they are the professor's signal that the topic is off the exam. Mark weak-zone overlaps with an asterisk but do not upgrade the tier on that basis alone.

Close the file with a "Recommended drill priority" section ranking top 6 items by `HW density × (user-declared weakness if matches)`.

## Step 4 — Chat summary

After writing all three files, print:

```
course-index/ 생성 완료.

- summary.md:  <X> sections, <Y> subsections
- patterns.md: <N> recurring patterns (P1..P<N>), <M> one-off techniques
- coverage.md: 🔥🔥 <a> · 🔥 <b> · 🟡 <c> · ⚪ <d>

Top 3 exam-primary sections:
  1. <§X> — <title>  [recommend: $paideia-blind <hw-id>]
  2. <§Y> — <title>  [recommend: $paideia-twin <hw-id>]
  3. <§Z> — <title>  [recommend: $paideia-quiz <§Z> 3]

다음 단계:
  $paideia-hwmap hot        — 🔥🔥 exam-primary 구간 확인
  $paideia-pattern §<weak>  — 약점 영역 패턴 카드 리뷰
  $paideia-blind <hw-id>    — 약점과 가장 가까운 HW 드릴
```

## Conventions

- Explanations in Korean, math as LaTeX (`$...$`, `$$...$$`).
- Every pattern/section cites its source file under `converted/`.
- Pattern IDs stay Latin (`P1`, `P2`, ...).
- See `AGENTS.md` in the course folder for per-course conventions.
