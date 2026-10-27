# RecallLab

## Expanded bank checkpoint, 27 October 2026

**4,213 published problems; the 4,200 allocated target is met.** 243 draft candidates are excluded from counters and selection. The original 53 problems and their IDs are preserved. The existing Tools page now supports /problem, /hint, /stuck, /solved, /next, /review, /progress and /why; hints count as assistance. It shows current level, next challenge, per-tool/overall actual progress, a published challenge browser and a 209-problem curated Job-Ready pathway with four practical assessments. [Actual counts, validation and review limits](BANK-EXPANSION.md); [machine-readable manifest](../../tools/problem-bank/manifest.json). The older 53-problem description below records the initial batch.

Local daily revision over this repository's existing learning records. Website: **http://127.0.0.1:8501**. No new repository, cloud account or database server is needed.

## Problem-first Tools practice, 26 October 2026

Open **Tools**, choose a technology, type /problem, implement the bounded business task, then type /solved. Submit your approach, all help sources, code/file contents and actual output. SQL problems run bounded read-only SQLite fixtures; their results show actual versus expected rows. Python, PostgreSQL, Spark and cloud artifacts require an explicit human review of actual results, edge cases and acceptance criteria. RecallLab does not automatically execute those submissions. A declaration alone never completes a problem.

Version 2026.10.26.1 publishes **53 problems across 32 technologies**: Python 12, SQL 8, PostgreSQL 4, and one starting task for each other tool. Every technology has Level 0–10 stage plans; unpublished stages are clearly excluded from totals. The bank expands in reviewed versioned batches. Existing folder IDs, PL/SQL and SAP HANA are retained; advanced tools remain available for later development. [The manifest](../../tools/curriculum.json) owns exact problem IDs, priorities, dependencies, published totals and official references.

Verified assisted work counts as completed. Independent mastery needs separate explicit no-help evidence; after assisted completion use a later changed-input followup. **Verify existing skills** offers bounded diagnostics where published: independent verification may cover specific earlier prerequisite skills without adding unsubmitted problems to the completed count. Pending/failed attempts retain their original evidence and never erase prior progress. Version changes display old/new totals for acknowledgement. Optional aggregate practice totals do not claim a readiness percentage.

Submissions/drafts save to the existing journal. **End session / save checkpoint** uses the existing bridge: immutable evidence, actual exercise review items, mistake observations, skill dimensions and the coach scheduling rule. Unsaved followup dates are provisional; checkpointed review dates come from the canonical queue. No new scheduler or timer is added. Checkpointed problem progress is recovered from canonical events on another computer, while unfinished drafts still need the existing journal export/import. Use Tools for problem verification and completion counters; existing Question Bank/revision pages can display registered exercise briefs without inventing note concepts.

The [single roadmap](../../plan/learning-and-revision-plan.md) now targets **20 January 2027**, with November 15 foundation, December 6 PySpark and December 27 Azure assessments. Applications can begin now using truthful demonstrated skills. Infrastructure changes add no learner scores or RDS-001 acceptance.

## Revision-first redesign, 26 October 2026

All thirteen pages share charcoal surfaces, mint actions, readable spacing, visible
keyboard focus and reduced-motion support. The dashboard leads with Start Today's
Revision; annual activity and the learning plan are secondary. Counts come from
saved evidence. Coding uses problem/editor panes with an adjustable width control;
on phones the panes stack. Notes and original learner attempts remain unchanged.

Daily sessions support durable pause/resume, answer reveal after a submitted recall
attempt and attestation, and separate difficulty self-reports. Ctrl+Enter submits
or resumes; Ctrl+Shift+Enter reveals; Ctrl+Right advances a submitted task. Shortcuts
are displayed by supported Streamlit versions. Pause saves app state and does not
operate the study timer. Settings' daily task limit bounds new plans; saved work is
never truncated. The existing coach remains the scheduler; no FSRS is claimed.

Mistakes now offer search, saved correction/help, recurrence evidence, actual next
review dates and a practice link. Search and question filters explain empty results.
Analytics separates concept coverage, assessed outcomes and activity. Existing
database upgrades create a consistent pre-migration backup and refuse newer schemas.

See [design plan](REDESIGN-PLAN.md), [research and audit](REDESIGN-QA.md),
[final verification](REDESIGN-RESULTS.md) and [actual screenshots](screenshots/).
Python execution remains unavailable without containment; SQLite challenges retain
their tested runner. Browser screenshots/tests use disposable copies of records.

## Azure preparation upgrade, 22 October 2026

Dashboard now reads date-effective daily/weekly targets and source-derived activity allocations from the repository roadmap/target policy. Historical six-hour weekdays stay unchanged; weekdays from 22 October are seven hours, weekends ten. Heatmap intensity uses the appropriate date's target. The transition week is 52 h, ordinary full weeks 55, final preparation partial week 35.

