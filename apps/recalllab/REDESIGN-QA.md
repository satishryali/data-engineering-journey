# Recall Lab redesign: audit, references and QA

Engineering audit on 26 October 2026. This document records product evidence,
not learner assessment. No study timer, proficiency, review event or project
acceptance is implied by implementing the application.

## Existing product and data contract

The application is Streamlit, local SQLite and repository Markdown/CSV/JSON.
Keep that stack and all thirteen routes in [routing.py](services/routing.py).
The actual feature inventory is:

| Page | Features to preserve |
| --- | --- |
| Dashboard | Actual due queue, activity, targets, weak concepts, note/task links |
| Today's Session | Saved bounded plan, one current task, drafts, hints, source consultation, assistance, submit, reference, human review, checkpoint recovery |
| Question Bank | Topic/mode/source/evidence search and practice links |
| Coding Challenges | Python/SQL filters, source editor, disposable SQL fixtures, hints, notes, code history, human review |
| Notes Browser | Original Markdown, heading selection, fenced code, tables, guarded links/images, related concepts/mistakes/exercises |
| Mistakes & Weak Topics | Real observed mistakes, source evidence, related due dates and retry links |
| Progress & Analytics | Actual scored outcomes, assistance, study and interview evidence |
| Revision Calendar | 365 IST dates, metric/date selection, activity distinctions, day links |
| Search Notes | Read-only original-note search and source links |
| Settings | Preferences, thresholds, pending drafts, backup/export/import, checkpoint retry, optional local Ollama opt-in |
| Learning Roadmap | Thirteen planned curriculum weeks and assessment buffer |
| Project | RRDAP checkpoint, active RDS-001 and actual acceptance criteria |
| Interview Practice | Prerequisite-aware questions, category selection, no answer reveal or automatic assessment |

Sources reviewed: [application](app.py), [components](components/),
[services](services/), [existing tests](tests/), [architecture](ARCHITECTURE.md)
and [existing audit](AUDIT.md). The old UI used small 9–12 px secondary text,
many competing saturated gradient cards, dense controls and an under-emphasized
daily-revision action. Session controls mixed drafting, references and assessment;
coding used one long vertical flow. Those are design problems to address without
removing controls or changing evidence semantics.

Pre-existing dirty changes at this audit's start were in the app, learning
component, journal, sessions and two test modules. Their substantive changes
included legacy SQLite session migration and bounded plan limits. Preserve these;
do not overwrite them as part of a visual refresh.

## Concrete design and acceptance plan

- One neutral charcoal shell, legible secondary copy, restrained accent, common
  borders/radii/spacing and consistent controls across all routes.
- Make Start Today's Revision the dashboard's strongest action. Show genuine due
  counts and estimates labelled as estimates; keep backlog workload bounded.
- Retain one saved current task. Hide the worked reference before submission,
  reject blank attempts, preserve pause/cursor/drafts across restart and retain
  assistance declarations. Record subjective recall separately from scored facts.
- Put challenge instructions and code/feedback side by side on desktop, stack on
  small screens, and retain the disabled Python executor explanation.
- Keep notes read-only and mistakes tied to recorded evidence. No mastery claim
  from note reading, activity, elapsed time or a planned curriculum week.
- Cover every route, meaningful navigation and persistence. Check real desktop
  and mobile rendering, keyboard focus, reduced motion and overflow with a browser.
- Preserve canonical trackers, handoff and active learner attempts during browsing,
  drafting, self-rating and engineering tests. Use disposable fixtures for scoring.

## Contemporary official references fetched

HTTP checks were performed during this engineering session. Public pages establish
patterns and current product descriptions; they are not an authenticated audit of
each application's internal workspace. No proprietary assets were copied.

