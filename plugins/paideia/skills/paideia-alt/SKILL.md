---
name: paideia-alt
description: Import an OPTIMETA Exam Radar (Alt plugin) export and fold its lecture-emphasis exam signal into the course index — write course-index/radar.md, add a lecture-emphasis column + divergence flags to coverage.md (without overriding the HW-based tier), and seed a gold-zone weakmap. The export form is fixed (exam-radar:v1 marker).
---

# paideia-alt

Exam Radar is OPTIMETA's Alt plugin. From lecture-recording transcripts it extracts the topics a professor **verbally emphasized**, ranks them by exam probability, and lets the user triage each into one of three zones. Its 복사 button emits a fixed markdown form. This skill ingests that form.

PAIDEIA already has one exam-probability signal — **HW density** (`course-index/coverage.md`). Exam Radar adds a second, independent one — **lecture emphasis**. The two corroborate where they agree and expose blind spots where they diverge.

**Premise (do not break).** HW density stays the primary `Exam tier`. Lecture emphasis is layered on as annotation and a second opinion — surfaced, never substituted. A single lecture signal does **not** auto-upgrade an HW-based tier (mirror `$paideia-analyze`'s rule). What it does is flag divergences for the user to judge.

## Arguments (free-form)

The pasted Exam Radar export (may be multi-line). If empty, fall back to `materials/radar.md`.

## Step 0 — Get the export

1. If the arguments contain the export (look for `<!-- exam-radar:v1`), use them.
2. Else if `materials/radar.md` exists, read it.
3. Else: tell the user — "Exam Radar에서 **학습 로드맵 → 복사** 후 `$paideia-alt` 뒤에 붙여넣거나, `materials/radar.md`로 저장해줘." — then stop.
4. Validate the marker. No `<!-- exam-radar:v1` → not an Exam Radar export; stop. Version `> 1` → warn that this skill parses v1 and may ignore new fields, then proceed best-effort.

## Step 1 — Parse the export (`exam-radar:v1`)

```
# Exam Radar 작전 — <course>
<!-- exam-radar:v1 source=alt -->

- 코스: <course>
- 시험까지: <D-N>
- 토픽: 총 <N>개 (골드존 <G> · 버려도 안전 <D>)
- 버려도 안전 비중: 전체의 <P>%

## 지금 할 것 — 골드존 (시험확률 높음 · 아직 약함)
1. <topic> · 시험확률 <p>%[ · 🎙]
...
## 이미 다진 것 (잘 알거나 시험에 덜 나옴)
- <topic> · 시험확률 <p>%
...
## 버려도 안전 (안 해도 되는 것)
- <topic> · 시험확률 <p>%
...
```

- Read `- 코스:`, `- 시험까지:` (D-N), the count line.
- Three `## ` headings → zones: `지금 할 것 — 골드존` = **gold** (high prob, low confidence), `이미 다진 것` = **strong**, `버려도 안전` = **skip**.
- Each line: `<name> · 시험확률 <p>%`, optional ` · 🎙` (verbally stressed). The leading `1.`/`-` is list markup. Parse `name`, integer `p` (0–100), and the `🎙` flag. Be lenient on whitespace. `(없음)` / `(아직 없음 …)` = empty zone.

## Step 2 — Write `course-index/radar.md` (canonical store)

Overwrite on re-import.

```markdown
<!-- SOURCE: Exam Radar (Alt), exam-radar:v1, course=<course>, <D-N>, imported <YYYY-MM-DD> -->
# Lecture-emphasis signal — <course>

Imported from Exam Radar. Exam probability here is **lecture emphasis** (professor's spoken stress + repetition across recordings), independent of HW density in `coverage.md`.

| Topic | Exam prob | Zone | Lecture signal |
|---|---|---|---|
| <topic> | <p>% | gold | 🎙 |
...one row per topic, exam-prob descending within each zone, gold → strong → skip.

## Now (gold zone)
High exam probability, still weak — drill these first:
- <topic> (<p>%)[ 🎙]

## Safe to drop
- <topic> (<p>%)
```

If `course-index/` doesn't exist yet, create it. `radar.md` stands on its own even before `$paideia-analyze` has run.

## Step 3 — Merge into `course-index/coverage.md` (if it exists)

If `coverage.md` is missing, skip this step and tell the user to run `$paideia-analyze` first — `radar.md` already captured the import.

Otherwise:

1. **Map** each Exam Radar topic to a reverse-map section (`§`) by title match — case- and spacing-insensitive, substring allowed (e.g. "Gram-Schmidt" ↔ "§3.2 Gram-Schmidt orthogonalization"). Keep the best match; leave the rest unmatched.
2. **Add/refresh a `Lecture emphasis` column** on the reverse-map table. Value from exam-prob: `🎙🎙` gold or ≥70%; `🎙` 40–69%; `·` <40% or unmapped.
3. **Do not change the `Exam tier`** — it is HW-derived and stays.
4. **Append a divergence section:**

   ```markdown
   ## Lecture vs HW — divergences (judge these)

   ### 🎙 Stressed in lecture, but no HW
   §/topic emphasized (🎙🎙) yet marked ⚪ Low-risk in coverage:
   - <§ or topic> — verbal-only exam point? decide; if it matters, `$paideia-derive` or `$paideia-quiz` it.

   ### HW-dense, but quiet in lecture
   § marked 🔥🔥/🔥 with `·` lecture emphasis:
   - <§> — quietly important; tested without lecture time on it.
   ```

   Respect the premise: the ⚪ line is a *prompt to judge*, not an automatic tier upgrade.
5. **Unmatched topics** — append under `## From Exam Radar (no HW section match)` so nothing is lost.
6. **Drill priority** — use lecture emphasis as a booster/tie-breaker (🎙🎙 + thin/blind ranks above an equal item without emphasis), without reordering across HW tiers.

Re-runs replace the `Lecture emphasis` column and the `Lecture vs HW` / `From Exam Radar` sections in place — never duplicate.

## Step 4 — Seed a gold-zone weakmap

The gold zone = **high exam probability + low self-confidence** = a weakness the user effectively declared, corroborated by lecture emphasis. Treat it like `$paideia-weakmap` Case B (user-declared weaknesses).

- Write a **new** `weakmap/weakmap_<YYYY-MM-DD_HHmm>.md` (never overwrite — preserve history).
- Use the `$paideia-weakmap` report format. Put gold-zone topics under `## User-declared weaknesses`, each tagged `(from Exam Radar gold zone)`, mapped to related `§`/`Pk` via `course-index/`, with a recommended drill (`$paideia-blind` / `$paideia-quiz` / `$paideia-derive`). Also run the weakmap latest-error snapshot so the report stays consistent. If `errors/log.md` and `course-index/` are absent, write a minimal report (gold zone only) and note that `$paideia-analyze` will enrich it.

## Idempotence

- `radar.md` — overwrite (snapshot of the latest Exam Radar state); warn if hand-edited (`<!-- SOURCE: Exam Radar` header missing).
- `coverage.md` — merge is re-runnable (replace, don't duplicate).
- `weakmap/` — never overwrite; always a new timestamped file.

## Notes

- Lecture-emphasis exam-prob and HW-density exam-prob are **different axes**; never average them into one number. Keep them as separate columns/files so the user sees both and can reason about divergence.
- Exam Radar topics are lecture-derived, so they overlap heavily with `summary.md` sections — but section numbering may have been edited. Always do best-effort matching and surface the unmatched rather than forcing a map.

## Output

Print a short summary (Korean prose, identifiers verbatim):

```
Exam Radar 반영 완료 (<course>, <D-N>).
- course-index/radar.md     ← 토픽 <N>개 (골드존 <G> · 이미 다진 것 <S> · 버려도 안전 <D>)
- course-index/coverage.md  ← Lecture emphasis 열 추가, 발산 <X>건
- weakmap/weakmap_<ts>.md   ← 골드존 <G>개를 약점으로 등록
다음: $paideia-weakmap (합쳐진 우선순위) · $paideia-quiz <gold §> (골드존 드릴)
```
