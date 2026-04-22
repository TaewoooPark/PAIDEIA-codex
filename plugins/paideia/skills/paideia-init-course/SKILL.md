---
name: paideia-init-course
description: Bootstrap the current directory into a fresh PAIDEIA course workspace. Checks system dependencies (Python, poppler, tesseract, optionally ollama), prompts for course metadata plus an OCR engine (openai-vision / qwen3-vl / tesseract), creates the directory skeleton, writes AGENTS.md, and runs git init. Run once per course folder, in that folder's CWD.
---

# paideia-init-course

Turn the user's current working directory into a PAIDEIA workspace. Everything you create lives in the **user's CWD**, not in the plugin. The plugin itself (skills + the bundled `paideia-mcp` MCP server) is already loaded — your job is the per-course state.

Keep chat output compact. The user is watching progress.

## Step 1 — Check system binaries

```bash
command -v pdftoppm  >/dev/null 2>&1 && echo "poppler: ok"   || echo "poppler: MISSING"
command -v tesseract >/dev/null 2>&1 && echo "tesseract: ok" || echo "tesseract: MISSING"
command -v ollama    >/dev/null 2>&1 && echo "ollama: ok (optional)" || echo "ollama: not installed (optional, only needed for --ocr=qwen3-vl)"
tesseract --list-langs 2>&1 | grep -q '^kor$' && echo "tesseract-kor: ok" || echo "tesseract-kor: MISSING"
```

`poppler` and `tesseract` (+ Korean trained data) are required. `ollama` is only needed if the user picks `qwen3-vl` in Step 3. For missing items, print the install command — do not auto-run, they typically need sudo/brew:

- macOS: `brew install poppler tesseract tesseract-lang`
- Ubuntu: `sudo apt-get install poppler-utils tesseract-ocr tesseract-ocr-kor`

## Step 2 — Check Python deps

```bash
python3 -c "import mcp.server, pypdf, pytesseract, pdf2image, PIL, reportlab, httpx" 2>&1 \
  || echo "MISSING_PYTHON_DEPS"
```

`mcp` is the stdio protocol package that the bundled `paideia-mcp` server imports at startup — if it's missing, Codex shows a scary "MCP startup failed: handshaking with MCP server failed" banner on every session start. Installing it here clears that. `httpx` is needed by the `openai-vision` and `qwen3-vl` OCR paths. The rest (`pypdf`, `pytesseract`, `pdf2image`, `pillow`, `reportlab`) are the PDF + OCR + cheatsheet-PDF pipeline.

If any are missing, offer:

```bash
python3 -m pip install --break-system-packages --user \
  "mcp>=1.2.0" pypdf pytesseract pdf2image pillow reportlab httpx
```

Run only with the user's OK. After install completes, tell the user to restart their Codex session so the MCP server is re-spawned with deps in place.

## Step 3 — Ask: which OCR engine?

Ask the user in Korean:

```
OCR 엔진을 선택해 주세요 (이후 `$paideia-grade --ocr=<engine>`로 호출마다 덮어쓸 수 있습니다):

  1) openai-vision — OpenAI Vision (기본값, OPENAI_API_KEY 필요, 필기 정확도 높음)
  2) qwen3-vl      — 로컬 Qwen3-VL 8B (외부 전송 전혀 없음, 최초 ~6 GB 다운로드 필요)
  3) tesseract     — pytesseract eng+kor (가장 가볍고 빠름, 필기 정확도는 낮음)

  입력 없이 Enter 시: openai-vision
```

Normalize to one of `openai-vision` / `qwen3-vl` / `tesseract`. Hold the value as `$OCR_ENGINE` for later steps.

If the user picked `openai-vision`, also verify `OPENAI_API_KEY` is set (`test -n "$OPENAI_API_KEY" && echo set || echo unset`). If unset, warn — the first `$paideia-ingest` or `$paideia-grade` will fail until it's exported.

## Step 3a — Ollama model pull (only if `$OCR_ENGINE = qwen3-vl`)

Skip entirely for `openai-vision` / `tesseract`.

If ollama binary is missing: stop and tell the user to install it first (`brew install ollama` on macOS, `https://ollama.com/install.sh` on Linux), then re-run `$paideia-init-course`.

Otherwise:

```bash
curl -fsS --max-time 2 http://localhost:11434/api/tags >/dev/null 2>&1 \
  && echo "daemon: up" || echo "daemon: down — run 'ollama serve &' in another shell"

if ! ollama list 2>/dev/null | awk '{print $1}' | grep -qx "qwen3-vl:8b"; then
  LOG=$(mktemp -t paideia-ollama-pull.XXXXXX.log)
  ( ollama pull qwen3-vl:8b > "$LOG" 2>&1 ) &
  echo "BACKGROUND_PULL_PID=$!"
  echo "LOG=$LOG"
fi
```

Hold the PID + LOG path. Report: "ollama 모델 백그라운드 pull 시작 (~6 GB, 메타데이터 입력과 병렬 진행)."

## Step 4 — Ask course metadata

Ask four short questions in Korean:

1. `COURSE_NAME` (예: Complex Analysis MATH 405)
2. `EXAM_DATE` (YYYY-MM-DD)
3. `EXAM_TYPE` (midterm / final / qualifier)
4. `WEAK_ZONES` (comma-separated topics, or `unknown`)

Wait for all four responses. Do not proceed without them.

## Step 5 — Scaffold (single Python call)

Call the bundled scaffolder with the collected values. It creates the directory skeleton, writes `.course-meta`, writes `AGENTS.md` from the template, seeds `errors/log.md`, and runs `git init` + `.gitignore` idempotently.

```bash
python3 "${CODEX_PLUGIN_ROOT}/skills/paideia-init-course/scripts/bootstrap.py" \
  --course-name  "$COURSE_NAME" \
  --exam-date    "$EXAM_DATE" \
  --exam-type    "$EXAM_TYPE" \
  --weak-zones   "$WEAK_ZONES" \
  --ocr-engine   "$OCR_ENGINE"
```

The scaffolder prints one line per file written (or `skip: ...` for idempotent no-ops). If it exits non-zero, surface its stderr and stop — do not press on with a half-built course folder.

## Step 6 — Wait on background pull (if any)

If Step 3a spawned a pull, `wait $BACKGROUND_PULL_PID` and report success or point the user at `$LOG`.

## Step 7 — Print next steps

```
✅ <COURSE_NAME> 준비 완료. (OCR: <OCR_ENGINE>)

다음 단계:
  1. materials/{lectures,textbook,homework,solutions}/ 에 PDF / MD 드롭
  2. $paideia-ingest        ← PDFs → LaTeX markdown
  3. $paideia-analyze       ← patterns, coverage, summary 생성
  4. $paideia-hwmap hot     ← 🔥🔥 시험 핫존 확인
```

## Notes

- `AGENTS.md` is the Codex equivalent of `CLAUDE.md` — Codex reads it every turn. If `AGENTS.md` already exists in CWD, the scaffolder **does not overwrite it** — it prints `skip: AGENTS.md exists (leaving alone)`. Ask the user if they want to merge the PAIDEIA template in by hand.
- This skill is idempotent. Re-running it on an already-initialized folder only refreshes `.course-meta` and tops up any missing directories.
- No statusline wiring: Codex CLI does not currently expose a persistent statusline slot. The phase readout is available on demand via `$paideia-phase`, or by calling `paideia-mcp.course_phase` from any skill.
