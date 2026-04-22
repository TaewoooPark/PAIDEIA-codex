---
name: paideia-cheatsheet
description: Compile an error-driven one-page exam cheatsheet from course-index and errors/log.md. Optionally render to PDF via reportlab — tuned by the user's actual mistakes, not the syllabus.
---

# paideia-cheatsheet

The cheatsheet is disproportionately valuable because it is generated from `errors/log.md` — whatever the user actually got wrong — not from the syllabus. Pattern frequency × user's own error types = what to memorize.

## Arguments

- `--pdf` — also render `cheatsheet/final.pdf` (2-column, 9pt, dense).

## Prerequisites

Read `course-index/patterns.md`, `course-index/coverage.md`, `course-index/summary.md`, and `errors/log.md`. If any is missing, tell the user to run `$paideia-analyze` (and `$paideia-grade` at least once for `errors/log.md`).

You may call MCP tool `paideia-mcp.course_phase()` to surface the current phase (`setup / diag / drill / mock / cram / cool`) in the header — useful if the cheatsheet is being compiled mid-study versus night-before.

## Procedure

1. **Collect highest-value items:**
   - Top 5 patterns by frequency of appearance (from `patterns.md`).
   - All formulas boxed in `derivations/*.md` (final results only).
   - User's most-frequent error types (from `errors/log.md`) — with the **correction**, not the error.
   - 🔴 blind-spot sections with one key formula each.

2. **Structure the cheatsheet** (target: fits on 1 page @ 10pt):

   ```markdown
   # <Course name> — Cheatsheet

   _Generated <date>. For exam reference only._

   ## Core formulas
   <table or compact list of boxed results from derivations/>

   ## Pattern quick-ref
   | Pk | Recognition | Move |
   |---|---|---|
   ...top 8 patterns only

   ## Traps to remember (from my errors/log)
   - <correction 1>
   - <correction 2>
   ...max 5

   ## Blind-spot formulas (memorize these — no HW drilled them)
   <one formula per blind-spot section, boxed>
   ```

3. **Write to** `cheatsheet/final.md`.

4. **If `--pdf` in arguments:** render `cheatsheet/final.pdf`.
   - Call MCP tool `paideia-mcp.render_cheatsheet_pdf(source='cheatsheet/final.md', out='cheatsheet/final.pdf')` if available.
   - Fallback: use `reportlab` with 2-column layout, 9pt font, minimal margins.
   - Remember: **no Unicode subscripts/superscripts in reportlab** — use `<sub>`/`<super>` XML tags.
   - If `pypandoc` is available as an alternative: `pypandoc.convert_file('final.md', 'pdf', outputfile='final.pdf')`.

5. **Print to chat:**
   - Filename of the cheatsheet.
   - Rough word count / page estimate.
   - Closing: "시험장에 가져갈 수 있는 자료는 강의 규정 확인. 반입 불가면 최소한 이걸 마지막으로 스캔해서 외워."

## Density tips

- Formulas only, no sentences. Anything derivable in the user's head doesn't belong.
- Use abbreviations the user will recognize (no first-time notation).
- Group by when-you'll-need-it, not by pedagogical order.
- The **"traps"** section is the most valuable — it's tailored to the user's specific mistakes.

## Conventions

- Korean prose, LaTeX math (`$...$`, `$$...$$`).
- Keep the generated cheatsheet dense; keep chat output ≤ 15 lines.
