<h1 align="center">ΠΑΙΔΕΙΑ · Paideia <sub>(Codex edition)</sub></h1>

<p align="center">
  <strong>Your course. Your patterns. Your errors. Your cheatsheet.</strong><br>
  <em>An OpenAI Codex CLI plugin that turns your own materials into a permanent, editable, per-course study graph — every artifact shaped by you, not by a generic syllabus.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/github/license/TaewoooPark/PAIDEIA-codex?style=flat-square&labelColor=000000&color=333333&cacheSeconds=3600" alt="License">
  <img src="https://img.shields.io/github/stars/TaewoooPark/PAIDEIA-codex?style=flat-square&logo=github&logoColor=white&labelColor=000000&color=333333&cacheSeconds=3600" alt="GitHub stars">
  <img src="https://img.shields.io/github/last-commit/TaewoooPark/PAIDEIA-codex?style=flat-square&labelColor=000000&color=333333&cacheSeconds=3600" alt="Last commit">
  <img src="https://img.shields.io/github/languages/top/TaewoooPark/PAIDEIA-codex?style=flat-square&labelColor=000000&color=333333&cacheSeconds=3600" alt="Top language">
  &nbsp;
  <img src="https://img.shields.io/badge/OpenAI%20Codex-000000?style=flat-square&logo=openai&logoColor=white&labelColor=000000&cacheSeconds=3600" alt="OpenAI Codex">
  <img src="https://img.shields.io/badge/Plugin-000000?style=flat-square&labelColor=000000&color=000000&cacheSeconds=3600" alt="Plugin">
  <img src="https://img.shields.io/badge/MCP-000000?style=flat-square&labelColor=000000&color=000000&cacheSeconds=3600" alt="MCP">
  <img src="https://img.shields.io/badge/Markdown-000000?style=flat-square&logo=markdown&logoColor=white&labelColor=000000&cacheSeconds=3600" alt="Markdown">
  <img src="https://img.shields.io/badge/Python-000000?style=flat-square&logo=python&logoColor=white&labelColor=000000&cacheSeconds=3600" alt="Python">
  <img src="https://img.shields.io/badge/Ollama-000000?style=flat-square&logo=ollama&logoColor=white&labelColor=000000&cacheSeconds=3600" alt="Ollama">
  <img src="https://img.shields.io/badge/Qwen3--VL-000000?style=flat-square&labelColor=000000&color=000000&cacheSeconds=3600" alt="Qwen3-VL">
  <img src="https://img.shields.io/badge/Tesseract-000000?style=flat-square&labelColor=000000&color=000000&cacheSeconds=3600" alt="Tesseract">
  &nbsp;
  <img src="https://img.shields.io/badge/LaTeX-000000?style=flat-square&logo=latex&logoColor=white&labelColor=000000&cacheSeconds=3600" alt="LaTeX">
  <img src="https://img.shields.io/badge/Obsidian-000000?style=flat-square&logo=obsidian&logoColor=white&labelColor=000000&cacheSeconds=3600" alt="Obsidian">
</p>

<p align="center">
  <a href="./README.ko.md">한국어 README</a>
</p>

<p align="center">
  <sub>Claude Code edition of the same plugin: <a href="https://github.com/TaewoooPark/PAIDEIA">TaewoooPark/PAIDEIA</a></sub>
</p>

---

<p align="center">
  <em>Generic study tools teach you the average syllabus. Paideia teaches you <strong>your</strong> syllabus —<br>
  from your professor's notes, your HW emphases, your handwriting, your errors. Every artifact is a markdown file you can edit.</em>
</p>

---

## What Paideia means

In ancient Greece, **Παιδεία** was never the deposit of facts into a passive student. It was the lifelong formation of a complete human being — through structured encounter with primary texts, guided practice under a master, and reflective dialogue that folds feedback into deeper revision.

This plugin implements that cycle for the specific, bounded problem of **exam preparation** in math, physics, and engineering courses:

```
  ingest ──▶ analyze ──▶ drill ──▶ grade ──▶ weakmap ──▶ cheatsheet
     ▲                                                        │
     └────────────────── feedback loop ───────────────────────┘
```

Every stage produces a markdown artifact that lives in your course folder forever. Nothing is ephemeral. Nothing is hidden behind an API. Nothing stops working when the next funding winter hits.

---

## Why a Codex edition

> **2026-04-21 note.** On April 21, 2026, scattered reports suggested Anthropic had revoked Claude Code access for the Pro tier. Anthropic later clarified that this was only a limited test rolled out to a subset of new users — not a wholesale restriction. The Codex edition was built and shipped that same day amid the uncertainty, and it stands on its own regardless: the port is a CLI-agnostic alternative that lets you run PAIDEIA under whichever agentic CLI you already pay for. Both editions are maintained; pick whichever one fits your subscription.

PAIDEIA was born as a Claude Code plugin. The heavy lifting — parallel vision ingest, strategy grading, pattern extraction from *your* solutions — didn't depend on Claude specifically; it depended on *any* agentic CLI with skills, subagents, plugins, and a workable vision path. OpenAI Codex CLI grew those affordances in 2026 (skills, subagents, MCP, plugins, `AGENTS.md`), so the port was a matter of re-homing the logic onto Codex's primitives, not rewriting the study graph.

