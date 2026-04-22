<h1 align="center">ΠΑΙΔΕΙΑ · Paideia <sub>(Codex edition)</sub></h1>

<p align="center">
  <strong>당신의 과목, 당신의 패턴, 당신의 오답, 당신의 치트시트.</strong><br>
  <em>당신의 자료에서 출발해 한 과목에 영속적으로 머무는 학습 그래프를 만드는 OpenAI Codex CLI 플러그인입니다 — 모든 산출물이 일반 실러버스가 아니라 당신의 손끝에서 빚어집니다.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/github/license/TaewoooPark/PAIDEIA-codex?style=flat-square&labelColor=000000&color=333333&cacheSeconds=3600" alt="라이선스">
  <img src="https://img.shields.io/github/stars/TaewoooPark/PAIDEIA-codex?style=flat-square&logo=github&logoColor=white&labelColor=000000&color=333333&cacheSeconds=3600" alt="GitHub 스타 수">
  <img src="https://img.shields.io/github/last-commit/TaewoooPark/PAIDEIA-codex?style=flat-square&labelColor=000000&color=333333&cacheSeconds=3600" alt="최근 커밋">
  <img src="https://img.shields.io/github/languages/top/TaewoooPark/PAIDEIA-codex?style=flat-square&labelColor=000000&color=333333&cacheSeconds=3600" alt="주요 언어">
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
  <a href="./README.md">English README</a>
</p>

<p align="center">
  <sub>같은 플러그인의 Claude Code 에디션: <a href="https://github.com/TaewoooPark/PAIDEIA">TaewoooPark/PAIDEIA</a></sub>
</p>

---

<p align="center">
  <em>일반적인 학습 도구는 평균적인 실러버스를 가르칩니다. Paideia는 <strong>당신의</strong> 실러버스를 가르칩니다 —<br>
  당신의 교수님 강의노트, 당신의 숙제 경향, 당신의 필기, 당신의 오답에서 출발해서요. 모든 산출물은 당신이 직접 편집할 수 있는 마크다운 파일입니다.</em>
</p>

---

## Paideia라는 이름에 대하여

고대 그리스에서 **Παιδεία(파이데이아)**는 수동적인 학생에게 사실을 주입하는 일이 아니었습니다. 그것은 원전과의 구조화된 만남, 스승 아래에서의 연습, 그리고 피드백을 더 깊은 수정으로 되돌려 보내는 성찰적 대화를 통한 — 한 인간을 평생에 걸쳐 형성해 가는 일이었습니다.

이 플러그인은 그 순환을 **수학·물리·공학 과목의 시험 준비**라는 구체적이고 한정된 문제에 맞추어 구현합니다.

```
  ingest ──▶ analyze ──▶ drill ──▶ grade ──▶ weakmap ──▶ cheatsheet
     ▲                                                        │
     └────────────────── feedback loop ───────────────────────┘
```

각 단계는 당신의 코스 폴더에 영원히 남는 마크다운 파일 하나씩을 남깁니다. 휘발되는 것은 없고, API 뒤에 숨는 것도 없습니다. 다음 자금 한파가 닥쳐도 멈추는 것이 없습니다.

---

## 왜 Codex 에디션이 필요한가

> **2026-04-21 정책 안내.** 2026년 4월 21일(미국 시간), Anthropic이 소비자 요금제 약관을 개정하면서 **Pro 티어의 Claude Code 접근 권한을 폐지**했습니다 — 이제 Claude Code는 Max 요금제 혹은 API로만 쓰실 수 있습니다. PAIDEIA 원판을 Pro 구독으로 돌리시던 학생이 적지 않았고, 이분들은 하루아침에 접근 경로를 잃으셨습니다. 어느 러너를 감당하실 수 있든 PAIDEIA가 그대로 동작하도록, 같은 라이선스·같은 디스크 레이아웃을 유지한 채 플러그인을 OpenAI Codex CLI로 이식했습니다. 두 에디션 모두 함께 관리되니, 아직 구독 중이신 agentic CLI 쪽을 고르시면 됩니다.

PAIDEIA는 원래 Claude Code 플러그인으로 태어났습니다. 핵심 로직 — 병렬 비전 인제스트, 전략 기반 채점, *당신*의 풀이집에서 패턴을 추출하기 — 은 사실 Claude에 묶여 있던 적이 없었습니다. 대신 *어떤* agentic CLI든 "skills, subagents, plugins, 그리고 쓸만한 비전 경로"라는 네 가지 기반을 갖추기만 하면 얹을 수 있는 구조였습니다. OpenAI Codex CLI는 2026년에 그 기반(skills, subagents, MCP, plugins, `AGENTS.md`)을 모두 갖추게 되었고, 덕분에 이식은 학습 그래프를 새로 설계하는 일이 아니라 **기존 로직을 Codex의 기본 요소 위에 다시 얹는 일**로 마무리되었습니다.

디스크 위 학습 그래프는 **바이트 단위로 동일합니다**. `course-index/patterns.md`, `errors/log.md`, `weakmap/weakmap_<ts>.md`, `cheatsheet/final.md` — Claude 에디션이 쓰는 모든 산출물을 이 에디션도 같은 포맷으로 씁니다. Claude 에디션으로 만드신 코스 폴더를 그대로 이 에디션에서 여셔도(또는 그 반대도) 마찰 없이 이어 가실 수 있습니다.

### 무엇이 바뀌었는가

| 개념 | Claude Code 에디션 | Codex 에디션 |
|---|---|---|
| 명령 문법 | `/paideia:ingest` | `$paideia-ingest` |
| 프로젝트 컨텍스트 파일 | `CLAUDE.md` | `AGENTS.md` |
| 플러그인 루트 변수 | `${CLAUDE_PLUGIN_ROOT}` | `${CODEX_PLUGIN_ROOT}` |
| 무거운 파이프라인이 사는 곳 | PDF별 `general-purpose` 서브에이전트 | 번들 `paideia-mcp` stdio MCP 서버 |
| 기본 OCR | Claude 네이티브 비전(추가 설치 없음) | OpenAI Vision — Responses API (`OPENAI_API_KEY` 필요) |
| 로컬 OCR | `ollama` + `qwen3-vl:8b` | 동일 (`qwen3-vl`) |
| Tesseract 최후 보루 | 있음 | 있음 |
| Statusline 위젯 | `paideia · COURSE · D-N · phase · P<k>` | *(미포팅 — Codex에는 지속 statusline 슬롯이 없습니다. 단계는 `$paideia-phase`로 조회)* |

