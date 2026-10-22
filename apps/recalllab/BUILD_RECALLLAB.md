# RecallLab — End-to-End Implementation Brief

## Role and goal
You are a senior Python/full-stack engineer and careful maintainer of an existing learning repository. Build a complete, production-quality **local-first revision website** called **RecallLab** in **this same checkout**, at `apps/recalllab/`. Do **not** create another Git repository, git submodule, separate workspace, or cloud-hosted service.

The website must use my actual Data Engineering learning journey, notes, exercises, mistakes, assessments, and study history. It should strengthen long-term retention through retrieval practice, spaced practice, feedback and practical coding. It is not a replacement for my existing five-role tutor; it is a browser interface over the same durable learning records.

## Before coding: inspect and respect this repo
Read, in order:
- `AGENTS.md`, `README.md`, `START-HERE.md`
- `reference/learning-coach.md`, `reference/note-style.md`, `reference/checkpoints.md`
- `tracking/README.md`, `tracking/coach.py`, `tracking/note_revision.py`, `tracking/tests/test_coach.py`
- `tracking/revision-queue.csv`, `tracking/revision-history.csv`, `tracking/topic-map.json`, `tracking/mistakes.json`, `tracking/skill-state.json`, `tracking/study-log.csv`, `tracking/checkpoint-index.json`
- `Notes/README.md`, `Notes/revision/README.md`, relevant source notes under `Notes/`
- `progress/current.md`, latest `progress/session-history.md`, `plan/learning-and-revision-plan.md`
- `codex/skills/revision-coach/SKILL.md`, relevant current exercises in `tools/`, and `projects/rrdap/`.

Inspect actual code, tests, data schemas, existing commands and limitations instead of inferring behavior from filenames. Identify the authoritative record for each state in a small architecture note before implementing. Preserve the active RRDAP task, all timer state, existing scores, due dates, attempt IDs and learning history. Never infer completion or mastery from a note, notebook output, project setup or study duration.

## Required repository layout
Create only what is needed under this repository, preferably:
```
data-engineering-journey/
  apps/
    recalllab/
      README.md
      HANDOFF.md
      app.py
      pages/
      components/
      services/
      challenges/
      tests/
      config.example.toml
      requirements.txt
      .streamlit/config.toml
      data/                 # ignored local-only operational cache/drafts
  Notes/                     # EXISTING authoritative note source
  tracking/                  # EXISTING authoritative learning trackers
  progress/                  # EXISTING checkpoint/history
  tools/                     # EXISTING exercise evidence
  projects/rrdap/            # EXISTING active project
```
Add targeted `.gitignore` rules for local database files, generated runtime artifacts, uploaded code, credentials and caches. Do not copy the Notes vault into the app. Do not duplicate `MISTAKES.md`, `REVISION_SCHEDULE.md`, `AI_HANDOFF.md` or create a competing schedule. `apps/recalllab/HANDOFF.md` covers *website development state only*, not learning history. Reuse existing `START-HERE.md` for learning continuity.

## Stack and design
Prefer **Python + Streamlit** for a fast maintainable local website, reusable Python services, and SQLite **only for transient app-specific state** (question cache, pending submission journal, UI settings). Use existing CSV/JSON/Markdown records as authoritative learning state, through the existing `tracking/coach.py` interfaces; never rewrite them directly from UI callbacks. A safe coding runner may require a separate contained execution component. Avoid introducing Kubernetes, cloud infra or paid services.

Match the approved dark dashboard mockup as closely as Streamlit reasonably allows: dark navy/charcoal background, rounded bordered panels, clean sidebar, blue buttons, green activity heatmap, strong visual hierarchy, responsive desktop layout. Sidebar: Dashboard, Today's Session, Question Bank, Coding Challenges, Notes Browser, Mistakes & Weak Topics, Progress & Analytics, Revision Calendar, Search Notes, Settings.

