---
name: paideia-ingest
description: Convert every PDF under materials/** into LaTeX-faithful markdown under converted/**, via the bundled paideia-mcp server's parallel vision pipeline. Idempotent — skips files whose converted target is newer than the source; pass --force to reconvert.
---

# paideia-ingest

Drive `materials/**/*.pdf` → `converted/**/*.md` through the bundled `paideia-mcp` MCP server. The server handles the whole pipeline in-process: render at dpi=160 → resize ≤1800 px → parallel OCR via the selected engine → write LaTeX markdown with provenance headers.

Skill body stays thin. The heavy logic (`ProcessPoolExecutor` fan-out, per-engine dispatch, LaTeX-faithful transcription) is all in `paideia-mcp`'s `ingest_pdfs` tool.

## Arguments (free-form)

- `--force` — reconvert even if `converted/<cat>/<stem>.md` is newer than the source
- `--ocr=<engine>` — override the OCR engine for this call (`openai-vision` / `qwen3-vl` / `tesseract`)
- `--only=<cats>` — restrict to subset of `lectures,textbook,homework,solutions` (comma-separated)

## Routing rule

**Every PDF in `materials/**` goes through the vision pipeline.** `pdfplumber` was tried as a fast path for prose-heavy material and proved unreliable — even pages that *look* like plain prose silently word-salad once they mix equations, figures, or multi-column layout. One uniform pipeline is the right call; the extra OCR cost is bounded and caching is per-file.

| Source | Method |
|---|---|
| `materials/**/*.pdf` | Vision pipeline via `paideia-mcp.ingest_pdfs` |
| `materials/**/*.md` | Copy-through with provenance header (handled inside the MCP tool) |

Hand-written answer PDFs (`answers/*.pdf`) are a different path — use `$paideia-grade`, not `$paideia-ingest`.

## Procedure

### Step 1 — Preflight

Verify the CWD has a `materials/` directory. If not, tell the user to run `$paideia-init-course` first.

Read `.course-meta` to learn the default `OCR_ENGINE`. Precedence for this call:

1. `--ocr=<engine>` in this call's arguments
2. `OCR_ENGINE` in `.course-meta`
3. `openai-vision` as the ultimate default

If the chosen engine is `openai-vision`, verify `OPENAI_API_KEY` is exported. If unset, stop and ask the user to export it (or re-run with `--ocr=qwen3-vl` / `--ocr=tesseract`).

### Step 2 — Call `paideia-mcp.ingest_pdfs`

Invoke the MCP tool with the arguments you resolved:

```
paideia-mcp.ingest_pdfs(
  engine     = "<resolved engine>",
  force      = <true if --force in args, else false>,
  categories = <optional list from --only=..., else omit>
)
```

The tool returns a JSON summary shaped like:

```json
{
  "converted": [...],
  "skipped":   [...],
  "failed":    [{"path": "...", "error": "..."}],
  "counts":    {"lectures": {...}, "textbook": {...}, ...}
}
```

Do not await images or page contents — the tool writes `converted/**/*.md` directly and returns only the summary. Your context stays clean.

### Step 3 — Render the summary

Print a compact table from `counts`:

```
| Category  | Converted | Skipped | Failed |
|-----------|-----------|---------|--------|
| lectures  | N         | M       | F      |
| textbook  | ...       | ...     | ...    |
| homework  | ...       | ...     | ...    |
| solutions | ...       | ...     | ...    |
```

For each entry in `failed`, surface the error and its suggested workaround:

- Password-protected PDF → `qpdf --password=... --decrypt in.pdf out.pdf` first, then re-run
- Timeout / transient API error → `$paideia-ingest --force` to retry just that file
- Render step OOM on huge PDF → split the PDF first, ingest each half

End with one line:

```
다음 단계: $paideia-analyze 로 patterns / coverage / summary 생성
```

## Conventions

- Math renders as LaTeX (`$...$`, `$$...$$`), not Unicode glyphs — the MCP tool enforces this in its OCR prompt.
- Each output file starts with `<!-- SOURCE: materials/<cat>/<stem>.pdf, extracted <DATE>, engine: <ENGINE> -->`.
- `[?]` marks mean the OCR could not read a glyph confidently. Count them in the summary and flag files with >5 `[?]`.
- Skill output ≤ 25 lines; the tool's own log chatter is the user's to read on demand, not for you to paraphrase.