그 외의 것들 — 디렉토리 레이아웃, 패턴 추출 로직, 전략 채점, 숙제 밀도 기반 출제 티어링, `weakmap/`의 append-only 이력, 오답 기반 치트시트 — 은 모두 같습니다.

---

## 일반적인 학습 도구가 하지 못하는 것

대부분의 학습 도구는 *당신*의 과목, *당신*의 교수님, *당신*의 실수에 맞춰 개인화되지 못합니다 — 이들이 파는 상품 자체가 "일반적인 커리큘럼"이기 때문입니다.

- **Coursera, edX, Khan Academy** — 고정된 커리큘럼. 당신 교수님이 실제로 어디를 강조하시는지 알 길이 없습니다.
- **Quizlet, Anki, Brainscape** — 카드 하나하나를 당신이 직접 큐레이션해야 하고, 당신 과목의 해답지에서 패턴을 뽑아 주지 않습니다.
- **Chegg, Course Hero** — 범용 해답지. 당신 과목의 반복되는 관용구(idiom) 중심으로 정리되어 있지 않습니다.
- **Brilliant, Duolingo Max, Khanmigo** — 범용 문제집. 당신이 지난달 HW2에서 뭘 틀렸는지 알지 못합니다.
- **ChatGPT Study Mode, Gemini "Deep Study", NotebookLM** — 과목별 영속 상태가 없습니다. 세션을 새로 열 때마다 콜드 스타트이고, 지난주의 실수는 이번 주 드릴에 반영되지 않습니다 — 당신이 매번 다시 업로드하고 다시 설명하지 않는 한요.

이들 중 어느 것도 당신 앞에 놓인 그 특정 자료를 기반으로 이해를 *형성*하지 못합니다. 모든 학생에게 같은 답을 내어 줄 뿐이지요. Paideia는 반대 방향입니다: 모든 산출물이 *당신 폴더*의 강의노트·교재 챕터·숙제·풀이·필기 시도에서 파생되고, 당신이 직접 편집할 수 있는 평범한 마크다운으로 영구히 누적됩니다.

| 축 | Paideia | 일반적인 교육 SaaS / LLM 챗 |
|----|---------|------------------------------|
| 풀이 패턴 (`P1..Pk`) | *당신 과목*의 해답지에서 직접 추출하고, 당신의 파일을 인용합니다 | 범용 교과서 목록, 혹은 없음 |
| 드릴 우선순위 | *당신 교수님*의 숙제 강조도(HW 밀도 = 시험 티어)로 가중됩니다 | 고정 커리큘럼 또는 당신의 감 |
| 치트시트 | *당신*의 `errors/log.md` — 당신이 실제로 틀린 것으로 구성됩니다 | 실러버스 보일러플레이트 |
| 세션 간 과목 상태 | 마크다운 + YAML로 영속, 작업할수록 축적됩니다 | 대화 초기화, 이력은 유료 티어 |
| 산출물이 마음에 안 들 때 | 에디터로 `.md`를 열어 수정, 저장 | 읽기 전용 UI |
| 지난 학기 준비를 다음 학기로 | 과목 폴더를 fork해서 차이만 수정 | 처음부터 다시 |
| 자신의 이해에 대한 버전 관리 | 어떤 산출물이든 `git log` / `git diff` | 외부에 노출되지 않음 |
| 산출물이 있는 곳 | 당신의 디스크, 텍스트 파일로 | 원격 DB, 유료 티어에서만 내보내기 |

플러그인은 유료 API를 호출하는 Codex CLI로 무거운 일을 처리하지만, 그 결과물은 전부 당신 디스크 위의 평범한 마크다운입니다. 나중에 다른 모델 러너로 옮기시거나 OpenAI 구독을 잠시 중단하셔도, course-index·patterns·오답 로그·weakmap·치트시트는 여전히 당신이 열어 읽고, 수정하고, diff할 수 있습니다. 플러그인은 뼈대이고, 학습 그래프는 당신의 것입니다.

기본 설정에서 OCR은 당신의 `OPENAI_API_KEY`를 그대로 쓰는 OpenAI Vision(Responses API)으로 처리됩니다. 필기 PDF를 기기 밖으로 내보내고 싶지 않으시다면 `ollama pull qwen3-vl:8b`로 약 6 GB 모델 가중치를 한 번 내려받으면, 그 뒤 모든 OCR이 로컬 Qwen3-VL 추론으로 전환됩니다. 어느 쪽을 고르시든 이후의 산출물(패턴, 커버리지, weakmap, 치트시트, 오답 로그)은 전부 당신 디스크 위의 평범한 마크다운입니다.

---

## 핵심 원리: 숙제 밀도가 곧 출제 확률입니다

대부분의 "똑똑하게 공부하는 법"은 사각지대부터 공략하라고 말합니다. 그러나 이 조언은 **방향이 반대입니다**. 교수님은 이미 숙제를 배정하는 것으로 시험 포인트의 위치를 알려 주셨습니다. 숙제가 몰린 절은 🔥🔥 Exam-primary이고, 숙제가 전혀 없는 절은 ⚪ Low-risk일 뿐 "숨겨진 함정"이 아닙니다. 교수님의 침묵은 그 주제가 시험 범위 바깥이라는 가장 강력한 신호입니다.

Paideia의 우선순위는 이 원리를 명시적으로 반영합니다. 모든 드릴 명령이 기본값으로 이 티어링을 따릅니다.

| 티어 | 해당 절의 숙제 수 | 처리 방식 | 모의고사 점수 비중 |
|------|---------------------|-----------|--------------------|
| 🔥🔥 Exam-primary | 3+ | 가장 먼저, 가장 강도 높게 드릴 | ≥70% |
| 🔥 Exam-likely | 2 | 그 다음 드릴 | ~25% |
| 🟡 Exam-possible | 1 | 가볍게 복습 | ≤5% |
| ⚪ Low-risk | 0 | 참조·독서 용도만 | 0 |

