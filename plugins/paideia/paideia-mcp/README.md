# paideia-mcp

Stdio MCP server that powers the PAIDEIA Codex plugin. Owns the four pieces of heavy logic that skills should not attempt to do inline:

| Tool | Purpose |
|------|---------|
| `ingest_pdfs` | Render every `materials/**/*.pdf` to PNGs, resize to ≤1800 px long edge, then either (a) hand page paths back to the skill when `engine=codex-native` (Codex reads them with its bundled vision), or (b) OCR in-process and write LaTeX markdown to `converted/**` when `engine=qwen3-vl` / `tesseract`. |
| `grade_pdf` | Same dual behavior for a single hand-written answer PDF: `codex-native` rasterizes + returns page paths; `qwen3-vl` / `tesseract` run OCR in-process and write `answers/converted/<stem>.md` with a confidence tier. |
| `build_course_index` | Read `converted/**`, extract topic tree / recurring solution patterns (P1..Pk) / HW-density coverage, write `course-index/{summary,patterns,coverage}.md`. |
| `course_phase` | Artifact-derived phase (setup → diag → drill → mock → cram → cool). Returns `{phase, days_until_exam, top_miss_pattern}`. Replaces the Claude Code statusline's phase logic. |

Why MCP and not inline in skills: the ingest pipeline needs deterministic parallelism (`ProcessPoolExecutor` with bounded workers, resumable per PDF), which is fragile and context-heavy when driven from an agent loop. Pushing it into an MCP tool keeps skills thin (~40–80 lines of orchestration) and makes the whole pipeline `codex exec`-friendly.

## Running

Launched automatically by Codex when the plugin is installed (declared in `plugins/paideia/.mcp.json`). For dev / CI:

```bash
python3 -m paideia_mcp.server
```

## Layout

```
paideia_mcp/
├── server.py           stdio entrypoint, tool registration
├── ingest.py           ingest_pdfs tool (dual-mode: rasterize-only vs ocr-complete)
├── grade.py            grade_pdf tool (same dual-mode)
├── analyze.py          build_course_index tool
├── phase.py            course_phase tool
└── ocr/
    ├── qwen3vl.py        local Ollama Qwen3-VL 8B
    └── tesseract.py      pytesseract eng and/or kor (whichever is installed)
```

No `openai_vision.py`: the `codex-native` engine doesn't run OCR inside the MCP. It rasterizes PDFs to `.paideia-cache/pages/<stem>/p01.png` and returns a manifest so the calling skill can read pages with Codex CLI's bundled vision — the same vision ChatGPT Plus/Pro/Business subscribers already pay for via their subscription. No `OPENAI_API_KEY`, no separate API billing.

## Engines

| Engine | Default? | MCP does OCR? | Needs | Quality on handwriting | Quality on slides |
|---|---|---|---|---|---|
| `codex-native` | yes | no — skill reads page images via Codex's built-in vision | Codex CLI logged in with ChatGPT Plus/Pro/Business/Edu/Enterprise (no extra API key) | high | high |
| `qwen3-vl` | no | yes | `ollama pull qwen3-vl:8b` (~6 GB) | high, offline | high, offline |
| `tesseract` | no | yes | `tesseract` + at least one of `tesseract-ocr-eng` / `tesseract-ocr-kor` traineddata | low | medium |