## Feature A — GitHub-style 365-day activity calendar
- 7 weekday rows, week columns, monthly headings, small square cells, `Less → More` legend, green intensity from zero to extra activity, hover tooltips, click/day selection with real details. Use actual `Asia/Kolkata` dates and support the year boundary.
- Read **confirmed closed** study intervals from `tracking/study-log.csv` and actually answered events from `tracking/revision-history.csv`. Also link coding evidence where reliable. Distinguish All Learning, Revision Only, Coding Practice.
- Set configurable color thresholds *per metric*. A default all-study intensity scale should use the repo's existing weekday/weekend targets, with darkest green representing substantial **extra verified study above the day's target**. A revision-only activity scale may use 0, <15, 15–29, 30–59, 60–119, 120+ measured minutes when reliable. If no duration exists, use an explicitly labeled count-based revision scale instead of inventing time.
- Do not add minutes already included in a study interval to revision time again. Do not count unfinished/uncertain timer intervals as confirmed hours. Do not turn a cell green merely for opening the site, opening notes or generating questions. Failed-but-genuine attempts count as activity, not correctness.
- Show current streak, longest streak, active days, confirmed study hours, revision attempt count. For a clicked day: real recorded study time, questions and results, code outcomes, observed mistakes, recommended notes (or clear missing evidence). No fake metrics outside clearly labeled demo mode.

## Feature B — Adaptive daily revision
- Build a manageable daily queue from existing `tracking/revision-queue.csv`, history, topic mappings, prerequisites and real mistakes. Prefer due/overdue/weak topics without overwhelming the user. Initial/unassessed is not failed, and planned dates are not actual attempts.
- Each session mixes active recall, explaining concepts, code output prediction, error diagnosis, coding reconstruction and realistic application. Default 15–20 minutes, user-adjustable; allow extra optional practice.
- **Questions must meaningfully vary daily** (changed input data/scenarios/problem formats), while revisiting the underlying concept according to the schedule. Stable concept IDs and question variant IDs prevent pointless identical repeats; deterministic seeded variations or a local curated bank must work without AI. New questions should reference real source note paths/headings.
- Ask first, hide notes and worked solutions until answer/submission. Offer progressive hints, notes link, then changed-example retry. Track hints/help/notes consulted honestly. Do not spoil the active project task's future pain points or solve it in the learner's existing attempt files.
- Respect repository's existing 1/3/7/14/30-day schedule and scoring semantics in `tracking/coach.py`. **Do not switch to FSRS** or invent a second scheduler. Delayed recall and immediate correction must remain distinguishable; independent means genuinely unaided.

## Feature C — Coding challenge engine
- Python challenges: real problem statement, constraints, small sample inputs/expected outputs, writable editor, Run Tests, feedback, hints, Submit Attempt. First examples should be grounded in actual studied Python topics: lists, dictionaries, file operations, `csv.reader`, `DictWriter`, random/Faker, simple record cleaning and exception handling.
- SQL: join preservation, NULL counting, grouping/grain, aggregations and later studied topics. Validate output on multiple controlled fixtures, not SQL string similarity.
- **Safety gate:** Never run untrusted Python directly in the Streamlit process or in an unrestricted subprocess. Use a genuinely isolated runner with disabled network, minimal permissions, CPU/memory/time limits and no access to credentials or the learning repository; if not available, disable Run Tests and provide manual submission/evaluation. SQL must run only in an isolated disposable DB, never the learner's existing PostgreSQL or other databases. Handle infinite loops and malicious input safely.
- Record code submissions, test evidence, actual result and help usage. Do not declare correct merely from AI feedback. Keep scores for explanation, predicting, modifying, building and debugging separate where the existing state supports them. Extend to PySpark only after Python/SQL is stable and tested.

## Feature D — Personalized note recommendations
After each session show **top three specific notes/sections** to review. Source from real missed concepts, observed mistakes and coding test failures. For each: relative Markdown path, heading/anchor, observed gap, relevant attempt evidence, concise action, "Open Note" and "Retry". Notes should render read-only inside the site, preserving Markdown code blocks. Do not recommend full-note rereading by default; never treat opening a note as mastery. Detect changed notes and show mapping warnings instead of resetting review history.