`$paideia-quiz all`, `$paideia-mock`, `$paideia-hwmap hot` 모두 이 가중치를 존중합니다. 만약 사용자가 ⚪ 절을 굳이 드릴하겠다고 요청하면, 플러그인은 한 번은 따라 주지만 출제 확률이 낮다는 경고를 덧붙입니다. 제한된 시간은 상상 속 함정보다 훨씬 가치 있기 때문입니다.

---

## 형성 사이클, 단계별 해설

| 단계 | 하는 일 | 명령 | 산출물 |
|------|---------------|------|--------|
| **대면 (Encounter)** | 교수님이 보낸 신호를 읽습니다 | `$paideia-ingest` | `converted/**/*.md` — 모든 강의노트·교재 챕터·숙제·풀이를 깨끗한 마크다운으로 |
| **구조화 (Structure)** | 과목 고유의 문법을 추출합니다 | `$paideia-analyze` | `course-index/{summary,patterns,coverage}.md` — 주제 트리, 반복되는 풀이 패턴 (P1..Pk), 숙제 밀도 기반 출제 티어 |
| **연습 (Practice)** | 교수님이 실제로 시험하는 것에 가중치를 두어 능동 회상을 수행합니다 | `$paideia-quiz`, `$paideia-twin`, `$paideia-blind`, `$paideia-chain`, `$paideia-mock` | `quizzes/`, `twins/`, `chain/`, `mock/` — 종이에 풀 문제들 |
| **성찰 (Reflection)** | 손으로 쓴 답안이 채점 결과로 바뀝니다 | `$paideia-grade` | `answers/converted/<name>.md` + `errors/log.md` — OpenAI Vision(기본) / Qwen3-VL / Tesseract 중 선택한 엔진으로 OCR, 전략 기반 채점 |
| **진단 (Diagnosis)** | 오류를 우선순위가 매겨진 약점 리포트로 압축합니다 | `$paideia-weakmap` | `weakmap/weakmap_<ts>.md` — append-only 이력 |
| **증류 (Distillation)** | 오류에서 출발한 한 장짜리 인쇄물을 만듭니다 | `$paideia-cheatsheet`, `$paideia-derive`, `$paideia-pattern` | `cheatsheet/final.md`, `derivations/<slug>.md` — 실제로 필요한 것만 참조 |

보조 명령: `$paideia-hwmap`은 숙제 밀도 기반 출제 확률을 띄워 줍니다. `$paideia-init-course`는 새 코스 폴더를 부트스트랩합니다. `$paideia-phase`는 폴더가 현재 사이클의 어느 단계에 있는지를 알려 줍니다.

---

## 설치

### 사전 요구사항

**필수**

