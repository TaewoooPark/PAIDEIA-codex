---
name: paideia-derive
description: Write a clean reference derivation of a target equation or theorem to derivations/<slug>.md — pulls from the course's own materials rather than testing the user.
---

# paideia-derive

Pure reference-writer. The user explicitly asks for a derivation because they want to read, not type. Do NOT quiz the user; do NOT prompt for strategy. Just write.

## Arguments

`<target>` — name of the equation or theorem to derive. Free-form text. Gets slugified (lowercase-hyphenated) for the filename.

## Prerequisites

Read `course-index/summary.md` to resolve the target. Scan `converted/textbook/*.md` and `converted/lectures/*.md` for existing treatment.

## Procedure

1. **Locate the derivation** in `converted/textbook/*.md` and `converted/lectures/*.md`. If present in both, prefer the textbook (usually cleaner).
2. **If not in materials**, derive it from first principles using standard techniques for the course's domain. Cite which earlier results you're using.
3. **Format as a clean reference markdown file** with:
   - Starting definitions / assumptions clearly stated
   - Each step with a one-line explanation of why
   - Boxed final result
   - Short "물리적/수학적 해석" at the end
   - Typical pitfalls (common student errors) listed at bottom
4. **Save to** `derivations/<slug>.md`.
5. **Print:** "`derivations/<slug>.md` 저장. 열어서 읽어보고, 이해 안 되는 step 있으면 질문해."

## Format template

```markdown
# <Target name>

**목표.** <statement of what we want to derive>

**출발점.** <definition / law / axiom / earlier result>

---

### 1단계 — <step description>

$$<step equation>$$

<why this step>

### 2단계 — ...

...

---

**결과.**
$$\boxed{\;<final>\;}$$

**해석.** <1-2 sentences on what this means physically/mathematically>

**주의할 pitfall.**
- <common error 1>
- <common error 2>

**참조.** <source section in converted/>
```

## Conventions

- Korean prose, LaTeX math (`$...$`, `$$...$$`).
- No emojis except optional final $\blacksquare$ or ∎ at the result.
- Align with any existing `derivations/` file style in the course folder.
