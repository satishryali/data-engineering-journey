# RecallLab development handoff

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
