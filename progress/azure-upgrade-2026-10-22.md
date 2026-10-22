# Azure preparation upgrade — 22 October 2026

Implemented on `feat/azure-de-interview-roadmap-2027`, targeting assessment on **22 January 2027**. This is repository infrastructure and planning, not learner achievement.

## Result and authority

- One authoritative curriculum: [learning-and-revision-plan.md](../plan/learning-and-revision-plan.md). It contains all thirteen dated weeks, prerequisites, concepts, independent practice, RRDAP applications, debugging, interview expectations and observable completion criteria for seventeen primary technologies. Its CSV is a generated compatibility view; the old vault plan is now a navigation link.
- [study-targets.json](../tracking/study-targets.json) owns date-effective reporting targets. Existing study-log.csv remains the interval authority. Weekday targets stay six hours through 21 October and become seven from 22 October; weekends stay ten. Full new weeks are 55 hours. Daily allocation is 1.5/2/2/0.5/1 hours on weekdays and 2/2.5/3/1/1.5 on weekend days for learning/practice/project/debugging/revision-interviews. Full-week activity totals are 11.5/15/16/4.5/8.
- [Interview preparation](../plan/interview-preparation.md) adds a weekly routine, January 75-minute mocks, five-dimension rubric and sixteen-category prompt format. Questions have difficulty, prerequisite and official source references; no solutions are embedded. Actual assessment metadata round-trips through existing review event_json and checkpoint deduplication. No second assessment ledger or new proficiency results.
- [Engineering simulation](../reference/engineering-simulation.md) supplies seven reusable record templates. Requirements and acceptance stay in project tickets, phase state in the RRDAP roadmap, and learning/time in existing authorities. No future project requirement is assigned or active solution generated.
- Existing five roles, checkpoint boundaries, 1/3/7/14/30-day review mechanism and fifteen command folders preserved. New natural-language interview/weakness requests route through existing roles. Installing updated command copies is optional and uses the existing installer; unrelated global settings were not changed.

## Curriculum and date validation

| Week | Dates | Focus |
| --- | --- | --- |
| 1 | 22–28 October | SQL, Python, incremental ETL |
| 2 | 29 October–4 November | Modelling, Docker, introductory PySpark |
| 3 | 5–11 November | PySpark transformations, joins, aggregations |
| 4 | 12–18 November | Spark execution/optimization, Delta |
| 5 | 19–25 November | Azure fundamentals, ADLS Gen2 |
| 6 | 26 November–2 December | ADF fundamentals |
| 7 | 3–9 December | Advanced ADF, Azure SQL |
| 8 | 10–16 December | Azure Databricks |
| 9 | 17–23 December | Databricks, Delta, integration |
| 10 | 24–30 December | Airflow, dbt Core |
| 11 | 31 December–6 January | Airflow, dbt, identity/security, Key Vault |
| 12 | 7–13 January | Azure DevOps, CI/CD, Monitor, testing |
| 13 | 14–20 January | RRDAP integration, revision, timed mocks |
| Buffer | 21–22 January | Verification, gap repair, final assessment |

Curriculum weeks run Thursday–Wednesday. Time reports stay Monday–Sunday. Historical first partial week target 32 h; transition 19–25 October 52 h; new-preparation portion 22–25 October 34 h; ordinary and year-boundary weeks 55 h; final preparation week 18–22 January 35 h. Thirteen full curriculum weeks 715 h plus buffer 14 h = 729 planned hours, never attendance. November 30 remains a stretch for a minimal RRDAP flow; Azure integration may continue in December. Long-term volume experiments are outside required January scope. Snowflake is secondary; Fabric/Synapse optional; Kafka, advanced Kubernetes and ML engineering excluded from required scope.

## RecallLab

Initial local checkout was behind remote main. Fetched and merged commit `aabba79`, which supplied the existing RecallLab implementation and earlier test-fixture repairs. Preserved that architecture and functionality. Resolved only reporting-date conflicts, regenerated inventory views and preserved canonical learning evidence. The earlier setup history accurately records that website source was absent from the initial checkout; the later integration checkpoint supersedes that engineering status.

