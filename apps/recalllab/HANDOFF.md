# RecallLab development handoff

## Bank expansion checkpoint - target met, 27 October 2026

The existing Tools bank now has **4,213 published problems** and **243 drafts excluded from publication**. The 4,200 allocated target is met. Specialized agents authored separate foundations, Spark/Azure, engineering and integrated files. Low-distinction generated variations and Git tasks without history fixtures remain drafts. [Expansion audit](BANK-EXPANSION.md) records actual per-track counts, root cause of the previous 53 limit, implemented commands, the curated 209-problem pathway and validation and future editorial work. Main manifest/version is 2026.10.27.7. Existing learner evidence/timers and RDS-001 remain unchanged. No commit, push, deployment or autonomous generation.

## Current implementation revision, 26 October 2026

The existing app now has Tools: select technology, `/problem`, implementation,
`/solved`, approach/help/artifacts/results, verification, separate completion and
independent counters, and the next eligible challenge. Three implementation agents
worked on the curriculum, problem service and Tools UI; one tutor still owns the
five learning responsibilities. Existing uncommitted redesign work was preserved.

[The published manifest](../../tools/curriculum.json) has version 2026.10.26.1,
32 technologies and 53 actual problems (Python 12, SQL 8, PostgreSQL 4 and 29 tool
starters). Every tool retains Levels 0–10 plans; advanced stages remain unpublished,
outside the denominator. All 53 problems include changed-input followups. Explicit
independently reviewed diagnostics cover selected prerequisite skills without
counting skipped problems completed. Expansion notices show old/new totals.
All 32 official reference URLs were fetched; primary capability excerpts and
reachability-only checks are distinguished in the manifest.

SQL SELECT tasks use bounded disposable SQLite fixtures. Other implementation
artifacts need human review with actual output, edge checks and acceptance
attestation. No Python, PostgreSQL, Spark or cloud execution is claimed. SQL
diagnostics also need human verification of skills beyond query output. Unknown
help never earns independence; assisted completion is preserved, with later
changed-input practice. No autonomous AI grading was added.

Journal drafts/attempts/assessments use existing export/recovery. The checkpoint
bridge lazily registers actual problem exercise IDs in the canonical review queue,
preserves immutable evidence and uses coach scheduling/mistakes/skill records.
No fabricated note-concept mappings or extra scheduler. Canonical events restore
verified counters after computer changes; pending drafts still need journal export.
Existing question/revision routes can display the newly registered exercises.

The single roadmap now targets **20 January 2027**, with November 15 foundation,
December 6 transformation and December 27 Azure demonstrations. The final partial
reporting week has 21 planned hours; thirteen curriculum weeks total 715 planned
hours. No study interval, learner assessment or RDS-001 acceptance was added.
Main/project handoffs retain their exact pending learner work.

Verification on this revision: **102 app tests and 27 tracking tests passed**,
including seven Tools AppTests, all published SQL fixtures, dependency/bridge
validation, acceleration, submission/review, assistance, failures/mistakes,
counter deduplication, canonical/export persistence, checkpoint scheduling and
existing UI/recovery regressions. `coach.py validate`, Python compilation and
`git diff --check` passed. Synthetic assessments ran only in disposable journals
and record copies. No commit, push, deployment or cloud provisioning performed.

22 October 2026 upgrade: integrated this implementation from remote main into the Azure-roadmap feature branch. Added shared date-effective targets in heatmap/dashboard, source-derived daily allocations, Learning Roadmap, Project and read-only Interview Practice views, plus interview evidence/source-topic summaries in analytics. Existing journal/coding/revision/checkpoint flows preserved. RDS-001 remains pending; no genuine assessment or timer event created. Final upgrade validation is recorded in [upgrade report](../../progress/azure-upgrade-2026-10-22.md). No public deployment.

Completed supported local/manual release on 18 October 2026 IST. App: http://127.0.0.1:8501. Implementation and current brief are under apps/recalllab; see COMPLETION_BRIEF.md, AUDIT.md and README.md. No commit, push or deployment performed.

## Implemented