| Reference | Actual result and design implication |
| --- | --- |
| [Linear](https://linear.app) | HTTP 200. Official page emphasizes speed and reducing noise. Adopt restrained hierarchy and a quiet shell. Its current public copy concerns product-development workflows; do not claim an authenticated UI inspection. |
| [RemNote](https://www.remnote.com) | HTTP 200. Official page describes notes, flashcards, spaced repetition, practice quizzes and search. Connect source notes to retrieval while keeping reading and testing distinct. |
| [Anki studying](https://docs.ankiweb.net/studying.html) | HTTP 200, redirects to the current manual. Again means failed recall; Hard means correct but difficult; Good/Easy are successful retrieval. Adopt explicit wording so forgetting cannot be mislabelled difficult success. |
| [Duolingo](https://www.duolingo.com) | HTTP 200 but static response exposes only the title. The approach/info routes likewise require client rendering. [Official habit article](https://blog.duolingo.com/how-duolingo-streak-builds-habit/) failed certificate verification in this Python environment. Calm completion feedback is a design recommendation, not a newly verified claim about Duolingo's current authenticated UI. |
| [Brilliant](https://brilliant.org) | HTTP 200. Current page describes sequenced problem solving, targeted practice, hints and feedback before independent solving. Prefer genuine attempts and useful feedback over passive content consumption. |
| [LeetCode](https://leetcode.com) | HTTP 403; its official editor-support page also returned 403. [HackerRank Python](https://www.hackerrank.com/domains/python) returned 200 with real challenge list, difficulty and Solve Challenge actions. Focused instruction/editor/result grouping is a design recommendation; this audit does not claim to have accessed LeetCode's current editor. |
| [Raycast](https://www.raycast.com) | HTTP 200. Official page emphasizes fast, ergonomic interactions and keyboard access. Use discoverable native shortcuts and visible focus; do not replace accessible controls with hidden shortcuts. |

## Learning science and scheduler decision

[Dunlosky et al., DOI 10.1177/1529100612453266](https://doi.org/10.1177/1529100612453266)
returned HTTP 403 at the DOI landing page. The
[Crossref record and abstract](https://api.crossref.org/works/10.1177/1529100612453266)
and [official APS summary](https://www.psychologicalscience.org/publications/journals/pspi/learning-techniques.html)
both returned HTTP 200. They explicitly rate practice testing and distributed
practice highly. This supports retrieval before feedback and later revisits; it
does not establish one universally optimal interval sequence or guarantee recall.

[Anki deck options](https://docs.ankiweb.net/deck-options.html) returned HTTP 200.
Its current manual documents daily limits, desired retention, FSRS and rescheduling.
[FSRS4Anki](https://github.com/open-spaced-repetition/fsrs4anki) and its
[raw README](https://raw.githubusercontent.com/open-spaced-repetition/fsrs4anki/main/README.md)
returned HTTP 200. The README distinguishes the scheduler from the optimizer,
which learns parameters from review history.

Recall Lab already delegates scheduling to
[coach.schedule](../../tracking/coach.py), the repository's authoritative tested
1/3/7/14/30-day rule. It uses actual assessment dates and distinguishes initial,
immediate, delayed, unknown-help and assisted evidence. Keep it. This redesign
does not implement FSRS and must not label its scheduler or metrics FSRS.

A future opt-in FSRS migration needs a versioned mapping between existing rubric
scores/assistance and FSRS grades, sufficient suitable history, preserved immutable
event IDs and timestamps, replay comparisons, a backup and rollback. Unknown
assistance and broad coding assessment cannot silently become independent card
recall. Current stage/due fields and valid existing dates remain authoritative.

## Safety and integration findings

- [SQL runner](services/sql_runner.py) uses in-memory fixtures, disabled extensions,
  an authorizer allowlist and bounded query/step/time/result sizes. Preserve its
  tested scope: SQLite SELECT challenges, not arbitrary databases.
- Python source is saved for human review and never passed to exec/eval or an
  unrestricted process. Run Tests must remain disabled until containment exists.
- [Journal](services/journal.py) commits submissions transactionally; duplicate
  tokens cannot overwrite an original answer. Export/import preserves drafts and
  annotations and rejects conflicts transactionally.
- [Checkpoint bridge](services/bridge.py) uses immutable evidence, stable IDs,
  consistent backups and canonical coach refresh/validate/recovery. New visual
  interactions must not bypass this path.
- Flagged during audit: the pre-existing additive migration did not create a
  pre-migration backup or reject a newer database schema. Integration added both
  safeguards before any DDL; the integration owner verifies the migration cases.
- Self-reported recall difficulty must stay distinct from measured correctness and
  scheduling. A local draft preference can persist it without revising an immutable
  scored attempt. Source consultation and hints continue to count as assistance.
- CSS alone cannot prove keyboard accessibility, contrast or responsive layout.
  Native Streamlit testing does not substitute for browser visual inspection.

## Executed verification

Before redesign integration, using the repository root virtual environment:

```powershell
.venv/Scripts/python.exe -m unittest discover -s apps/recalllab/tests -v
.venv/Scripts/python.exe -m unittest discover -s tracking/tests -v
```

Baseline: **43 application tests passed** in 32.5 seconds and **27 tracking tests
passed** in 10.1 seconds. These include all thirteen routes, exact-once checkpoint
recovery, import conflicts, assistance-aware scheduling, guarded notes, query
containment, calendar and draft recovery. Tests copy records into disposable
directories; synthetic answers are not live learner evidence.

The new [test_design.py](tests/test_design.py) adds five meaningful checks:

1. A daily task limit survives restart and a larger requested budget.
2. Lowering a limit preserves an existing plan and unfinished drafts.
3. Pause/restart/resume retains the answer without recording a scored event.
4. Blank submission cannot unlock a worked reference or create an attempt.
5. Submission, attestation, reveal and persistent subjective difficulty preserve
   the original scored attempt and protected canonical/project handoff records.

Focused run: **5/5 passed** in 5.9 seconds. Full integrated/browser results and
actual screenshots are recorded by the integration owner after all agents finish;
these baseline/focused results do not claim that later changes were already tested.

Known platform notices during baseline: Streamlit's bare-mode ScriptRunContext
warning from AppTest and a Streamlit/Pandas reset_index deprecation warning.
Neither caused a failed test. No dependency upgrade was performed for these notices.