Dashboard now shows shared daily/weekly targets, confirmed hours, actual pending task, planned focus, source-derived duration allocations and interview status. Added Learning Roadmap, Project and read-only Interview Practice routes. Analytics shows actual interview metadata and exact source-topic hours. Heatmap intensity uses date-effective targets. Existing coding editor, SQLite fixture tests, revision, notes, durable journal and checkpoint bridge remain. New views have no learning-record write side effects.

Automatic execution/grading of the new interview bank is deferred: attempts go to the tutor for assessment/checkpointing. Existing Python human-review fallback remains; no contained Python, PostgreSQL or PySpark runner was added. No new persistence claim is made for the read-only prompt view. No browser-based visual inspection was performed for this upgrade; headless Streamlit UI tests cover all routes. No public deployment or external access was enabled.

## Validation

Commands and outcomes:

- `python tracking/coach.py refresh --date 2026-10-22` and `validate`: pass; 33 review items, 28 concepts, 17 mistakes, 8 existing review events.
- `python -m unittest discover -s tracking/tests -q`: **27 pass**. Initially seven tests failed in the old checkout. Remote main fixed five; two remaining tests assumed no existing source-change flags. Their disposable fixtures now compare against the actual baseline while still checking new flags and unchanged dates. No real source hashes or scores were rewritten to satisfy tests.
- `.venv/Scripts/python.exe -m unittest discover -s apps/recalllab/tests -q`: **41 pass**, including every route, durable submissions/checkpoints/import/recovery, date-effective heatmap and read-only schedule/interview checks. Dependencies installed into ignored local .venv from the app's pinned requirement. Expected bare-mode Streamlit warnings are not test failures.
- `python -m unittest discover -s codex/tests -q`: **4 pass**. Three modified command skills also pass skill-creator validation.
- `python tracking/interview.py validate`: 16 prompts / 16 categories; selection exposes no answers. Isolated metadata persistence and repeat-checkpoint test passes without changing study-log.csv.
- `python tracking/check_links.py`: all repository-local Markdown/vault links resolve. External websites are not exhaustively crawled; Azure/Delta overview references were opened during planning.
- Excel rebuilt using existing artifact-tool builder, recalculated and rendered. Daily, Weekly, Sessions retained; Topics added with exact source labels. First/transition/ordinary/year-boundary/final-partial targets checked; post-deadline report extension checked, then restored to **22 October 2026**. Source, daily and topic confirmed-hour totals reconcile; formula-error checks pass. Preview images remain ignored.
- `git diff --check`: pass. Scoped added-text credential-pattern scan found no matching credentials; this is not a full-history security audit.
- Due weekly summary reconstructed from saved evidence as of 22 October, with partial historical tracking and uncertainty labelled. No missing hours, answered reviews or learning success inferred.

## Preserved records and next study action

Git blob hashes for study-log.csv, revision-queue.csv, revision-history.csv, mistakes.json and skill-state.json match remote main. Topic identities, source-version history, note-section mappings and prerequisites preserved; inventory file hashes/config exclusions reflect this checkout. Original learner attempts, notebooks, project input CSVs, RDS-001 brief, RetailFlow and legacy evidence unchanged. Existing valid due dates preserved. User's pre-existing Obsidian configuration change was excluded from commits. No Azure resources or large datasets were created; no study timer started.

Confirmed overall time remains **11h09m05s**; today/this week has **0 confirmed logged hours**, not proof that no study occurred. Timer remains paused since 17 October at 21:27:54 IST. RRDAP closed time remains 2h44m34s.

**Current unfinished task: RDS-001 Product Catalogue.** Next session: propose an approach or independently implement the 1,000-product PostgreSQL catalogue, then submit code and SQL verification against the six acceptance criteria. Preserve generator/CSV attempts. Stored catalogue acceptance remains unverified. Start today's learning loads this task without a timer; an explicit Start command begins study time.