- [OpenAI Codex CLI](https://github.com/openai/codex) (`codex`가 `PATH`에 잡혀 있어야 합니다)
- 쉘에 `OPENAI_API_KEY`가 export 되어 있어야 합니다 (기본 OCR 엔진이 이 값을 씁니다)
- Python 3.10+ (번들 MCP 서버가 파이썬으로 작성되어 있습니다)
- Unix 계열 쉘 (`bash` / `zsh`). 부트스트랩 스킬이 heredoc·`mkdir -p`·`mktemp`·서브쉘 백그라운드 실행을 쓰기 때문에, Windows 네이티브 `cmd` / PowerShell은 현재 지원하지 않습니다.
- **macOS**: `brew install poppler tesseract tesseract-lang`
- **Linux (Debian/Ubuntu)**: `apt-get install poppler-utils tesseract-ocr tesseract-ocr-kor`
- **Windows**: [WSL2](https://learn.microsoft.com/windows/wsl/install)를 설치하신 뒤, WSL 쉘 안에서 위의 Linux 경로를 그대로 따라 주세요.

**선택 — `--ocr=qwen3-vl` 모드를 쓰고 싶을 때만 (페이지 이미지가 기기 밖으로 전혀 나가지 않습니다)**

- `ollama` + `qwen3-vl:8b` 모델 (~6 GB). macOS: `brew install ollama`. Linux: [ollama 설치 스크립트](https://ollama.com/install.sh). 이후 `ollama pull qwen3-vl:8b`.

Ollama를 설치하지 않으셔도 괜찮습니다. 기본 OCR 엔진은 Responses API로 접근하는 OpenAI Vision이라, Codex CLI가 이미 필요로 하는 `OPENAI_API_KEY` 외에는 별도로 설치할 것이 없습니다.

### Codex 플러그인 마켓플레이스로 설치

Codex 안에서 **각 줄을 한 번에 하나씩** 실행해 주세요.

```
/plugins marketplace add https://github.com/TaewoooPark/PAIDEIA-codex.git
```

```
/plugins install paideia@paideia-marketplace
```

> URL을 전부 적는 이유가 있습니다 — `owner/repo` 짧은 형태를 쓰면 CLI가 SSH를 먼저 시도하기 때문에, GitHub에 SSH 키가 등록돼 있지 않은 환경에서는 실패합니다. HTTPS URL을 쓰면 언제나 동작합니다.

설치가 끝나면 14개의 동사가 `$paideia-` 접두어로 제공되고, 코스 폴더에 들어가시는 순간 `paideia-mcp` stdio 서버가 자동으로 스폰됩니다.

### 코스별 부트스트랩

해당 코스용으로 쓰실 폴더 안에서 Codex CLI를 여신 뒤 다음을 실행해 주세요.

```
$paideia-init-course
```

이 스킬은 대화식으로 다음을 수행합니다.
1. Python / poppler / tesseract 의존성을 확인하고, 누락된 항목은 설치를 제안합니다 (ollama는 아래 3단계에서 `qwen3-vl` 엔진을 선택하신 경우에만 점검합니다)
2. `COURSE_NAME`, `EXAM_DATE`, `EXAM_TYPE`, `WEAK_ZONES` 값을 입력받습니다
3. 기본 OCR 엔진을 고릅니다 — `openai-vision` (당신의 `OPENAI_API_KEY` 사용) / `qwen3-vl` (로컬 Ollama, 약 6 GB 모델을 백그라운드에서 받음) / `tesseract` (가장 가볍고 빠름, 필기 정확도는 낮음)
4. 디렉토리 골격을 생성합니다 (`materials/`, `converted/`, `course-index/`, `quizzes/`, `mock/`, `twins/`, `chain/`, `derivations/`, `cheatsheet/`, `weakmap/`, `answers/converted/`, `errors/`)
5. `.course-meta`(`OCR_ENGINE`을 담고 있으며 `$paideia-grade`가 이 값을 읽습니다)와 프로젝트 수준 `AGENTS.md`를 작성합니다
6. `git init`을 수행해 첫 키 입력부터 준비 과정이 버전 관리되도록 합니다

개별 채점 호출에서는 엔진을 그때그때 덮어쓰실 수 있습니다. 예: `$paideia-grade --ocr=openai-vision path/to/answer.pdf`.

---

## 코스 폴더 구조

`$paideia-init-course`를 실행하고 나면 코스 폴더가 다음과 같이 구성됩니다.

```
my-course/
├── .course-meta                     # 코스명, 시험일, OCR 엔진 설정
├── AGENTS.md                        # Codex가 매 턴 읽는 프로젝트 규칙
├── .gitignore                       # 답안 PDF, 정답 키, OCR 임시물 제외
│
├── materials/                       # 직접 원본을 넣는 곳 (PDF 또는 MD)
│   ├── lectures/                    # 강의노트 / 슬라이드
│   ├── textbook/                    # 교재 챕터
│   ├── homework/                    # 과제 문제지
│   └── solutions/                   # 과제 풀이 / 예제 풀이
│
├── converted/                       # 자동 생성된 마크다운 — 직접 수정하지 마세요
│   ├── lectures/                    # $paideia-ingest의 산출물 (비전으로 전사한 LaTeX)
│   ├── textbook/
│   ├── homework/
│   └── solutions/
│
├── course-index/                    # 지식 베이스 — $paideia-analyze가 생성
│   ├── summary.md                   # 주제 트리 (§1, §1.1, §2, …)
│   ├── patterns.md                  # 반복되는 풀이 패턴, P1, P2, … 라벨
│   └── coverage.md                  # HW ↔ § 매핑 + 🔥🔥 / 🔥 / 🟡 / ⚪ 시험 티어
│
├── answers/                         # 직접 필기 스캔 PDF를 넣는 곳
│   └── converted/                   # $paideia-grade가 OCR한 마크다운을 여기에 씁니다
│
├── errors/
│   └── log.md                       # append-only YAML 오답 로그 ($paideia-weakmap / $paideia-cheatsheet의 원천)
│
├── quizzes/                         # $paideia-quiz — 문제마다 숨겨진 _answers.md 형제
├── mock/                            # $paideia-mock — 모의고사 (숨겨진 _sol.md 형제)
├── twins/                           # $paideia-twin — 같은 패턴, 다른 표면
├── chain/                           # $paideia-chain — 다중 패턴 통합 문제
├── derivations/                     # $paideia-derive — 참조용 유도 모음
├── cheatsheet/                      # $paideia-cheatsheet — 오답 기반 한 장 요약 (+ 선택적 PDF)
└── weakmap/                         # $paideia-weakmap — 시간순, append-only 이력
```

**직접 손으로 관리하시는 디렉토리는 두 개뿐입니다.**
- `materials/` — 원본 PDF(또는 MD)를 해당 하위 폴더에 넣어 주세요.
- `answers/` — 필기 스캔 PDF를 루트에 넣어 주세요. OCR 결과는 `answers/converted/` 아래에 생깁니다.

나머지 디렉토리는 모두 스킬이 만들어내는 산출물이니, 언제든 삭제하고 재생성하시거나, `git log <dir>`로 시간에 따른 자기 진전을 확인하시거나, Obsidian을 폴더 전체에 걸어 vault로 여시면 됩니다.

---

## 읽기 팁: Obsidian을 쓰세요

Paideia는 모든 것을 LaTeX 수식(`$...$`, `$$...$$`)이 포함된 평범한 마크다운으로 씁니다. 어떤 에디터로도 읽을 수 있지만, **[Obsidian](https://obsidian.md)**이 가장 자연스러운 선택입니다.

- 별도 설정 없이 MathJax로 `$...$`, `$$...$$` 수식을 렌더링합니다
- 백링크를 통해 `quizzes/q_<ts>.md`에서 인용된 `converted/lectures/chN.md §K`로 클릭 한 번에 이동할 수 있습니다
- 코스 폴더 전체가 그 자체로 볼트(vault)입니다 — Obsidian을 `~/courses/my-course`로 향하게 하면, 모든 파일이 검색 가능한 그래프가 됩니다
- 완전히 오프라인, 무료, 로컬에서 동작합니다. Paideia의 철학과 정확히 맞닿아 있습니다 — 당신의 필기, 당신의 디스크, 당신의 도구

마크다운 수식 확장을 설치한 VS Code도 가능합니다. 다만 터미널은 — 마크다운 프리뷰를 얹더라도 — 수식을 읽기에 적합하지 않으니 억지로 맞추지 마세요.

---

## 전체 워크플로우 — 예시

### Phase 0 — 코스당 한 번 (15분)

```bash
cp ~/textbooks/ch*.pdf      ~/courses/my-course/materials/textbook/
cp ~/lecture-notes/wk*.pdf  ~/courses/my-course/materials/lectures/
cp ~/hw/hw*.pdf             ~/courses/my-course/materials/homework/
cp ~/hw/hw*_sol.pdf         ~/courses/my-course/materials/solutions/
```

Codex CLI에서:

```
$paideia-ingest                     # 모든 PDF → paideia-mcp 병렬 비전 파이프라인, LaTeX 충실
$paideia-analyze <약점 힌트>        # 패턴 + 커버리지 + 요약 생성
$paideia-hwmap hot                  # 🔥🔥 exam-primary 영역 띄우기
```

### Phase 1 — 진단 (40분)

```
$paideia-quiz all 20                # 광범위 진단, 20문항
# 종이에 풀고 (40분), answers/diagnostic.pdf로 스캔
$paideia-grade                      # OpenAI Vision OCR + 전략 채점
```

### Phase 2 — 타겟 드릴링 (준비 시간의 대부분)

```
$paideia-weakmap                    # 우선순위 약점 리포트
$paideia-blind hw3-p2               # 이미 풀어 본 문제의 전략만 점검
$paideia-twin hw3-p2                # 같은 패턴, 새로운 표면의 변형 문제
$paideia-chain 3                    # 3개 패턴이 결합된 통합 문제
$paideia-quiz weakmap 5             # 최신 weakmap을 겨냥한 5문항
```

### Phase 3 — 통합 (약 90분)

```
$paideia-mock 90                    # 숙제 밀도로 가중된 90분 모의고사
# 종이에 풀고 answers/mock_<ts>.pdf로 스캔
$paideia-grade                      # 모의고사 채점
```

### Phase 4 — 압축 (60분, 시험 전날 밤)

```
$paideia-cheatsheet --pdf           # 오류에서 출발한 한 장짜리 치트시트
$paideia-weakmap                    # 약점 구역을 한 번 더 훑기
```

### Phase 5 — 쿨다운 (시험 10분 전)

```
$paideia-weakmap                    # 상위 3개만. 새로운 것을 배우지는 마세요.
```

---

## 명령어 (총 14개)

| 명령 | 용도 |
|------|------|
| `$paideia-init-course` | 새 코스 폴더 부트스트랩 (의존성 확인, 골격, 메타데이터 입력, 백그라운드 `ollama pull`) |
| `$paideia-ingest [--force]` | `materials/**`의 모든 PDF를 `converted/**`의 마크다운으로 변환. `paideia-mcp` 병렬 비전 파이프라인으로 일괄 처리합니다. |
| `$paideia-analyze [힌트]` | `course-index/{summary,patterns,coverage}.md` 구축 |
| `$paideia-hwmap hot\|<§>` | 숙제 밀도 순으로 🔥🔥 Exam-primary 절 띄우기 |
| `$paideia-pattern <§\|Pk\|키워드>` | course-index에 있는 패턴 카드 표시 |
| `$paideia-derive <타겟>` | `derivations/<slug>.md`에 정돈된 참조 유도 저장 |
| `$paideia-quiz <주제\|§\|weakmap> [N]` | N개 연습 문항 생성, 답은 형제 `_answers.md`에 숨김 |
| `$paideia-blind <problem-id>` | 이미 본 문제의 전략만 확인하는 드릴 (재풀이 아님, 접근 기술) |
| `$paideia-twin <problem-id>` | 같은 패턴, 새 표면의 변형 문제 |
| `$paideia-chain <N>` | N개 패턴을 묶은 통합 문제 |
| `$paideia-mock <분>` | 숙제 밀도 가중 모의고사 전체 |
| `$paideia-grade [--ocr=<engine>] [경로]` | `.course-meta`의 엔진 선택(OpenAI Vision / Qwen3-VL / Tesseract)으로 OCR 후 전략 채점, `errors/log.md`에 누적 기록 |
| `$paideia-weakmap [개념]` | `weakmap/weakmap_<ts>.md`에 저장되는 우선순위 약점 리포트 |
| `$paideia-cheatsheet [--pdf]` | 오류 주도 한 장짜리 치트시트 |

---

## 내부 구조

### MCP 서버: `paideia-mcp`

Claude 에디션은 병렬 비전 인제스트를 PDF당 `general-purpose` 서브에이전트로 몰아서 처리했습니다. Codex에도 서브에이전트가 있지만 작업 단위가 더 무겁고, Codex의 `view_image` 도구는 이미지마다 사용자의 명시적 동의를 요구합니다 — 200페이지짜리 교재를 인제스트하는 일에는 어느 쪽도 맞지 않습니다. 그래서 Codex 에디션은 무거운 일을 **번들 stdio MCP 서버**인 `paideia-mcp`로 옮겼고, 스킬이 처음 MCP를 호출하는 순간 Codex가 이 서버를 자동으로 스폰합니다. 노출되는 도구는 네 개입니다.

| 도구 | 하는 일 |
|------|------|
| `ingest_pdfs` | `materials/**/*.pdf`를 전부 PNG로 렌더링하고, 긴 변을 ≤1800 px로 축소한 뒤, 선택된 엔진(`openai-vision` / `qwen3-vl` / `tesseract`)으로 병렬 OCR을 돌려 LaTeX 마크다운을 `converted/**`에 씁니다. `ProcessPoolExecutor`로 결정적 fan-out을 수행하며, PDF 단위로 재개(resume) 가능합니다. |
| `grade_pdf` | `.course-meta`에 설정된 엔진(인수로 덮어쓰기 가능)으로 필기 답안 PDF 한 건을 OCR하고, `answers/converted/<stem>.md`로 저장한 뒤 마크다운 + 신뢰도 티어를 반환합니다. |
| `build_course_index` | `converted/**`를 읽어 주제 트리 / 반복 풀이 패턴(P1..Pk) / 숙제 밀도 기반 커버리지를 추출하고 `course-index/{summary,patterns,coverage}.md`를 생성합니다. |
| `course_phase` | 디스크 위 산출물에서 현재 단계(setup → diag → drill → mock → cram → cool)를 도출해 `{phase, days_until_exam, top_miss_pattern}`을 반환합니다. `$paideia-phase`가 이 도구를 호출하며, 사이클 위치를 알아야 하는 다른 스킬들도 함께 씁니다. |

스킬 본체는 얇게(오케스트레이션 ~40–80 줄) 유지됩니다 — 인수 파싱, 올바른 MCP 도구 호출, 결과 요약. 원시 페이지 이미지는 절대 Codex의 컨텍스트로 들어오지 않습니다.

### 인제스트 파이프라인: 모든 PDF를 비전으로

`$paideia-ingest`는 `materials/**`의 모든 PDF를 동일한 비전 파이프라인으로 처리합니다. `pdfplumber`를 본문 위주 자료(교재, 과제)의 빠른 경로로 먼저 시도해 봤지만, 실제로는 신뢰할 수 없었습니다 — 얼핏 본문처럼 보이는 페이지도 수식·도표·다단 레이아웃·여백 주석이 섞이는 순간 조용히 단어 샐러드로 망가졌습니다. 코스마다 재조정이 필요한 카테고리별 휴리스틱과 폴백을 유지하느니, 모든 파일을 한 경로로 통일하는 편이 더 단순하고 안정적입니다.

| 원본 | 방법 |
|---|---|
| `materials/**/*.pdf` | 비전 파이프라인 (MCP 병렬 fan-out, LaTeX 충실) |
| `materials/**/*.md` | 프로비넌스 헤더를 붙여 통과 복사 |

파이프라인이 동작하는 방식: 각 페이지를 `dpi=160`로 PNG 렌더링하고, 어떤 OCR 호출이 나가기 전에 모든 PNG의 긴 변을 ≤1800 px로 축소합니다. 그 뒤 `paideia-mcp.ingest_pdfs`가 선택된 엔진으로 디스패치하며, PDF당 워커 프로세스 하나를 띄우고 그 안에서 I/O 바운드 OCR 호출을 위한 `ThreadPoolExecutor`를 돌립니다. 결과는 `ℏ ∂ p2 ℏ 2 ∂ 2 p ̂` 같은 파편이 아니라 `$$\hat H = -\frac{\hbar^2}{2m}\partial_x^2 + V(x)$$` 같은 깔끔한 수식입니다.

### 필기 OCR: 세 가지 엔진 중에서 직접 고르실 수 있습니다

사용자는 채팅에 수식을 타이핑하지 않습니다. 종이에 풀고, PDF로 스캔하고, 그 PDF를 `answers/`에 떨어뜨리신 뒤 `$paideia-grade`를 실행하시면 됩니다. 플러그인은 세 엔진 중 선택하신 엔진으로 스캔본을 마크다운으로 바꿉니다. 기본 엔진은 코스별 `.course-meta`의 `OCR_ENGINE`으로 지정하며, 개별 호출에서는 `$paideia-grade --ocr=<engine>`로 덮어쓰실 수 있습니다.

| 엔진 | 기본값? | 동작 방식 | 이럴 때 고르세요 |
|---|---|---|---|
| `openai-vision` | **예** | `paideia-mcp.grade_pdf`가 각 페이지를 PNG로 렌더링해서 OpenAI Responses API에 base64 이미지로 올려 보내고, 한 번에 마크다운으로 합성합니다. 당신의 `OPENAI_API_KEY`를 사용합니다. | 가장 마찰이 적은 기본 경로. 한국어·LaTeX 모두 강하고 로컬 모델 로딩 지연도 없습니다. |
| `qwen3-vl` | 선택 | Ollama HTTP API로 로컬 Qwen3-VL 8B를 호출하며, 실패 시 자동으로 tesseract로 폴백합니다. | 페이지 이미지조차 기기 밖으로 내보내고 싶지 않으실 때. 최초 `ollama pull qwen3-vl:8b` (~6 GB)가 필요합니다. |
| `tesseract` | 선택 | `pytesseract` `eng+kor`만 사용합니다. | 가장 빠르고 가볍습니다. 타이핑된 스캔엔 괜찮고, 필기엔 정확도가 낮습니다. |

세 엔진 모두 `answers/converted/<stem>.md`에 `<!-- SOURCE: ... -->` / `<!-- TIER: ... -->` 헤더 코멘트를 남기므로, `$paideia-grade`가 OCR 신뢰도가 낮을 때 그에 맞게 태도를 바꿀 수 있습니다.

기본 엔진(`openai-vision`)은 의도적으로 가장 마찰이 적은 선택으로 잡았습니다 — Codex CLI가 이미 `OPENAI_API_KEY`를 필요로 하기에, 기본 엔진에도 추가 설치나 키 관리가 없습니다. `qwen3-vl` 엔진은 페이지 이미지 자체에 대해 단단한 프라이버시 경계를 원하실 때를 위해, `tesseract` 엔진은 다른 엔진을 쓸 수 없을 때의 안정적인 하한선으로 남겨져 있습니다.

### 라인 단위가 아닌, 전략 기반 채점

손으로 쓴 수식의 OCR 잡음은 엄격한 대수식 채점을 사실상 쓸모없게 만듭니다 — 한 글자 `∫` ↔ `∑` 오독이 전체를 무너뜨리기 때문입니다. 더 중요한 사실은, **시험의 실제 병목은 패턴 인식이지 산수가 아니라는 점**입니다. 그래서 채점기는 문항마다 세 가지를 확인합니다.

1. **패턴 (Pattern)** — `course-index/patterns.md`에서 올바른 Pk를 골랐는지
2. **변수 (Variables)** — 올바른 치환 / 기저 / 인덱스 / 경로를 식별했는지
3. **최종 형태 (End-form)** — 최종 표현의 모양(차원, 점근, 구조)이 맞는지

오류는 타입이 지정된 분류(`pattern-missed | wrong-variable | wrong-end-form | algebraic | sign | definition`)와 함께 YAML 형태로 `errors/log.md`에 기록됩니다. 이 로그가 `$paideia-weakmap`의 씨앗이자, `$paideia-cheatsheet --pdf`의 *유일한* 입력이 됩니다.

### *당신의* 풀이에서 추출된 패턴

`$paideia-analyze`는 일반적인 "미적분 기법" 목록을 배포하는 도구가 아닙니다. 당신 과목의 실제 해답지를 읽어 반복되는 풀이 패턴을 추출하고, P1, P2, … 로 라벨을 붙인 뒤, 당신 자신의 `converted/solutions/` 파일을 인용하는 worked instance를 함께 제공합니다. 패턴은 *당신 과목 고유의 관용구*이지 어떤 교과서의 것도 아닙니다. 복소해석 수업에서 P3는 "닫힌 경로 + Jordan's lemma + 본질 특이점에서의 residue"일 수 있고, 선형 시스템 수업에서 P3는 "부분분수 + 복소극점을 갖는 역Laplace"일 수 있습니다. 각 분야는 자신만의 손놀림을 가지고 있고, 그것은 과목 자신을 통해서만 드러납니다.

### Append-only 이력

`weakmap/` 디렉토리는 절대 덮어쓰지 않습니다. `$paideia-weakmap`을 호출할 때마다 `weakmap/weakmap_<ISO-timestamp>.md`가 새로 생성됩니다. `git log weakmap/`를 통해 어떤 약점이 가장 먼저 무너졌는지, 어떤 약점이 끈질기게 남아 있었는지, 진단 모의고사 이후 어떤 새로운 약점이 등장했는지 정확히 확인할 수 있습니다. "자신의 이해를 시간 축 위에서 `git diff`한다"는 발상이 실제로 구현된 지점이 이곳입니다.

### 단계 감지

Codex는 Claude Code처럼 지속되는 statusline 슬롯을 노출하지 않기 때문에, Claude 에디션이 그 자리에 그려 주던 네온 한 줄은 이식되지 않았습니다. 다만 그 뒤에 있던 단계 감지 로직 자체는 고유한 동사로 노출되어 있습니다.

```
$paideia-phase
```

`setup · diag · drill · mock · cram · cool` 중 하나와 `D-<시험까지 남은 일수>`, 그리고 최신 weakmap의 top-miss 패턴을 함께 출력합니다. 단계는 달력이 아니라 **디스크 위의 산출물**에서 도출되며, 산출물이 실제로 생겨야만 단계가 넘어갑니다.

- `setup` — `course-index/patterns.md`가 아직 없음 → `$paideia-ingest` + `$paideia-analyze`
- `diag` — 패턴은 있으나 퀴즈가 아직 없음 → `$paideia-quiz all 20`으로 전체 진단
- `drill` — 퀴즈는 있으나 모의고사가 아직 없음 → `$paideia-blind` · `$paideia-twin` · `$paideia-quiz weakmap` 반복
- `mock` — 모의고사가 있고 치트시트가 아직 없음 → `$paideia-cheatsheet --pdf`로 압축
- `cram` — `cheatsheet/final.{md,pdf}` 존재 → 테이퍼링, weakmap 재독, 새 개념은 학습하지 않기
- `cool` — `D-0` (시험 당일)은 위 모든 분기를 덮어씁니다

---

## 배포물

```
PAIDEIA-codex/
├── .agents/plugins/marketplace.json     # 마켓플레이스 매니페스트 (Codex)
├── LICENSE                              # MIT
├── README.md                            # 영문
├── README.ko.md                         # 본 파일
└── plugins/paideia/
    ├── .codex-plugin/plugin.json        # 플러그인 매니페스트 (name, version, author)
    ├── .mcp.json                        # paideia-mcp 스폰 설정
    ├── README.md                        # 빠른 참조 카드
    ├── paideia-mcp/                     # 번들 stdio MCP 서버
    │   ├── pyproject.toml
    │   ├── README.md
    │   └── paideia_mcp/
    │       ├── server.py                # stdio 엔트리, 도구 등록
    │       ├── ingest.py                # ingest_pdfs
    │       ├── grade.py                 # grade_pdf
    │       ├── analyze.py               # build_course_index
    │       ├── phase.py                 # course_phase
    │       └── ocr/
    │           ├── openai_vision.py     # OpenAI Responses API (OPENAI_API_KEY 필요)
    │           ├── qwen3vl.py           # 로컬 Ollama Qwen3-VL 8B
    │           └── tesseract.py         # pytesseract eng+kor
    └── skills/                          # 14개의 동사 스킬
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

## 설계 원칙

1. **터미널은 수식 읽기에 나쁩니다.** Codex는 마크다운 파일을 만들고, 당신은 그것을 (가능하면 Obsidian에서) 읽습니다.
2. **풀이를 타이핑하는 일은 느리고 오류에 취약합니다.** 종이에 풀고 스캔하면, 플러그인이 (로컬로, 또는 OpenAI Vision을 통해) OCR을 처리합니다.
3. **OCR 잡음은 피할 수 없습니다.** 그래서 채점은 전략 기반(패턴 / 변수 / 최종 형태)으로 이뤄집니다 — 라인별 대수 검증이 아니라요. 실제 시험 채점자가 보는 것과 동일한 관점이기도 합니다.
4. **패턴은 *당신 과목의* 풀이에서 추출되어야 합니다** — 범용 목록에서가 아니라요. 각 분야는 고유한 관용구를 가지며, 그 관용구는 해당 과목 자신을 통해서만 드러납니다.
5. **당신의 오류는 가장 가치 있는 학습 신호입니다** — 교과서보다, 강의보다 더요. 치트시트는 실러버스가 아니라 `errors/log.md`에서 생성됩니다.
6. **숙제 밀도가 시험을 알려 줍니다.** 당신의 시간은 유한하니, 점수가 있는 곳에 쓰세요.
7. **모든 것이 직접 편집 가능합니다.** 패턴·weakmap·치트시트·오답 로그 전부 당신 git 이력 안의 평범한 마크다운/YAML입니다. `P3`이 틀린 것 같으면 고쳐 쓰시면, 다음 드릴부터 그 수정본이 사용됩니다. 지난 학기 과목 폴더를 fork해서 이번 학기용으로 차이만 수정하셔도 됩니다. 플러그인은 뼈대이고, 학습 그래프는 당신의 것입니다.
8. **무거운 파이프라인은 스킬 본체가 아니라 MCP에 삽니다.** 병렬 비전 인제스트, 다중 엔진 OCR 디스패치, 패턴 추출, 단계 감지는 모두 `paideia-mcp` 안에 구현되어 있고 스킬은 그 위에서 오케스트레이션만 담당합니다. 덕분에 스킬 본체가 손으로 감사 가능한 길이로 유지되고, 원시 페이지 이미지가 Codex의 컨텍스트에 들어오지도 않습니다.

---

## FAQ

**수학 과목이 아닌 경우에도 쓸 수 있나요?**
문제-패턴 추출을 중심으로 설계되어 있어, 정량 분야에서 강점을 가장 잘 드러냅니다: 수학, 물리, 전자공학, 전산 이론, 머신러닝 이론, 통계, 공학 등입니다. 역사나 문학 같은 과목에서도 인제스트와 요약은 동작하지만, 드릴 명령은 "문제에 풀이 패턴이 존재한다"는 전제를 두고 있습니다.

**한국어·영어가 섞인 자료도 되나요?**
됩니다. 인제스트와 OCR이 `eng+kor`로 설정되어 있고, 패턴과 채점 응답도 원자료의 언어 구성을 그대로 따라갑니다.

**그냥 ChatGPT / Claude / Gemini에게 공부 도와 달라는 것과 뭐가 다른가요?**
과목별 영속성입니다. LLM 챗은 당신이 2주 전 HW2에서 놓친 패턴을 기억하지 못하고, 당신 교수님이 어느 절을 실제로 강조하시는지에 대한 랭킹이 없으며, "당신의 전형적인 실수 유형"이라는 개념 자체가 없습니다. Paideia는 그 모든 것을 당신 디스크의 마크다운 파일에 써 넣습니다. `errors/log.md`가 append-only이기 때문에, 오늘 호출한 `$paideia-weakmap`은 과목 시작 이후의 모든 `$paideia-grade` 기록을 반영해서 작성됩니다. 일반 챗 세션은 아무리 똑똑해도 열 때마다 백지 상태입니다.

**패턴 / 치트시트 / weakmap이 마음에 안 들면 직접 고칠 수 있나요?**
네. 산출물을 평범한 마크다운으로 두는 이유가 정확히 그것입니다. `P3`이 틀린 것 같으면 `course-index/patterns.md`를 열어 다시 쓰시면 됩니다 — 이후 드릴은 그 수정본을 사용합니다. 치트시트가 엉뚱한 걸 강조한다면 잘라 내시면 됩니다. 플러그인은 뼈대이고, 학습 그래프의 모양은 당신이 잡으십니다.

**Ollama / Qwen3-VL이 꼭 필요한가요?**
아니요. 기본 OCR 엔진은 Responses API로 동작하는 OpenAI Vision입니다 — Codex CLI가 이미 필요로 하는 `OPENAI_API_KEY`를 그대로 쓰고, 추가로 설치할 것이 없습니다. Ollama + `qwen3-vl:8b`는 페이지 이미지까지 기기 안에 붙잡아 두고 싶으실 때를 위한 선택 경로입니다. `tesseract`는 설치를 최소로 하고 싶거나 타이핑된 스캔만 다루실 때를 위한 세 번째 옵션입니다.

**`qwen3-vl:8b`를 선택했는데 제 기기가 감당하지 못하면요?**
MCP 서버의 OCR 디스패처가 Ollama 실패 시 자동으로 tesseract `eng+kor`로 폴백합니다. 또는 `.course-meta`의 `OCR_ENGINE`을 `openai-vision`으로 바꾸시거나 `--ocr=openai-vision`을 붙이시면 Ollama를 완전히 우회할 수 있습니다.

**여러 과목에서 재사용할 수 있나요?**
네 — 각 과목은 자신만의 폴더 안에 자신의 `.course-meta`, `course-index/`, `errors/log.md`, `weakmap/`을 가집니다. 과목 간에 공유되거나 섞이는 것이 없습니다. 그때그때 작업하실 과목 폴더 안에서 Codex CLI를 여시면 됩니다.

**LLM이 매긴 채점 결과를 믿어도 되나요?**
채점은 전략 기반(대수식 검증이 아니라 패턴 매칭)이며, 채점기는 `course-index/patterns.md`의 패턴을 인용하고, 모든 채점은 `errors/log.md`에 감사 가능한 YAML 항목으로 남습니다. 혹시 채점이 잘못되었다면 해당 YAML 항목만 수정하시면 됩니다 — 다음 `$paideia-weakmap`이 수정 사항을 반영합니다.

**제 데이터는 외부로 나가지 않나요?**
PDF·마크다운·오답 로그·weakmap은 모두 로컬 코스 폴더 안에만 머물며, 어떤 제3자 서비스로도 업로드되지 않습니다. 플러그인이 일으키는 네트워크 트래픽은 선택하신 OCR 엔진에 따라 달라집니다. `openai-vision`(기본)을 고르시면 페이지 이미지는 HTTPS로 OpenAI Responses API에 전송됩니다(= Codex CLI 자체가 이미 쓰고 있는 동일한 엔드포인트). `qwen3-vl`을 고르시면 최초 모델 다운로드 이후에는 어떠한 데이터도 기기 밖으로 나가지 않습니다. `tesseract`는 아무 때도 네트워크를 타지 않습니다.

**Claude Code 에디션과 산출물을 공유할 수 있나요?**
네. 디스크 레이아웃이 바이트 단위로 호환됩니다. Claude 에디션이 초기화한 코스 폴더는 Codex 에디션에서도 그대로 열리며(기존 `CLAUDE.md` 옆에 `AGENTS.md`만 하나 더 있으면 됩니다 — `$paideia-init-course`가 생성해 드립니다), 그 반대도 마찬가지입니다. 한 에디션에서 기록된 오답이 다른 에디션의 weakmap으로 그대로 흘러갑니다 — 변환이 필요하지 않습니다.

---

## 연락

<p align="center">
  <a href="https://github.com/TaewoooPark"><img src="https://img.shields.io/badge/-GitHub-181717?style=for-the-badge&logo=github&logoColor=white&cacheSeconds=3600" alt="GitHub"></a>
  <a href="https://x.com/theoverstrcture"><img src="https://img.shields.io/badge/-X-000000?style=for-the-badge&logo=x&logoColor=white&cacheSeconds=3600" alt="X (Twitter)"></a>
  <a href="https://www.linkedin.com/in/taewoo-park-427a05352"><img src="https://img.shields.io/badge/-LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white&cacheSeconds=3600" alt="LinkedIn"></a>
  <a href="https://www.instagram.com/t.wo0_x/"><img src="https://img.shields.io/badge/-Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white&cacheSeconds=3600" alt="Instagram"></a>
  <a href="mailto:ptw151125@kaist.ac.kr"><img src="https://img.shields.io/badge/-Email-D14836?style=for-the-badge&logo=gmail&logoColor=white&cacheSeconds=3600" alt="Email"></a>
</p>

---

## 라이선스

MIT. 자유롭게 쓰시고, 본인 과목에 맞춰 fork하거나 수정하셔도 됩니다 — 이 플러그인의 핵심은 플러그인이 만들어 주는 학습 그래프가 고정된 제품이 아니라 당신이 모양을 잡을 수 있는 산출물이라는 점에 있습니다.

---

<p align="center">
  <em>일반적인 커리큘럼은 평균적인 학생을 가르칩니다. Παιδεία — 한 명의 학생을 위한 형성.</em>
</p>