Learning Roadmap displays thirteen planned weeks and the 21–22 January verification buffer. Project reads the existing RRDAP checkpoint, RDS-001 acceptance criteria and phase roadmap. Interview Practice presents the sixteen-category prompt bank without answers or new assessment writes. Share interview attempts with the tutor for review/checkpointing through existing authorities. Progress & Analytics shows saved interview metadata and exact source-topic hours; unassessed categories stay unassessed. Existing Coding Challenges, notes, journal, human review and checkpoint bridge remain in place.

Automatic grading/execution of these new interview prompts is deferred. Existing SQL fixture tests and manual Python assessment retain their supported scope; no PostgreSQL/PySpark runner or new timer system was introduced. No public deployment or Azure resources were created. The only roadmap authority is [the repository plan](../../plan/learning-and-revision-plan.md).

## Start in Windows PowerShell

From the repository root, using Python 3.12+ (verified on 3.13.7):

```powershell
python -m venv apps/recalllab/.venv
& apps/recalllab/.venv/Scripts/python.exe -m pip install -r apps/recalllab/requirements.txt
Set-Location apps/recalllab
& .venv/Scripts/python.exe -m streamlit run app.py
```

If Streamlit is already installed, run from `apps/recalllab`:

```powershell
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501 --browser.gatherUsageStats false
```

This directory's `.streamlit/config.toml` supplies the dark theme, localhost binding and disabled usage statistics. Keep the terminal open. Ctrl+C stops the website without changing tutor study timers. Restart after code updates if an older imported component remains loaded.

## Daily use

1. Choose **Start Today's Revision**. The dashboard shows actual due/overdue rows, weak concepts, note sections and suggested coding practice.
2. Work through the saved mixed-format plan, usually about 20 minutes. Targets and prerequisites come from the existing coach. At most one unassessed concept is introduced through its selection. A larger budget extends the plan without discarding answers. No study timer starts.
3. Attempt before consulting notes. Hints/source consultation and other help are recorded. Unknown help cannot earn independence. Explanations and manual code remain unscored until reviewed.
4. Submit Attempt durably saves before displaying **Saved locally / pending sync**. Next Task advances the saved cursor. Restart restores the plan, task and draft. Draft text saves when the field loses focus; press Tab or click outside before closing.
5. SQL Run Query checks outputs against three disposable SQLite fixtures. Python Run Tests stays disabled without verified containment. Python/text submissions have a **Human assessment** form requiring reviewer, observed verification/output, feedback, rubric score and attestation. It preserves the original answer and assistance. A human report is labelled human_review, never executable test evidence.
6. Use **End session / save checkpoint**. The bridge freezes the exact batch, saves immutable attempt evidence, makes a consistent local backup and calls the existing coach recovery/record/refresh/validate workflow. A completed Notes to Review report lists at most three actual gaps, exact headings, triggering questions/answers, evidence and changed follow-ups. Partial sessions can be saved; unevaluated answers keep null scores.
7. The next completed-session cycle chooses current targets and different formats/inputs, avoiding used variant IDs. An unfinished plan resumes rather than silently regenerating questions.

Extra concept practice and Coding Challenges are also available. The coding page shows submitted source, fixture feedback and saved code history. Revision completion never changes active RRDAP files, `progress/current.md`, `START-HERE.md` or study timers.

## Activity is separate from proficiency

- The calendar has exactly 365 IST dates, seven weekday rows, month labels, uniform squares, tooltips and root-based date links. Narrow containers scroll instead of squeezing cells.
- All Learning uses merged confirmed closed intervals, split at IST midnight, and actual answered learning events. Overlaps are not counted twice. Running/uncertain intervals, page views, notes opened and generated plans add no activity.
- Revision Only counts delayed reviews or explicitly submitted revision-session answers. Initial learning, ordinary application and unlabelled corrections are excluded. It opens by default in Revision Calendar and has its own streak.
- Coding Practice requires explicitly linked code evidence. Failed genuine attempts count as activity, not correctness.
- No question counts are converted into hours; revision/coding duration is **Not measured** when absent. Review events do not add minutes already included in study intervals.
- Study thresholds use 6h weekdays / 10h weekends; the highest level defaults to 125% of target. Settings separates study, revision and coding thresholds.
- The existing coach alone owns 1/3/7/14/30-day stages. Initial/application, immediate correction and delayed retrieval stay distinct. Different tasks on the same day do not advance delayed retention. Human review uses its actual assessment date for scoring/scheduling, preserves the original submitted date for activity, and cannot claim delayed retrieval.
- Passing output tests assess only the tested dimension. Assisted, independent, partial, failed, unassessed and human-reported outcomes remain separate. Hours and notes never imply mastery.

## Navigation and notes

All generated links use root URLs such as `/?view=Notes+Browser&note=...`; day links cannot inherit `/list-plus.md`. Sidebar changes synchronize selection, title and URL while clearing stale note parameters. Calendar date/metric, note section, search and bank filters persist locally. The page menu also works on mobile or when the sidebar is collapsed.