## Exact file manifest

Compared with fetched remote main (`aabba79`). Generated files are labelled by their owning documentation; no imported unchanged app files are counted as new upgrade work.

- [AGENTS.md](../AGENTS.md)
- [Notes/learning-and-revision-plan.md](../Notes/learning-and-revision-plan.md)
- [Notes/revision/plan.md](../Notes/revision/plan.md)
- [README.md](../README.md)
- [START-HERE.md](../START-HERE.md)
- [apps/recalllab/ARCHITECTURE.md](../apps/recalllab/ARCHITECTURE.md)
- [apps/recalllab/HANDOFF.md](../apps/recalllab/HANDOFF.md)
- [apps/recalllab/README.md](../apps/recalllab/README.md)
- [apps/recalllab/app.py](../apps/recalllab/app.py)
- [apps/recalllab/components/learning.py](../apps/recalllab/components/learning.py)
- [apps/recalllab/services/records.py](../apps/recalllab/services/records.py)
- [apps/recalllab/services/routing.py](../apps/recalllab/services/routing.py)
- [apps/recalllab/tests/test_recalllab.py](../apps/recalllab/tests/test_recalllab.py)
- [apps/recalllab/tests/test_ui.py](../apps/recalllab/tests/test_ui.py)
- [codex/README.md](../codex/README.md)
- [codex/skills/learning-coach/SKILL.md](../codex/skills/learning-coach/SKILL.md)
- [codex/skills/progress-tracker/SKILL.md](../codex/skills/progress-tracker/SKILL.md)
- [codex/skills/todays-schedule/SKILL.md](../codex/skills/todays-schedule/SKILL.md)
- [outputs/study-tracker/study-hours.xlsx](../outputs/study-tracker/study-hours.xlsx)
- [plan/interview-preparation.md](../plan/interview-preparation.md)
- [plan/learning-and-revision-plan.md](../plan/learning-and-revision-plan.md)
- [plan/weekly-learning-plan.csv](../plan/weekly-learning-plan.csv)
- [progress/azure-upgrade-2026-10-22.md](../progress/azure-upgrade-2026-10-22.md)
- [progress/current.md](../progress/current.md)
- [progress/session-history.md](../progress/session-history.md)
- [progress/weekly/2026-W42.md](../progress/weekly/2026-W42.md)
- [projects/rrdap/README.md](../projects/rrdap/README.md)
- [projects/rrdap/checkpoint.md](../projects/rrdap/checkpoint.md)
- [projects/rrdap/roadmap.md](../projects/rrdap/roadmap.md)
- [projects/rrdap/templates/engineering-records.md](../projects/rrdap/templates/engineering-records.md)
- [reference/engineering-simulation.md](../reference/engineering-simulation.md)
- [reference/learning-coach.md](../reference/learning-coach.md)
- [reference/retailflow.md](../reference/retailflow.md)
- [reference/rrdap.md](../reference/rrdap.md)
- [reference/study-tracking.md](../reference/study-tracking.md)
- [tracking/README.md](../tracking/README.md)
- [tracking/check_links.py](../tracking/check_links.py)
- [tracking/checkpoint-index.json](../tracking/checkpoint-index.json)
- [tracking/coach.py](../tracking/coach.py)
- [tracking/interview.py](../tracking/interview.py)
- [tracking/interview/questions.json](../tracking/interview/questions.json)
- [tracking/study-targets.json](../tracking/study-targets.json)
- [tracking/study_plan.py](../tracking/study_plan.py)
- [tracking/tests/test_coach.py](../tracking/tests/test_coach.py)
- [tracking/tests/test_study_plan.py](../tracking/tests/test_study_plan.py)
- [tracking/topic-map.json](../tracking/topic-map.json)
- [tracking/update-study-tracker.mjs](../tracking/update-study-tracker.mjs)
