---
name: paideia-ingest
description: Convert every PDF under materials/** into LaTeX-faithful markdown under converted/**. Default engine (codex-native) rasterizes each PDF and hands the page images back for Codex to read with its bundled vision; qwen3-vl / tesseract run OCR inside the paideia-mcp server. Idempotent — skips files whose converted target already exists; pass --force to reconvert.
---

# paideia-ingest

Drive `materials/**/*.pdf` → `converted/**/*.md` through the bundled `paideia-mcp` MCP server. The server does the deterministic work (rasterize at dpi=160 → resize ≤1800 px long edge → `ProcessPoolExecutor` fan-out) and hands results back in one of two shapes depending on the engine.

Skill body stays thin. Heavy fan-out lives in `paideia-mcp.ingest_pdfs`.

## Arguments (free-form)

- `--force` — reconvert even if `converted/<cat>/<stem>.md` already exists
- `--ocr=<engine>` — override the OCR engine for this call (`codex-native` / `qwen3-vl` / `tesseract`)
- `--only=<cats>` — restrict to a subset of `lectures,textbook,homework,solutions` (comma-separated)

## Routing rule

**Every PDF in `materials/**` goes through a vision pipeline.** `pdfplumber` was tried as a fast path for prose-heavy material and proved unreliable — even pages that *look* like plain prose silently word-salad once they mix equations, figures, or multi-column layout. One uniform pipeline is the right call; caching is per-file.

| Source | Method |
|---|---|
| `materials/**/*.pdf` | `paideia-mcp.ingest_pdfs` (engine-dependent, see below) |
| `materials/**/*.md` | Copy-through with provenance header (handled inside the MCP tool) |

Hand-written answer PDFs (`answers/*.pdf`) are a different path — use `$paideia-grade`, not `$paideia-ingest`.

## Procedure

### Step 1 — Preflight

Verify the CWD has a `materials/` directory. If not, tell the user to run `$paideia-init-course` first.

Read `.course-meta` to learn the default `OCR_ENGINE`. Precedence for this call:

1. `--ocr=<engine>` in this call's arguments
2. `OCR_ENGINE` in `.course-meta`
3. `codex-native` as the ultimate default

No API-key check is needed — `codex-native` uses the Codex CLI session's bundled vision (already paid for via the user's ChatGPT Plus/Pro/Business subscription); `qwen3-vl` hits a local Ollama at `localhost:11434`; `tesseract` is fully local.

### Step 2 — Call `paideia-mcp.ingest_pdfs`

Invoke the MCP tool with the arguments you resolved:

```
paideia-mcp.ingest_pdfs(
  engine     = "<resolved engine>",
  force      = <true if --force in args, else false>,
  categories = <optional list from --only=..., else omit>
)
```

The tool returns one of two response shapes, keyed by `mode`:

**`mode: "ocr-complete"`** (`qwen3-vl` / `tesseract`) — the MCP wrote `converted/**/*.md` directly. You just print a summary:

```json
{
  "mode": "ocr-complete",
  "engine": "qwen3-vl",
  "converted": [{"path": "...", "destination": "...", "pages": N}],
  "skipped":   ["..."],
  "failed":    [{"path": "...", "error": "..."}]
}
```

**`mode: "rasterize-only"`** (`codex-native`) — the MCP wrote PNGs under `.paideia-cache/pages/<stem>/p01.png`, `p02.png`, ... and handed the manifest back. You must now turn those images into markdown yourself:

```json
{
  "mode": "rasterize-only",
  "engine": "codex-native",
  "pending": [
    {
      "path":        "materials/lectures/ch01.pdf",
      "destination": "<abs>/converted/lectures/ch01.md",
      "pages":       14,
      "page_paths":  ["<abs>/.paideia-cache/pages/ch01/p01.png", ...],
      "category":    "lectures"
    }
  ],
  "skipped":     ["..."],
  "failed":      [{"path": "...", "error": "..."}],
  "ingested_at": "2026-04-22T09:15:02Z"
}
```

### Step 2a — Only for `rasterize-only`: transcribe each pending PDF

For **each entry in `pending`**, open every `page_paths[i]` image with Codex's built-in vision (you can read each PNG the same way you read any local image), transcribe page-by-page, and write the combined result to `destination`.

Prompt skeleton for each page (apply uniformly, translate any chat to Korean if the user prefers):

> Transcribe the provided PDF page into GitHub-flavored markdown. Use LaTeX for math (`$...$` inline, `$$...$$` display), never Unicode glyphs. Preserve heading levels, lists, and tables. When a glyph is illegible, write `[?]` and keep going. Output only the markdown — no preface, no commentary.

Between pages, insert the page separator `\n\n---\n\n`. Prefix the whole file with this provenance header + title:

```
<!-- source: materials/<cat>/<stem>.pdf -->
<!-- engine: codex-native -->
<!-- pages: <N> -->
<!-- ingested: <ingested_at from the response> -->

# <stem>

<page 1 markdown>

---

<page 2 markdown>

...
```

Create the destination directory if needed (`mkdir -p`). Write the file in one shot. Do **not** leave partial files on failure — if a page transcription fails, skip writing that PDF's markdown and add `{path, error}` to the failed list you'll report in Step 3.

Parallelism: if there are multiple PDFs in `pending`, it's fine to spawn a subagent per PDF (one-agent-per-PDF, sequential pages is the contract). Each subagent gets one entry from `pending` and writes its own destination. Do not fan out across pages inside a single PDF — Codex context stays cleaner when a single agent sees a PDF end-to-end.

For very large PDFs (>30 pages), consider chunking the page list into batches of ~10 and emitting partial progress to the user.

### Step 3 — Render the summary

Print a compact table:

```
| Category  | Converted | Skipped | Failed |
|-----------|-----------|---------|--------|
| lectures  | N         | M       | F      |
| textbook  | ...       | ...     | ...    |
| homework  | ...       | ...     | ...    |
| solutions | ...       | ...     | ...    |
```

For `rasterize-only` runs, "Converted" means "PDFs you successfully wrote markdown for in Step 2a" — add the MCP's `failed` entries to your own Step 2a failures for the `Failed` column.

For each entry in `failed`, surface the error and a suggested workaround:

- Password-protected PDF → `qpdf --password=... --decrypt in.pdf out.pdf` first, then re-run
- Timeout / transient engine error → `$paideia-ingest --force` to retry just that file
- Render step OOM on huge PDF → split the PDF first, ingest each half
- `codex-native` page-read failure → rerun, or fall back with `$paideia-ingest --ocr=qwen3-vl`

End with one line:

```
다음 단계: $paideia-analyze 로 patterns / coverage / summary 생성
```

## Conventions

- Math renders as LaTeX (`$...$`, `$$...$$`), not Unicode glyphs. For `codex-native` this is your job via the transcription prompt; for the in-process engines the MCP enforces it.
- Each output file starts with `<!-- source: ... -->`, `<!-- engine: ... -->`, `<!-- pages: N -->`, `<!-- ingested: <ISO> -->`.
- `[?]` marks mean a glyph couldn't be read confidently. Count them and flag files with >5 `[?]` in the summary.
- `.paideia-cache/` is gitignored; the rasterized PNGs are a private working set for the `codex-native` flow. They're safe to delete after ingest.
- Skill output ≤ 25 lines; any per-page chatter from subagents is their own to produce — don't paraphrase it into the main thread.
