---
name: paideia-grade
description: Grade a hand-written, scanned answer PDF. OCR via the engine set in .course-meta (override with --ocr=codex-native|qwen3-vl|tesseract). codex-native rasterizes pages and lets Codex read them via its bundled vision; the others OCR inside the MCP. Strategy-based grading (pattern / variables / end-form) against the reference solution. Errors append to errors/log.md for weakmap and cheatsheet.
---

# paideia-grade

Convert a hand-written scan to markdown, then grade the user's approach against the reference solution by strategy — not line-by-line algebra. OCR noise in hand-writing makes strict algebraic grading useless, and pattern recognition is the actual exam bottleneck.

## Arguments (free-form)

- Positional: path to answer file (`answers/<stem>.pdf` or an already-cleaned `.md`). If omitted, use the most recently modified file in `answers/` that isn't in `answers/converted/`.
- `--ocr=<engine>` — override engine for this call (`codex-native` / `qwen3-vl` / `tesseract`).

## Step 1 — Resolve target + engine

1. If `$ARGUMENTS` has a positional path, use it. Else pick `answers/*.pdf` (or `*.md`) with the newest `mtime`.
2. If target is `.md`, skip Step 2 entirely — treat it as user-cleaned OCR output and jump to Step 3.
3. Engine precedence: `--ocr=` flag → `OCR_ENGINE` in `.course-meta` → `codex-native`.
4. No API-key check — `codex-native` uses the Codex CLI session's bundled vision (no `OPENAI_API_KEY` needed).

## Step 2 — Call `paideia-mcp.grade_pdf` (PDF only)

```
paideia-mcp.grade_pdf(
  path   = "<resolved target>",
  engine = "<resolved engine>"   # omit to let the server read .course-meta
)
```

The response shape depends on `mode`:

**`mode: "ocr-complete"`** (`qwen3-vl` / `tesseract`) — the MCP already wrote `answers/converted/<stem>.md`:

```json
{
  "mode":            "ocr-complete",
  "markdown_path":   "answers/converted/<stem>.md",
  "pages_processed": <int>,
  "tier":            "medium" | "low",
  "engine":          "qwen3-vl" | "tesseract",
  "source":          "answers/<stem>.pdf"
}
```

**`mode: "rasterize-only"`** (`codex-native`) — the MCP wrote per-page PNGs under `answers/.paideia-cache/<stem>/p01.png` ... and handed the list back:

```json
{
  "mode":        "rasterize-only",
  "engine":      "codex-native",
  "tier":        "high",
  "destination": "<abs>/answers/converted/<stem>.md",
  "page_paths":  ["<abs>/answers/.paideia-cache/<stem>/p01.png", ...],
  "pages":       <int>,
  "source":      "answers/<stem>.pdf",
  "ingested_at": "2026-04-22T..."
}
```

### Step 2a — Only for `rasterize-only`: read pages + write markdown

Open each `page_paths[i]` image with Codex's bundled vision and transcribe page-by-page. Hand-written math is the hard case: use this prompt per page (adjust to Korean if the user prefers):

> Transcribe the hand-written answer PDF page into markdown. Use LaTeX for math (`$...$`, `$$...$$`). Preserve problem numbering (e.g., `## Problem 2`, `### (a)`). Where a glyph is unreadable, write `[?]` and keep going — do not guess. Output only the markdown.

Write the combined result to `destination` with this header:

```
# Vision-OCR transcription

<!-- source: answers/<stem>.pdf -->
<!-- engine: codex-native -->
<!-- tier: high -->
<!-- pages: <N> -->
<!-- ingested: <ingested_at> -->

## Page 1

<page 1 markdown>

## Page 2

<page 2 markdown>

...
```

If a page transcription fails, surface the OCR quality escape hatch (below) and stop — don't grade on a partial transcription.

### Step 2b — Tier-gated quality check

If `tier == "low"` (tesseract fallback, or <100 chars of extracted text after your transcription), print the **OCR quality escape hatch** below and stop. Do not grade on garbled text.