- Screenshot-based dark dashboard; fixed square calendar cells; responsive navigation including a collapsed-sidebar menu and working native expand button.
- Root-absolute allowlisted routes; sidebar, note sections, calendar date/metric, challenge and practice mode synchronize URL and persisted preferences. Notes links never become unrelated Markdown paths.
- Revision Only counts actual delayed reviews or explicitly recorded revision submissions. Initial learning/application/correction remain separate. No fabricated revision minutes or accuracy. Closed study intervals are unioned before IST midnight splitting.
- Frozen daily mixed-format plans use existing coach targets/prerequisites and actual note references. Drafts, cursor, variants and budget extensions survive restart. Extra concept practice remains available.
- Submitted evidence saves transactionally before success. SQL runs bounded SELECT-only queries against disposable SQLite fixtures. Partial, failed, assisted and unknown-help results remain distinct.
- Python and text submissions use explicit human assessment with reviewer, observed verification, feedback, rubric and attestation. Original answers/help remain immutable. Human annotations cannot claim executable-test or delayed-retention evidence.
- End-session checkpoint uses existing coach record/recover/refresh/validate APIs with stable IDs, frozen batch, immutable evidence, consistent backup and duplicate protection. Completed report includes targeted note sections and follow-ups.
- Notes Browser renders original Markdown, code, guarded links and local images; heading selection and related concepts/mistakes/exercises are available.
- Settings supports backup, full pending-journal JSON export and transactional idempotent import. Conflicts preserve local data. Imported frozen batches can reconstruct missing attempt evidence before recovery.
- Optional local Ollama explanations are off by default, require explicit opt-in and a post-submission request, reject external endpoints/redirects and cannot grade or update records. No model/provider was installed or contacted.

## Verification

- Final RecallLab suite: 39 tests passed; canonical tracker suite: 20 tests passed. Synthetic submissions use temporary checkout copies.
- Service and UI checks cover all pages, URL/refresh/filter/draft/task persistence, question variation, human assessment through checkpoint/report, duplicates, SQL fixtures/rejections, import conflicts, interrupted completion, IST overlap and missed-day streaks.
- Desktop Chrome and 390 x 844 mobile checks passed. Mobile navigation opened Coding Challenges; desktop Notes-to-Coding navigation and refresh matched content. Temporary viewport override removed. Final dashboard refreshed without exceptions or inventory warning and left open.
- Python 3.12 grammar checks, git diff --check and local health endpoint passed. Expected bare-mode Streamlit test warnings do not indicate test failures.
- coach.py validate passes: 33 review items, 28 concepts, 17 mistakes, 8 review events.
- Resolved stale notes inventory using notes-sync --date 2026-10-18: only new Obsidian graph.json configuration was excluded; no changed learning sections, missing mappings or reassessment flags. Metadata/derived inventory views updated. Hashes confirmed history, queue, mistakes, skills, study log, checkpoint index, current/handoff/history and RRDAP checkpoint unchanged.
- No genuine revision was submitted during development: current revision activity remains zero. Existing workbook/practice CSV changes remain untouched.

## Limits and next step

No verified contained Python runner is installed: Run Tests stays disabled, with working saved-source/human-review fallback. SQL supports SQLite fixtures; PostgreSQL-specific and PySpark execution are unavailable. Optional AI needs an installed/running Ollama model and explicit Settings opt-in. Single writer only; local SQLite drafts do not automatically synchronize through Git.

No remaining engineering task blocks the supported release. Start a genuine daily revision in the browser. A future Python runner must demonstrate filesystem, network, credential and resource isolation before enabling execution.

## Start and recovery

From repository root in PowerShell:

```powershell
Set-Location apps/recalllab
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501 --browser.gatherUsageStats false
```

Use Retry interrupted checkpoint after a failed completion. Preserve the current database before restoring a trusted backup; Settings can import a trusted pending export. Complete/save before computer switching, intentionally sync canonical evidence/trackers through Git, and separately export pending local work. Full install, backup, synchronization and optional AI instructions: README.md. Learning continuity remains START-HERE.md and authoritative trackers; this file records engineering only.
26 October 2026 redesign: all thirteen routes now share charcoal/mint styling;
home prioritizes revision, sessions add durable pause/resume, gated reveal and
separate difficulty self-report, coding has adjustable problem/editor panes,
mistakes have search/due-date practice actions and analytics has readable coverage.
Existing uncommitted fixes were retained. 54 app tests, 27 tracking tests and 26
desktop/mobile route checks passed, plus browser interaction scenarios in scratch
data. Learning records/handoffs remain byte-identical; no learning result or timer
was created. See [results and screenshots](REDESIGN-RESULTS.md),
[design plan](REDESIGN-PLAN.md) and [source research](REDESIGN-QA.md).