Notes Browser reads the original vault without rewriting it. Select a heading, follow guarded Markdown/wiki links, see local raster images, and inspect related concepts, actual mistakes and exercises. Code blocks remain text. Mapping/source changes warn without resetting history. SQL SUM has an existing standalone-note deferral and real exercise evidence; no missing explanation is invented.

## Storage and automatic saving

| Location | Purpose | Git behavior |
| --- | --- | --- |
| `data/recalllab.sqlite3` | Plans, cursor, drafts, pending submissions, manual annotations, preferences and cached explanations | Ignored; local only |
| `data/backup-*.sqlite3` | Consistent completion snapshots and Settings backups | Ignored; preserve safe copies |
| `evidence/ATT-RL-*.json` | Immutable original question/answer/code/help plus test or human-review evidence | Track intentionally with checkpoint changes |
| Existing `tracking/*` | Canonical review history, queue, mistakes, skill observations and IDs | Existing Git workflow |
| `progress/session-history.md` | Actual checkpoint outcomes, evidence and recommended sections | Existing Git workflow |

Every submitted answer uses a SQLite transaction before success. A manual annotation retains the original submission. Canonical records change only through the explicit session-completion checkpoint. Replaying the same attempt/review/checkpoint IDs does not create duplicate scores. Website engineering notes live in HANDOFF.md, separate from learning history.

## Recovery and computer switching

**Interrupted checkpoint:** choose Retry interrupted checkpoint in Today's Session or Settings. The frozen batch keeps the same IDs and can recreate missing immutable evidence after a journal import. Concurrent edits are refused and preserved. From the repository root, existing helper recovery is also available:

```powershell
python tracking/coach.py recover
python tracking/coach.py validate
```

**Stale inventory:** inspect the warning, use the existing `notes-sync --date YYYY-MM-DD` with the actual IST date, map genuinely new sections and refresh/validate. The bridge synchronizes metadata at a genuine checkpoint but refuses missing mappings. Do not clear warnings by inventing a learning event.

**Backup/export:** Settings makes consistent SQLite backups and exports the complete pending journal as JSON. Import your trusted export through Settings. Import is transactional and idempotent; conflicts preserve existing data and show an error. No import automatically pushes or creates canonical reviews. Frozen batches cannot import arbitrary handoff-write fields.

**SQLite restore:** stop RecallLab, preserve the current database under a safety filename, copy a trusted snapshot to `data/recalllab.sqlite3`, then restart and retry completion. JSON import is usually easier. Backups contain private answers; keep them safe. Do not replace canonical trackers with a cache.

Before switching computers:

1. Complete the session and confirm its canonical checkpoint/report.
2. Intentionally review, commit and push its evidence, tracker, derived-view and session-history changes using the existing Git workflow.
3. Export any still-pending local journal. Ignored SQLite files and uncommitted edits do not automatically travel through GitHub.
4. Preserve edits on the other computer, pull safely, install/start RecallLab and import a trusted pending export if necessary. Work with one writer at a time.
5. Fresh AI chats read START-HERE.md, canonical tracking files and session-history.md. Read apps/recalllab/HANDOFF.md for website engineering state.

## Optional AI and safe execution

Offline questions and evaluation always work without AI. Optional **local Ollama** is off by default. If already installed, start it with `ollama serve`, inspect installed models using `ollama list`, and configure its base URL/model in Settings. Enable the explicit local-note-sharing opt-in. Ask local explanation, available after submission, sends only that question/answer and its source section to the configured loopback endpoint. Feedback is unverified and cached locally; it cannot grade, run tests or change history. Unavailable models/network errors leave offline practice working. Remote endpoints and redirects are rejected. No provider/model was installed or contacted during development. [Ollama API reference](https://github.com/ollama/ollama/blob/main/docs/api.md)

No verified contained Python runner is configured. RecallLab never executes submitted Python using exec/eval or an unrestricted subprocess. Its working fallback is saved source plus human review with observed verification evidence. Installing Docker alone would not prove isolation; a future runner needs tested network/filesystem/credential isolation and CPU/memory/time limits before enabling Run Tests. SQLite queries use disposable in-memory databases, disabled extensions, an authorization allowlist and bounded input/instructions/time/results. PostgreSQL-specific and PySpark execution are unsupported.

## Verification

From the repository root:

```powershell
python -m unittest discover -s tracking/tests -v
python -m unittest discover -s apps/recalllab/tests -v
git diff --check
```

Synthetic submissions run only in disposable checkout copies. Checks cover every page, stale-note navigation, root URLs, refresh/date/filter/draft/task recovery, plan variation, manual-review/report UI, partial executable results, immutable originals, import conflict rollback, interrupted checkpoints, overlapping IST time and preserved project/timer state. Browser checks cover desktop and mobile without fake live submissions.

See AUDIT.md for gaps identified before coding, ARCHITECTURE.md for authority mapping, and HANDOFF.md for actual verification results. The initial supplied implementation brief is retained in BUILD_RECALLLAB.md.