The study graph on disk is **byte-for-byte the same**. `course-index/patterns.md`, `errors/log.md`, `weakmap/weakmap_<ts>.md`, `cheatsheet/final.md` — all the artifacts the Claude edition writes, this edition also writes, in the same format. Fork a course folder from the Claude edition into this one (or vice versa) and the new runner picks up without friction.

### What moved

| Concept | Claude Code edition | Codex edition |
|---|---|---|
| Verb syntax | `/paideia:ingest` | `$paideia-ingest` |
| Project context file | `CLAUDE.md` | `AGENTS.md` |
| Plugin-root variable | `${CLAUDE_PLUGIN_ROOT}` | `${CODEX_PLUGIN_ROOT}` |
| Heavy pipeline host | Per-PDF `general-purpose` subagents | Bundled `paideia-mcp` stdio MCP server |
| Default OCR | Claude's native vision (no install) | Codex CLI's native vision (no install; no extra API key — uses the ChatGPT Plus/Pro/Business subscription Codex CLI already requires) |
| Local OCR | `ollama` + `qwen3-vl:8b` | same (`qwen3-vl`) |
| Tesseract floor | yes | yes |
| Statusline widget | `paideia · COURSE · D-N · phase · P<k>` | *(not ported — Codex has no persistent statusline slot; phase is available via `$paideia-phase`)* |

Everything else — directory layout, pattern extraction logic, strategy-grading, HW-density exam tiering, the append-only `weakmap/` history, the error-driven cheatsheet — is the same.

---

## What generic study tools can't do

Most study tools can't personalize to *your* course, *your* professor, or *your* mistakes — because the product they sell is a generic curriculum.

- **Coursera, edX, Khan Academy** — fixed curriculum; no idea what your professor actually emphasizes.
- **Quizlet, Anki, Brainscape** — you manually curate every card; nothing derives patterns from your own solution manuals.
- **Chegg, Course Hero** — generic solution manuals; not organized around your course's recurring idioms.
- **Brilliant, Duolingo Max, Khanmigo** — generic exercises; no knowledge of what you got wrong on HW2 last month.
- **ChatGPT Study Mode, Gemini "Deep Study", NotebookLM** — no persistent per-course state. Every new session starts cold, and last week's mistakes don't shape this week's drill unless you re-upload and re-explain.

None of them *form* understanding around the specific material in front of you. They each give every student the same answer. Paideia does the opposite: every artifact is derived from *your* folder — lecture notes, textbook chapter, HW, solutions, handwritten attempts — and accumulates permanently in plain markdown you can edit.

| Axis | Paideia | Typical edu-SaaS / LLM chat |
|-----|---------|------------------------------|
| Solution patterns (`P1..Pk`) | Extracted from *your course's* own solutions, citing your own files | Generic textbook list, or none |
| Drill priority | Weighted by *your professor's* HW emphasis (HW density = exam tier) | Fixed curriculum, or your own guesswork |
| Cheatsheet | Built from *your* `errors/log.md` — whatever you actually got wrong | Boilerplate from the syllabus |
| Per-course state across sessions | Permanent markdown + YAML, grows as you work | Conversation resets; paid tier for history |
| Editing an artifact you disagree with | Open the `.md` in any editor, save | Read-only UI |
| Carrying last semester's prep into next semester | Fork the course folder, edit deltas | Start over |
| Version history of your own understanding | `git log` / `git diff` any artifact | Not surfaced |
| Where the artifacts live | Your disk, as text | Remote DB, exportable only with paid tier |

The plugin uses Codex CLI (which calls paid OpenAI APIs) to do the heavy lifting, but everything it produces lives on your disk as plain markdown. If you later switch to a different model runner, or pause your OpenAI subscription, the course-index, patterns, error log, weakmaps, and cheatsheets are all still yours to open, read, edit, and diff. The scaffold is the plugin; the study graph is yours.

By default, OCR uses Codex CLI's **built-in vision** — the same vision ChatGPT Plus/Pro/Business/Edu/Enterprise subscribers already pay for via their subscription. The plugin just rasterizes each PDF page to PNG under `.paideia-cache/` and hands Codex the image paths to read directly. No separate `OPENAI_API_KEY`, no additional API billing. If you'd rather the handwritten PDFs never leave the machine, `ollama pull qwen3-vl:8b` is a one-time ~6 GB download that flips every subsequent OCR pass to local Qwen3-VL inference. Either way, everything downstream — patterns, coverage, weakmaps, cheatsheets, the error log — is plain markdown on your disk.

---

## The load-bearing principle: HW density = exam probability

Most "study smart" advice tells you to hunt your blind spots. That is **backwards**. The professor has *already told you* where the exam points live — by assigning homework. Sections with heavy HW coverage are 🔥🔥 Exam-primary. Sections with zero HW are ⚪ Low-risk, not "hidden traps". The professor's omission is the strongest possible signal that the topic is off the exam.

Paideia's ranking is explicit about this, and every drill skill honors it by default:

