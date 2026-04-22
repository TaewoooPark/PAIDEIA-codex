# paideia-mcp

Stdio MCP server that powers the PAIDEIA Codex plugin. Owns the four pieces of heavy logic that skills should not attempt to do inline:

| Tool | Purpose |
|------|---------|
| `ingest_pdfs` | Render every `materials/**/*.pdf` to PNGs, resize to ≤1800 px long edge, parallel-OCR via the selected engine (`openai-vision` / `qwen3-vl` / `tesseract`), write LaTeX markdown to `converted/**`. |
| `grade_pdf` | OCR a single hand-written answer PDF via the engine set in `.course-meta` (override via arg), write `answers/converted/<stem>.md`, return the markdown plus a confidence tier. |
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
├── ingest.py           ingest_pdfs tool
├── grade.py            grade_pdf tool
├── analyze.py          build_course_index tool
├── phase.py            course_phase tool
└── ocr/
    ├── openai_vision.py  calls the OpenAI Responses API (needs OPENAI_API_KEY)
    ├── qwen3vl.py        local Ollama Qwen3-VL 8B
    └── tesseract.py      pytesseract eng+kor
```

## Engines

| Engine | Default? | Needs | Quality on handwriting | Quality on slides |
|---|---|---|---|---|
| `openai-vision` | yes | `OPENAI_API_KEY` | high | high |
| `qwen3-vl` | no | `ollama pull qwen3-vl:8b` (~6 GB) | high, offline | high, offline |
| `tesseract` | no | `tesseract-ocr-kor` | low | medium |