```
OCR 결과 품질이 낮음 (채점 신뢰도 떨어짐).
옵션:
  (a) $paideia-grade --ocr=codex-native <pdf>   ← Codex 내장 비전으로 재시도 (기본)
  (b) 더 밝게/크게 재스캔 후 다시 $paideia-grade
  (c) 답안을 직접 .md로 타이핑해서 answers/converted/<stem>.md 에 저장 후 다시 $paideia-grade
  (d) 채점 대신 $paideia-blind <problem-id>로 전략만 말로 체크
```

## Step 3 — Locate the reference solution

Based on the answer filename stem:

- `hw3.pdf` → `converted/solutions/hw3_sol.md` (or `converted/solutions/hw3.md`)
- `diagnostic.pdf` → `quizzes/diagnostic_answers.md`
- `<topic>_<ts>.pdf` → `quizzes/<topic>_<ts>_answers.md`
- `twin_<id>_<ts>.pdf` → `twins/<id>_<ts>_sol.md`
- `chain_<ts>.pdf` → `chain/<ts>_sol.md`
- `mock_<ts>.pdf` → `mock/<ts>_sol.md`

If unresolvable, ask the user to specify.

Also open `course-index/patterns.md` — you will cite `Pk` labels in the grade.

## Step 4 — Strategy-based grading

For each numbered problem in the user's OCR'd markdown, judge four things against the reference:

1. **Pattern match** — did the user invoke the right `Pk` from `patterns.md`?
2. **Variable choice** — did they hold the right things fixed / identify the right substitution, basis, index, or contour?
3. **End form** — does their final expression have the right shape (dimensions, asymptotics, structure)?
4. **Completeness** — where did they stop? Partial credit if the approach was correct but execution truncated.

Do **not** grade individual algebraic steps — one misread `∫` vs `∑` in OCR would cascade, and that's not the exam bottleneck anyway.

## Step 5 — Compact grade table (≤ 15 lines)

```
| P#  | Pattern | Vars | End form | Overall |
|-----|---------|------|----------|---------|
| 1   | ✅ P3   | ✅   | ✅       | 만점     |
| 2   | ❌ P5→P7 wrong invoke | — | — | 패턴 오인 |
| 3   | ✅ P2   | ⚠️   | ✅       | 부분    |
| ...
```

Close with exactly one line:

```
우세한 실수: <type>. 다음 드릴: $paideia-<command> <target>.
```

Where `<type>` is one of `pattern-missed | wrong-variable | wrong-end-form | algebraic | sign | definition`, and the recommended next drill matches the dominant error type:

- `pattern-missed` → `$paideia-blind <problem-id>` (strategy-only re-attempt)
- `wrong-variable` → `$paideia-twin <problem-id>` (same pattern, new surface forces re-identification)
- `wrong-end-form` → `$paideia-derive <topic>` (re-anchor the canonical form)
- `algebraic / sign` → `$paideia-quiz <§> 3` (pure reps on the same section)
- `definition` → `$paideia-pattern <Pk>` (re-read the card)

## Step 6 — Log errors

For every non-✅ row, append one YAML entry to `errors/log.md`:

```yaml
- problem_id: <id as it appears in the answer file, e.g. hw3-p2>
  pattern:    <Pk>
  error_type: pattern-missed | wrong-variable | wrong-end-form | algebraic | sign | definition
  summary:    "<one-line English or Korean description>"
  date:       <ISO8601>
```

This log is the **sole seed** of `$paideia-weakmap` and `$paideia-cheatsheet --pdf`. Do not skip it even if the user groans.

## Step 7 — What NOT to do

- Do **not** print the full reference solution. The user opens it themselves if they want to study.
- Do **not** exceed 15 lines of grade output in chat. Detail belongs in the error log, not in chat.
- Do **not** re-grade a `.md` that already has a paired `errors/log.md` entry with the same `problem_id` + `date` — it creates duplicate weight for `$paideia-weakmap`.

## When both `.pdf` and `.md` exist

If `answers/<stem>.pdf` AND `answers/converted/<stem>.md` both exist and the `.md` was edited within the last hour, use the `.md` directly — the user likely hand-cleaned the OCR output. Skip Step 2.