| Tier | HW count on section | Treatment | Share of mock-exam points |
|------|---------------------|-----------|---------------------------|
| 🔥🔥 Exam-primary | 3+ | Drill hardest | ≥70% |
| 🔥 Exam-likely | 2 | Drill next | ~25% |
| 🟡 Exam-possible | 1 | Warm-pass review | ≤5% |
| ⚪ Low-risk | 0 | Reference only | 0 |

`$paideia-quiz all`, `$paideia-mock`, `$paideia-hwmap hot` all weight output by this tiering. If you insist on drilling a ⚪ section, the plugin complies once and warns you that exam probability is low — your limited time is worth more than an imagined gotcha.

---

## The formation cycle, stage by stage

| Stage | What it does | Verbs | Produces |
|-------|-------------|-------|----------|
| **Encounter** | Read the professor's signal | `$paideia-ingest` | `converted/**/*.md` — every lecture, textbook chapter, HW, solution, as clean markdown |
| **Structure** | Extract the grammar of the course | `$paideia-analyze` | `course-index/{summary,patterns,coverage}.md` — topic tree, recurring solution patterns (P1..Pk), HW-density exam-tier ranking |
| **Practice** | Active recall weighted by what the professor actually tests | `$paideia-quiz`, `$paideia-twin`, `$paideia-blind`, `$paideia-chain`, `$paideia-mock` | `quizzes/`, `twins/`, `chain/`, `mock/` — problems you solve on paper |
| **Reflection** | Your hand-written work becomes a grade | `$paideia-grade` | `answers/converted/<name>.md` + `errors/log.md` — OCR via Codex's bundled vision (default), Qwen3-VL, or Tesseract; then strategy-based grading |
| **Diagnosis** | Errors compressed into a priority-ranked weakness report | `$paideia-weakmap` | `weakmap/weakmap_<ts>.md` — append-only history |
| **Distillation** | One page, error-driven, printable | `$paideia-cheatsheet`, `$paideia-derive`, `$paideia-pattern` | `cheatsheet/final.md`, `derivations/<slug>.md` — reference only what you actually need |

Supporting: `$paideia-hwmap` surfaces HW-density exam-probability, `$paideia-init-course` bootstraps a fresh course folder, `$paideia-phase` reports which stage of the cycle the folder is in.

---

## Install

### Prerequisites

**Required**