## Feature E — Durable history, consistency, recovery
- Every **submitted** attempt must be durably written before displaying "Saved". If the existing coach requires a checkpoint batch, introduce an app-specific durable pending-event journal (local SQLite or append-only files) and a safe idempotent commit bridge that follows the coach's constraints; do not silently bypass checkpoint rules. Distinguish "saved locally/pending sync" from "recorded in canonical tracker" and "pushed to GitHub".
- Reuse `tracking/coach.py record`, `refresh`, `validate`, `recover` workflows as documented. Use stable unique `attempt_id`, `review_id` and `checkpoint_id`, guard against double submits and replay/retry, and preserve evidence. If necessary extend existing helper APIs narrowly with tests, but keep all existing consumers working.
- Save actual question text, learner answer/code or safe file reference, feedback, score or null, hints and note usage, assessment kind and IST timestamp. A blank/unevaluated answer cannot earn a mastery score. Do not overwrite original attempts.
- End session: persist concise outcome and exact notes to review, update authoritative queue/history/mistakes/skill observations through existing workflow, refresh generated `Notes/revision` views and validate. Do not rewrite `progress/current.md` or `START-HERE.md` unless the meaning of the current learning checkpoint truly changed and both are updated consistently under existing rules.
- On restart, restore pending drafts, prior sessions, saved outcomes and due schedule. Recovery from partial writes should be tested. Write no local credentials into Git.
- On laptop/desktop switching, tracked learning history syncs only after intentional commit/push and pull. Local SQLite caches/drafts **do not** automatically sync. Provide safe export/recovery instructions, local backups, and warn when uncommitted attempts exist. Never auto-push or force-pull.

## Feature F — Dashboard and reports
- Dashboard top: 365-day green calendar plus active days, current/longest streak and hours. Cards: today's revision progress, assessed recall accuracy, coding tests passed, specific notes to review. Area: "Start Session", task queue, focus areas, recent activities, note recommendations, weekly trend.
- Dedicated pages: question bank with evidence/source filters; coding challenges; notes browser; observed mistakes; progress analytics with accuracy vs activity separation; full calendar; search notes; settings.
- Performance should distinguish initial success, delayed retention, assisted versus independent, unknown outcomes and unassessed concepts. A high activity count is not the same as mastery. Display a clear empty state if historical data is missing.
- Optional AI for grounded question generation/feedback: disabled by default; offline deterministic questions must work. Let user opt into a provider, explicitly disclose when notes are sent, keep secrets in environment variables, cache/check generated content, fail gracefully when offline.

## Implementation order — finish all supported phases, with gates
1. Inspect repo and write concise architecture/record authority mapping. Verify original tracking tests pass before changes. Build a **read-only** dashboard/heatmap and note browser using real files.
2. Build daily queue, question bank, variation, submissions and durable recovery; integrate canonical review recording and notes recommendations. Test accurate scheduling, duplication and help semantics.
3. Build coding challenges and fully isolated runner(s); if isolation is not deliverable, still deliver manual coding assessment and clearly identify Run Tests as disabled, never fake safety.
4. Add remaining pages, analytics, settings and optional opt-in AI; polish accessibility/responsiveness and tests.
5. Run integration tests and a local browser/manual smoke test if possible. Show realistic empty states, not mock metrics. Document Windows PowerShell install/start commands and the exact URL.

## Acceptance tests
- Existing learning/revision tests still pass; actual tracked history is unchanged until a genuine user revision is submitted.
- GitHub-like annual calendar renders actual dated records and gets darker for verified extra learning; zero/missing/uncertain activity stays empty.
- A reviewed SQL/Python attempt generates truthful score/help/evidence and a targeted note recommendation; review schedule updates per existing rules.
- Repeated submit and interrupted writes recover without duplication; closing/reopening the site retains historical outcomes and pending drafts.
- AI-off mode runs and produces meaningful bounded review questions from current notes; date-to-date variation is demonstrable.
- No scripts automatically start/stop existing tutor study timers; no unintended RRDAP or progress changes.
- No arbitrary Python execution without a tested isolated runner; no SQL execution against the learner's databases.
- Single repository, website under `apps/recalllab/`, no separate repository, no public deployment.

## Handoff and completion report
At every major phase update `apps/recalllab/HANDOFF.md` with completed/verified functions, test commands/results, issues and exact next engineering task so a new coding-agent chat can continue. This is **development handoff only**; learning history stays in original tracking/progress files.

After completion, report precise files changed, commands run, tests/results, locally tested URL, features verified versus incomplete, storage/recovery behavior and how to use RecallLab every day. Never say a feature was implemented without files/tests proving it. Do not commit/push/host externally unless explicitly instructed.

**Begin now**: inspect the actual checkout, state the authoritative record mapping and integration risks concisely, then implement. Ask only if a blocker requires an essential decision; otherwise take the smallest safe path and continue building.