- [OpenAI Codex CLI](https://github.com/openai/codex) (`codex` on `PATH`), signed in with a ChatGPT Plus / Pro / Business / Edu / Enterprise account (the default OCR engine reads page images via Codex CLI's bundled vision — no separate `OPENAI_API_KEY` needed)
- Python 3.10+ (the bundled MCP server is written in Python)
- A Unix-style shell (`bash` / `zsh`). The bootstrap skill uses heredocs, `mkdir -p`, `mktemp`, and subshell backgrounding — native Windows `cmd` / PowerShell isn't currently supported.
- **macOS**: `brew install poppler` (plus `tesseract tesseract-lang` only if you plan to use the `tesseract` engine)
- **Linux (Debian/Ubuntu)**: `apt-get install poppler-utils` (plus `tesseract-ocr tesseract-ocr-eng tesseract-ocr-kor` only for the `tesseract` engine)
- **Windows**: use [WSL2](https://learn.microsoft.com/windows/wsl/install), then follow the Linux path inside the WSL shell.

**Optional — only if you want the `--ocr=qwen3-vl` mode (every page image stays on your machine)**

- `ollama` + the `qwen3-vl:8b` model (~6 GB). macOS: `brew install ollama`. Linux: see the [ollama install script](https://ollama.com/install.sh). Then `ollama pull qwen3-vl:8b`.

If you don't install Ollama, Paideia's default engine (`codex-native`) reads page images through Codex CLI's built-in vision — the same vision your ChatGPT subscription already includes. No extra install, no second API key to manage.

### Sandbox note

If you run Paideia inside a sandboxed Codex session, local-engine and verification flows may trigger an approval prompt:

- `qwen3-vl` talks to the local Ollama HTTP server at `http://localhost:11434`
- live verification commands such as `codex exec --image ...` need to run outside the shell sandbox

If Codex asks for approval in either case, click **Approve** so the plugin can reach the local model or run the verification command. Otherwise the OCR/test call can fail even when Ollama and Codex are installed correctly.

### Install via Codex plugin marketplace

Run each line as a separate command inside Codex:

```
/plugins marketplace add https://github.com/TaewoooPark/PAIDEIA-codex.git
```

```
/plugins install paideia@paideia-marketplace
```

> The full `https://...` URL is deliberate — `owner/repo` shorthand can make the CLI try SSH first, which fails if you don't have a GitHub SSH key registered. HTTPS always works.

After install, 15 verbs become available under the `$paideia-` prefix, and the `paideia-mcp` stdio server auto-launches when you enter a course folder.

### Per-course bootstrap

Open Codex CLI inside the folder you want to use for this course, then type:

```
$paideia-init-course
```

This interactively:
1. Checks Python / poppler / tesseract deps and offers to install missing ones (ollama is only probed when you pick the `qwen3-vl` engine in step 3).
2. Asks for `COURSE_NAME`, `EXAM_DATE`, `EXAM_TYPE`, `WEAK_ZONES`.
3. Asks which OCR engine you want as the default: `codex-native` (pages read via Codex CLI's bundled vision — no extra API key, no extra install), `qwen3-vl` (local Ollama, pulls the 6 GB model in the background), or `tesseract` (lightest, lowest fidelity).
4. Creates the directory skeleton (`materials/`, `converted/`, `course-index/`, `quizzes/`, `mock/`, `twins/`, `chain/`, `derivations/`, `cheatsheet/`, `weakmap/`, `answers/converted/`, `errors/`).
5. Writes `.course-meta` (carries `OCR_ENGINE`, read by `$paideia-grade`) and a project-level `AGENTS.md`.
6. Runs `git init` if needed and merges the PAIDEIA-managed `.gitignore` rules so your prep is versioned from the first keystroke.

You can always override the OCR engine for a single grade call: `$paideia-grade --ocr=codex-native path/to/answer.pdf`.

---

## Course folder layout

After `$paideia-init-course`, your course folder looks like this:

```
my-course/
├── .course-meta                     # course name, exam date, OCR engine
├── AGENTS.md                        # project rules Codex reads every turn
├── .gitignore                       # hides raw answer PDFs, OCR scratch, optional PDF export
│
├── materials/                       # YOU DROP RAW FILES HERE (PDF or MD)
│   ├── lectures/                    # professor's notes, slide decks
│   ├── textbook/                    # textbook chapters
│   ├── homework/                    # HW problem sets
│   └── solutions/                   # HW solutions / worked examples
│
├── converted/                       # auto-generated markdown — do not edit
│   ├── lectures/                    # output of $paideia-ingest (vision-transcribed LaTeX)
│   ├── textbook/
│   ├── homework/
│   └── solutions/
│
├── course-index/                    # knowledge base — built by $paideia-analyze
│   ├── summary.md                   # topic tree (§1, §1.1, §2, …)
│   ├── patterns.md                  # recurring solution patterns, labeled P1, P2, …
│   └── coverage.md                  # HW ↔ § map with 🔥🔥 / 🔥 / 🟡 / ⚪ exam tiers
│
├── answers/                         # YOU DROP HAND-WRITTEN SCAN PDFs HERE
│   └── converted/                   # $paideia-grade writes OCR'd markdown here
│
├── errors/
│   └── log.md                       # append-only YAML error log (seed for /weakmap + /cheatsheet)
│
├── quizzes/                         # $paideia-quiz — each problem has a hidden _answers.md sibling
├── mock/                            # $paideia-mock — full mock exams (hidden _sol.md siblings)
├── twins/                           # $paideia-twin — same pattern, new surface
├── chain/                           # $paideia-chain — multi-pattern integration problems
├── derivations/                     # $paideia-derive — clean reference derivations
├── cheatsheet/                      # $paideia-cheatsheet — error-driven one-pager (+ optional PDF)
└── weakmap/                         # $paideia-weakmap — timestamped, append-only history
```

**Only two directories are yours to edit by hand:**
- `materials/` — drop source PDFs (or MDs) into the matching subfolder.
- `answers/` — drop hand-written scan PDFs into the root; the OCR'd markdown shows up under `answers/converted/`.

Everything else is produced by skills and should be treated as regenerable. Delete and rebuild whenever, `git log <dir>` to see your own progress over time, or point Obsidian at the whole folder as a vault.

---

## A reading tip: use Obsidian

Paideia writes everything as plain markdown with LaTeX math (`$...$`, `$$...$$`). You can read it in any editor, but **[Obsidian](https://obsidian.md)** is the natural choice:

- Renders `$...$` and `$$...$$` math via MathJax with zero configuration
- Backlinks let you click from `quizzes/q_<ts>.md` straight into the cited `converted/lectures/chN.md §K`
- The whole course folder is just a vault — point Obsidian at `~/courses/my-course`, and everything is a searchable graph
- Works entirely offline, free, local. Consistent with Paideia's philosophy: your notes, your disk, your tool

VS Code with a markdown-math extension works too. The terminal — even with a markdown preview — is bad for math; don't fight that.

---

## Full workflow — an example

### Phase 0 — once per course (15 minutes)

```bash
cp ~/textbooks/ch*.pdf      ~/courses/my-course/materials/textbook/
cp ~/lecture-notes/wk*.pdf  ~/courses/my-course/materials/lectures/
cp ~/hw/hw*.pdf             ~/courses/my-course/materials/homework/
cp ~/hw/hw*_sol.pdf         ~/courses/my-course/materials/solutions/
```

In Codex CLI:

```
$paideia-ingest                     # every PDF → vision pipeline (paideia-mcp parallel fan-out, LaTeX-faithful)
$paideia-analyze <weak-zone hints>  # build patterns + coverage + summary
$paideia-hwmap hot                  # surface 🔥🔥 exam-primary zones
```

### Phase 1 — diagnostic (40 minutes)

```
$paideia-quiz all 20                # broad diagnostic, 20 problems
# solve on paper (40 min), scan to answers/diagnostic.pdf
$paideia-grade                      # codex-native OCR (Codex reads the page images) + strategy grade
```

### Phase 2 — targeted drilling (bulk of your prep time)

```
$paideia-weakmap                    # priority-ranked weakness report
$paideia-blind hw3-p2               # strategy-only drill on a known problem
$paideia-twin hw3-p2                # variant with same pattern, new surface
$paideia-chain 3                    # multi-pattern integration problem
$paideia-quiz weakmap 5             # 5 problems targeting the latest weakmap
```

### Phase 3 — integration (~90 minutes)

```
$paideia-mock 90                    # full 90-min mock weighted by HW density
# solve on paper, scan, upload to answers/mock_<ts>.pdf
$paideia-grade                      # grade the mock
```

### Phase 4 — compression (60 minutes, night before exam)

```
$paideia-cheatsheet --pdf           # error-driven one-pager
$paideia-weakmap                    # review weak zones one more time
```

### Phase 5 — cool-down (10 minutes before exam)

```
$paideia-weakmap                    # top 3 only. Do not learn new things.
```

---

## Verbs (15 total)

| Verb | Purpose |
|------|---------|
| `$paideia-init-course` | Bootstrap a fresh course folder (dep check, skeleton, metadata prompt, background `ollama pull`) |
| `$paideia-ingest [--force]` | Every PDF in `materials/**` → markdown in `converted/**` via the `paideia-mcp` parallel vision pipeline |
| `$paideia-analyze [hints]` | Build `course-index/{summary,patterns,coverage}.md` |
| `$paideia-phase` | Show the current artifact-derived phase snapshot (`setup` → `cool`) |
| `$paideia-hwmap hot\|<§>` | Surface 🔥🔥 Exam-primary sections ranked by HW density |
| `$paideia-pattern <§\|Pk\|keyword>` | Show pattern cards from course-index |
| `$paideia-derive <target>` | Clean reference derivation to `derivations/<slug>.md` |
| `$paideia-quiz <topic\|§\|weakmap> [N]` | N practice problems, answers hidden in sibling `_answers.md` |
| `$paideia-blind <problem-id>` | Strategy-check drill on a known problem (no re-solve, describe approach) |
| `$paideia-twin <problem-id>` | Variant of a known problem — same pattern, new surface |
| `$paideia-chain <N>` | Multi-pattern integration problem combining N patterns |
| `$paideia-mock <minutes>` | Full mock exam, HW-density weighted |
| `$paideia-grade [--ocr=<engine>] [path]` | OCR answer PDF via the engine set in `.course-meta` (Codex-native vision / Qwen3-VL / Tesseract), strategy-grade, append `errors/log.md` |
| `$paideia-weakmap [concept]` | Priority-ranked weakness report saved to `weakmap/weakmap_<ts>.md` |
| `$paideia-cheatsheet [--pdf]` | Error-driven one-pager |

---

## Under the hood

### The MCP server: `paideia-mcp`

The Claude edition drove parallel vision ingest by spawning one `general-purpose` subagent per PDF. Codex subagents exist but are heavier per-task, and Codex's `view_image` tool requires explicit user consent for each image — neither is a good fit for a 200-page textbook ingest. The Codex edition therefore moves the heavy work into a **bundled stdio MCP server**, `paideia-mcp`, that Codex spawns automatically the first time a skill calls into it. It exposes four tools:

| Tool | What it does |
|------|--------------|
| `ingest_pdfs` | Render every `materials/**/*.pdf` to PNGs, resize to ≤1800 px on the long edge, then either (a) hand the page paths back to the calling skill when `engine=codex-native` (Codex reads them with its bundled vision), or (b) OCR in-process and write LaTeX markdown to `converted/**` when `engine=qwen3-vl` / `tesseract`. Deterministic `ProcessPoolExecutor` fan-out, resumable per PDF. |
| `grade_pdf` | Same dual behavior for a single hand-written answer PDF: `codex-native` rasterizes + returns page paths; `qwen3-vl` / `tesseract` run OCR in-process and write `answers/converted/<stem>.md` with a confidence tier. |
| `build_course_index` | Read `converted/**`, write a machine-generated baseline `course-index/{summary,patterns,coverage}.md`, and return the inventory the analyze skill can refine. |
| `course_phase` | Artifact-derived phase (setup → diag → drill → mock → cram → cool). Returns `{phase, days_until_exam, top_miss_pattern}`. Used by `$paideia-phase` and any skill that needs to know where the user is in the cycle. |

Skills stay thin (~40–80 lines of orchestration): parse arguments, call the right MCP tool, summarize the result for the user. Raw page images never enter Codex's context.

### Ingest pipeline: vision for every PDF

`$paideia-ingest` routes every PDF in `materials/**` through the same vision pipeline. `pdfplumber` was tried first as a fast path for prose-heavy material (textbook, HW) and proved unreliable: even pages that *look* like plain prose silently word-salad as soon as they mix equations, figures, multi-column layouts, or margin notes. Rather than maintain a per-category heuristic with fallbacks we'd have to retune per course, we route everything uniformly.

| Source | Method |
|---|---|
| `materials/**/*.pdf` | Vision pipeline (MCP parallel fan-out, LaTeX-faithful) |
| `materials/**/*.md` | Copy-through with provenance header |

How the pipeline runs: every page is rendered to PNG at `dpi=160`; every PNG is resized to ≤1800 px on the long edge before any OCR call fires; then `paideia-mcp.ingest_pdfs` dispatches to the selected engine, with one worker process per PDF and an `ThreadPoolExecutor` inside each worker for I/O-bound OCR calls. Output like `$$\hat H = -\frac{\hbar^2}{2m}\partial_x^2 + V(x)$$` instead of `ℏ ∂ p2 ℏ 2 ∂ 2 p ̂`.

### Hand-writing OCR: three engines, you pick

The user does not type math into chat. They solve on paper, scan to PDF, drop the PDF into `answers/`, and run `$paideia-grade`. The plugin converts the scan to markdown via one of three engines, chosen per course (via `OCR_ENGINE` in `.course-meta`) and overridable per call (via `$paideia-grade --ocr=<engine>`):

| Engine | Default? | How it runs | When to pick it |
|---|---|---|---|
| `codex-native` | **Yes** | `paideia-mcp.grade_pdf` renders each page to PNG under `answers/.paideia-cache/<stem>/`, then hands the page paths back so Codex CLI can read them with its bundled vision — the same vision your ChatGPT Plus/Pro/Business subscription already includes. No `OPENAI_API_KEY` and no separate API billing. | The out-of-the-box path. Strong on Korean + LaTeX + hand-written math; no local model-load stall; no double-billing. |
| `qwen3-vl` | opt-in | Local Qwen3-VL 8B via Ollama's HTTP API, with automatic tesseract fallback. | You want the page images to never leave the machine. Requires `ollama pull qwen3-vl:8b` once (~6 GB). |
| `tesseract` | opt-in | `pytesseract` with whichever of `eng` / `kor` traineddata is installed (auto-detected; falls back to the single available language if the other is missing). | Fastest and lightest; acceptable for typed scans; poor on hand-writing. |

Each engine writes `answers/converted/<stem>.md` with a `<!-- source: ... -->` / `<!-- tier: ... -->` header comment so `$paideia-grade` can caveat low-confidence OCR.

Default choice (`codex-native`) is deliberately the path of least friction and least spend: if you're running Codex CLI you're already paying for the ChatGPT subscription that includes vision, so the default engine neither installs extra software nor charges you twice. The `qwen3-vl` engine exists for users who want a hard privacy boundary on the page images themselves, and `tesseract` exists as a reliable floor when nothing else is available.

### Strategy-based grading, not line-by-line

OCR noise in hand-written math makes strict algebraic grading useless — a single misread `∫` vs `∑` would cascade. More importantly, **pattern recognition is the actual exam bottleneck**, not arithmetic. The grader therefore checks three things on each problem:

1. **Pattern** — did the student pick the right Pk from `course-index/patterns.md`?
2. **Variables** — did they identify the right substitution / basis / index / contour?
3. **End-form** — does their final expression have the right shape (dimensions, asymptotics, structure)?

Errors get logged as YAML to `errors/log.md` with a typed classification (`pattern-missed | wrong-variable | wrong-end-form | algebraic | sign | definition`). This log is the seed for `$paideia-weakmap` and the *only* input to `$paideia-cheatsheet --pdf`.

The schema is canonical across every skill that appends here — `$paideia-grade`, `$paideia-blind`, and any future drill — with exactly the keys `problem_id · pattern · error_type · summary · source · date`. The single source of truth is `plugins/paideia/skills/paideia-grade/SKILL.md` §6; downstream readers (`paideia-mcp.course_phase`, `$paideia-phase`, `$paideia-weakmap`) pattern-match on `pattern:` and `source:`, and the `source:` field is what lets phase detection distinguish a mock-grade entry from a homework-grade entry. Any schema drift silently hides entries from the weakmap, so new drills must use the canonical keys.

After `$paideia-grade` succeeds, the original hand-written PDF is moved from `answers/<stem>.pdf` into `answers/_archive/<stem>_<ts>.pdf` so the next invocation's "most recently modified in `answers/`" resolver stops re-picking the same stale file when you upload a newer scan. The converted markdown stays under `answers/converted/` and is version-controlled; only the bulky scan itself is archived (and gitignored via `answers/**/*.pdf`).

### Patterns extracted from *your* solutions

`$paideia-analyze` doesn't ship a generic "calculus moves" list. It reads your course's actual solution manual, extracts recurring solution patterns, and labels them P1, P2, ... with worked instances that cite your own `converted/solutions/` files. The patterns are *your course's idioms*, not a textbook's. For a complex analysis course, P3 might be "closed contour + Jordan's lemma + residue at essential singularity." For a linear systems course, P3 might be "partial fractions + inverse Laplace with complex poles." Every discipline has its own moves; only the course itself reveals them.

### Append-only history

`weakmap/` never overwrites. Every `$paideia-weakmap` invocation produces `weakmap/weakmap_<ISO-timestamp>.md`. You can `git log weakmap/` and see exactly which weaknesses collapsed first, which ones persisted, which new ones emerged after the diagnostic mock. This is "`git diff` your own understanding over time" in practice.

### Phase detection

Codex doesn't expose a persistent statusline slot the way Claude Code does, so the neon one-liner that the Claude edition paints there is not ported. The underlying phase detection, however, is exposed as its own verb:

```
$paideia-phase
```

Prints `setup · diag · drill · mock · cram · cool` along with `D-<days-to-exam>` and the top-miss pattern from the latest weakmap. The phase is **activity-based**: creating an empty `patterns.md` or dropping a seeded `mock/<name>.md` does not advance it. The student must have actually graded something — an `errors/log.md` entry with a canonical `pattern:` key — before the phase moves past `diag`.

- `setup` — `course-index/patterns.md` doesn't exist yet → run `$paideia-ingest` + `$paideia-analyze`
- `diag` — patterns exist, but `errors/log.md` has no graded entries yet → run `$paideia-quiz all 20` and grade it
- `drill` — at least one graded entry lives in `errors/log.md` → cycle `$paideia-blind` · `$paideia-twin` · `$paideia-quiz weakmap`
- `mock` — a mock-sourced entry (any `errors/log.md` row whose `source:` contains `mock`) has been graded → compress with `$paideia-cheatsheet --pdf`
- `cram` — `cheatsheet/final.{md,pdf}` exists → taper, re-read the weakmap, stop learning new things
- `cool` — `D-0` overrides everything (exam is today)

Why activity-based rather than file-existence-based: an artifact that was never acted on is not the same signal as one the student produced. Treating `quizzes/*.md` (a problem set) as evidence of drilling conflates "a file exists" with "the student has actually drilled on it." Requiring a graded entry in `errors/log.md` ensures the phase reflects what the user did, not what the filesystem declares.

---

## What ships

```
PAIDEIA-codex/
├── .agents/plugins/marketplace.json     # marketplace manifest (Codex)
├── LICENSE                              # MIT
├── README.md                            # this file
├── README.ko.md                         # Korean mirror
└── plugins/paideia/
    ├── .codex-plugin/plugin.json        # plugin manifest (name, version, author)
    ├── .mcp.json                        # spawn config for paideia-mcp
    ├── README.md                        # quick-reference card
    ├── paideia-mcp/                     # bundled stdio MCP server
    │   ├── pyproject.toml
    │   ├── README.md
    │   └── paideia_mcp/
    │       ├── server.py                # stdio entrypoint, tool registration
    │       ├── ingest.py                # ingest_pdfs tool
    │       ├── grade.py                 # grade_pdf tool
    │       ├── analyze.py               # build_course_index tool
    │       ├── phase.py                 # course_phase tool
    │       └── ocr/
    │           ├── qwen3vl.py           # local Ollama Qwen3-VL 8B
    │           └── tesseract.py         # pytesseract eng / kor (auto-detected)
    └── skills/                          # 15 verb-skills (paideia-ingest, paideia-grade, paideia-phase, ...)
        ├── paideia-init-course/
        │   ├── SKILL.md
        │   ├── scripts/bootstrap.py
        │   └── assets/AGENTS.md.template
        ├── paideia-ingest/SKILL.md
        ├── paideia-grade/SKILL.md
        ├── paideia-analyze/SKILL.md
        ├── paideia-hwmap/SKILL.md
        ├── paideia-pattern/SKILL.md
        ├── paideia-derive/SKILL.md
        ├── paideia-quiz/SKILL.md
        ├── paideia-blind/SKILL.md
        ├── paideia-twin/SKILL.md
        ├── paideia-chain/SKILL.md
        ├── paideia-mock/SKILL.md
        ├── paideia-weakmap/SKILL.md
        └── paideia-cheatsheet/SKILL.md
```

---

## Design convictions

1. **The terminal is bad for math.** Codex produces markdown files; you read them (ideally in Obsidian).
2. **Typing solutions is slow and error-prone.** You solve on paper, scan, and the plugin OCRs (locally, or via Codex CLI's bundled vision — no extra billing for ChatGPT subscribers).
3. **OCR noise is inevitable.** So grading is strategy-based (pattern / variables / end-form), not line-by-line algebra. This is what the actual exam grader is evaluating anyway.
4. **Patterns must be extracted from *your* course's solutions** — not from a generic list. Every discipline has its own idioms; only the course itself reveals them.
5. **Your errors are the most valuable study signal** — more than the textbook, more than the lectures. The cheatsheet is generated from `errors/log.md`, not from the syllabus.
6. **HW density tells you the exam.** Your time is finite; spend it where the points are.
7. **Everything is yours to edit.** Patterns, weakmaps, cheatsheets, the error log — all plain markdown/YAML in your own git history. Disagree with `P3`? Rewrite it, and the next drill uses your edit. Fork a course folder from last semester into a new one and edit deltas. The plugin is a scaffold; the study graph is yours.
8. **Heavy pipelines live in MCP, not in skill bodies.** The parallel vision ingest, multi-engine OCR dispatch, pattern extraction, and phase detection are all implemented in `paideia-mcp`. Skills just orchestrate. This keeps skill bodies short enough to audit by hand and keeps Codex's context free of raw page images.

---

## FAQ

**Does this work for non-math courses?**
It's built around problem-pattern extraction, so it shines in quantitative disciplines: math, physics, EE, CS-theory, ML-theory, statistics, engineering. For history or literature it would still ingest and produce summaries, but the drill skills assume problems have solution patterns.

**Korean and English mixed materials?**
Yes. Ingestion and OCR are configured for `eng+kor`. Patterns and grading responses honor the language mix of your source materials.

**How is this different from just asking ChatGPT / Claude / Gemini to help me study?**
Per-course persistence. An LLM chat has no memory of the pattern you missed on HW2 two weeks ago, no ranking of which sections your professor actually emphasizes, no notion of "your typical error type." Paideia writes all of that to markdown files on your disk. A `$paideia-weakmap` today is informed by every `$paideia-grade` since the course began, because `errors/log.md` is append-only. A generic chat session, however smart, is a blank slate every time you open it.

**Can I edit the patterns / cheatsheet / weakmap if I disagree?**
Yes. That's the whole point of keeping them as plain markdown. If `P3` feels wrong, open `course-index/patterns.md` and rewrite it — subsequent drills will use your edit. If the cheatsheet emphasizes the wrong thing, trim it. The plugin is a scaffold; the study graph is yours to shape.

**Do I need Ollama / Qwen3-VL to use this?**
No. The default engine is `codex-native`, which reads page images via Codex CLI's built-in vision — the same vision your ChatGPT Plus/Pro/Business/Edu/Enterprise subscription already includes. No separate API key, no additional install. Ollama + `qwen3-vl:8b` is an opt-in path for users who want the page images to stay on their machine entirely. `tesseract` is a third option for minimal-install setups or typed scans.

**Do I need a separate `OPENAI_API_KEY`?**
No. Codex CLI authenticates via "Sign in with ChatGPT" and bundles vision as part of the subscription. Paideia's default engine just hands page images to Codex — it never makes a separate paid API call on your behalf. (The old `openai-vision` engine, which did call the Responses API with a second key, has been removed to avoid double-billing Codex users.)

**What if my machine can't run `qwen3-vl:8b` even though I picked Qwen3-VL?**
The MCP server's OCR dispatcher automatically falls back to tesseract on any Ollama failure. You can also just set `OCR_ENGINE: codex-native` in `.course-meta` (or pass `--ocr=codex-native`) and skip Ollama entirely.

**Can I reuse the plugin across multiple courses?**
Yes — each course lives in its own folder with its own `.course-meta`, `course-index/`, `errors/log.md`, and `weakmap/`. Nothing is shared or polluted across courses. Open Codex CLI inside whichever course folder you're working on.

**Can I trust an LLM to grade my work?**
Grading is strategy-based (pattern match, not algebra), the grader cites the pattern from `course-index/patterns.md`, and every grade writes a YAML entry you can audit in `errors/log.md`. If a grade is wrong, fix the YAML entry — the next `$paideia-weakmap` reflects the correction.

**Is my data private?**
Your PDFs, markdown, errors, and weakmaps all live in your local course folder — nothing is uploaded to any third-party service by the plugin itself. The only network traffic depends on the OCR engine you pick: with `codex-native` (default), page images are read by Codex CLI's own vision (so they travel over the same secure channel Codex already uses for every other turn — nothing new); with `qwen3-vl`, nothing leaves the machine after the one-time model download; with `tesseract`, nothing leaves the machine ever.

**Can I share artifacts with the Claude Code edition?**
Yes. The on-disk layout is byte-compatible. A course folder initialized by the Claude edition opens cleanly in the Codex edition (you just need an `AGENTS.md` alongside the existing `CLAUDE.md`, which `$paideia-init-course` will offer to generate), and vice versa. Errors logged by one edition feed the weakmap of the other without conversion.

---

## Connect

<p align="center">
  <a href="https://github.com/TaewoooPark"><img src="https://img.shields.io/badge/-GitHub-181717?style=for-the-badge&logo=github&logoColor=white&cacheSeconds=3600" alt="GitHub"></a>
  <a href="https://x.com/theoverstrcture"><img src="https://img.shields.io/badge/-X-000000?style=for-the-badge&logo=x&logoColor=white&cacheSeconds=3600" alt="X (Twitter)"></a>
  <a href="https://www.linkedin.com/in/taewoo-park-427a05352"><img src="https://img.shields.io/badge/-LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white&cacheSeconds=3600" alt="LinkedIn"></a>
  <a href="https://www.instagram.com/t.wo0_x/"><img src="https://img.shields.io/badge/-Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white&cacheSeconds=3600" alt="Instagram"></a>
  <a href="mailto:ptw151125@kaist.ac.kr"><img src="https://img.shields.io/badge/-Email-D14836?style=for-the-badge&logo=gmail&logoColor=white&cacheSeconds=3600" alt="Email"></a>
</p>

---

## License

MIT. Use freely. Fork and modify for your own courses — the point of the plugin is that the study graph it builds is yours to shape, not a fixed product you have to live with.

---

<p align="center">
  <em>Generic curricula teach the average student. Παιδεία — formation, one student at a time.</em>
</p>
