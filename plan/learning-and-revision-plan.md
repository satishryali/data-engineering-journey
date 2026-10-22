# Azure Data Engineer learning and revision plan

Agreed 22 October 2026. Preparation: **22 October 2026–22 January 2027**, Asia/Kolkata (IST). Goal: independently solve practical Azure Data Engineer and interview problems for India, especially Hyderabad. The date is an assessment target, not a job, salary or mastery promise.

This file owns curriculum, weekly milestones and activity allocation. [study-targets.json](../tracking/study-targets.json) owns date-effective hour targets for reporting code. [weekly-learning-plan.csv](weekly-learning-plan.csv) is generated with `python tracking/study_plan.py --refresh-roadmap`; never maintain a second plan there. Actual progress comes from [current checkpoint](../progress/current.md), project acceptance and canonical tracking records.

## Starting position

The learner reports 4–5 years in database development and production support, with SQL/PLSQL and SAP HANA, plus exposure to Python, PostgreSQL, Snowflake, Git, Docker, Airflow, dbt Core, PySpark and basic Kubernetes/Spark experiments. Windows laptop, Ubuntu server, PostgreSQL and distributed Spark lab are reported; verify access and capacity when relevant. Keep prior employment separate from educational project experience. Reported familiarity is not verified mastery.

Needs: independently build complete solutions, implement realistic pipelines, retain older concepts, revise regularly and explain work confidently. Use a short independent diagnostic before extensive repeat teaching. Preserve actual SQL/Python independent and assisted evidence; never reset scores because of this plan.

**RRDAP remains active; RDS-001 Product Catalogue remains in progress.** Generator/CSV evidence exists; PostgreSQL loading and six SQL acceptance checks remain unverified. Earlier Python CSV output/read-back and SQL-003 remain deferred. RetailFlow remains historical. Follow the exact next task in the checkpoint.

## Daily focused study budget

From **22 October** use seven hours Monday–Friday and ten hours Saturday/Sunday: **55 hours/full week**. Before that date keep six-hour weekdays and ten-hour weekends. Breaks, meals, sleep and unrelated work are excluded. Only legitimate timer entries establish actual hours. Report shortfall; reduce scope if this schedule is unsustainable, without inventing catch-up work.

| Activity | Weekday hours | Weekend hours per day | Weekly hours |
| --- | ---: | ---: | ---: |
| Learn new technology | 1.5 | 2 | 11.5 |
| Independent practice | 2 | 2.5 | 15 |
| RRDAP implementation | 2 | 3 | 16 |
| Debugging, testing and production scenarios | 0.5 | 1 | 4.5 |
| Revision and interviews | 1 | 1.5 | 8 |
| Total | 7 | 10 | 55 |

Arrange duration blocks around actual availability, with breaks outside focused time. No new reminders or fixed clock slots are assumed. Start revision with about ten minutes of weak/due retrieval and at most five minutes for one diagnostic, then use the rest for reconstruction, changed examples and interviews. Docker stays inside this budget. The old one-Azure-concept-per-week limit is superseded by this prerequisite-based sequence.

Curriculum weeks are Thursday–Wednesday. Hour reports stay Monday–Sunday: historical 15–18 October target **32 h**; transition week 19–25 October **52 h** (three old weekdays, two new weekdays and weekend); new preparation portion 22–25 October **34 h**. Ordinary weeks **55 h**; final preparation week 18–22 January **35 h**. Thirteen curriculum weeks total **715 h**, plus **14 h** for 21–22 January: **729 planned preparation hours**, never actual attendance.

## Thirteen-week curriculum

All rows are planned. Calendar advancement does not complete a milestone. Carry unmet prerequisites forward and reduce optional depth first. Without Azure access/budget use a labelled local implementation plus architecture exercise; actual cloud execution remains unverified.

| Week | Start IST | End IST | Primary focus | Azure connection | Observable milestone | Hours |
| --- | --- | --- | --- | --- | --- | ---: |
| 1 | 2026-10-22 | 2026-10-28 | SQL, Python, incremental ETL | Source-to-cloud boundaries | Continue RDS-001 first; validate a small changed-record load and explain reruns when prerequisites are met | 55 |
| 2 | 2026-10-29 | 2026-11-04 | Data modelling, Docker/Compose, introductory PySpark | Relational versus lake storage | State grain and keys; model a small star; reproduce a bounded runtime and typed DataFrame | 55 |
| 3 | 2026-11-05 | 2026-11-11 | PySpark transformations, joins, aggregations | Portable processing | Reconcile SQL/Spark totals on changed input with nulls and duplicate keys | 55 |
| 4 | 2026-11-12 | 2026-11-18 | Spark execution, optimization, Delta Lake | Lakehouse boundary | Read a physical plan; measure a change; verify merge reruns and schema checks | 55 |
| 5 | 2026-11-19 | 2026-11-25 | Azure fundamentals and ADLS Gen2 | Identity, storage and cost | Document a least-privilege small storage experiment and cleanup; label cloud versus local evidence | 55 |
| 6 | 2026-11-26 | 2026-12-02 | Azure Data Factory fundamentals | Linked services, datasets, runtime | Parameterize a small copy pipeline; inspect run evidence; reassess November stretch scope | 55 |
| 7 | 2026-12-03 | 2026-12-09 | Advanced ADF and Azure SQL | Incremental copy and relational sink | Verify watermark commit behaviour, retries and rerun results | 55 |
| 8 | 2026-12-10 | 2026-12-16 | Azure Databricks | Compute, jobs, storage access | Parameterize a bounded job; capture validation, failure logs and termination settings | 55 |
| 9 | 2026-12-17 | 2026-12-23 | Databricks, Delta and pipeline integration | ADF-to-job boundary | Reconcile an accepted project slice and demonstrate a safe end-to-end rerun | 55 |
| 10 | 2026-12-24 | 2026-12-30 | Apache Airflow and dbt Core | Orchestration boundaries | Run a small dependency graph and tested models; explain intervals without duplicate scheduling | 55 |
| 11 | 2026-12-31 | 2027-01-06 | Airflow, dbt, Azure security and Key Vault | Secure configuration | Verify a bounded backfill and changed dimension; diagnose redacted access failure | 55 |
| 12 | 2027-01-07 | 2027-01-13 | Git, Azure DevOps, CI/CD, Monitor and testing | Delivery and alerts | Validate a change in CI; rehearse rollback; inspect monitoring for a labelled failure | 55 |
| 13 | 2027-01-14 | 2027-01-20 | RRDAP integration, revision and timed mocks | Architecture tradeoffs | Independently rebuild/repair an unfamiliar slice; give timed coding, design and project explanations | 55 |

**21–22 January: verification buffer and final assessment (14 planned hours).** Re-run acceptance, reconcile counts, inspect security/cost cleanup and repair priority gaps. Assess on 22 January from actual evidence and document unfinished work. Do not convert planned rows into completions.

## Technology requirements

The following are planning themes, not future requirements or solutions to reveal during RDS-001. Each row also requires a changed-input reconstruction and later **1/3/7/14/30-day retrieval** under the shared guide. Completion requires reviewed implementation, debugging and explanation evidence with help recorded; assisted completion does not imply independence or retention.

| Technology | Prerequisites | Concepts | Independent practice | RRDAP application | Debugging scenario | Interview expectation | Observable completion evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SQL | Tables/keys; saved gap review | Joins, nulls, grouping, windows, dates, transactions, indexes, plans | Unfamiliar customer-preserving report and latest-row query | Catalogue checks and reporting totals | Filter drops customers or join multiplies totals | Explain grain, nulls and query plan | Executed correct queries, edge cases and unaided variant |
| Python | Records/functions; guided cleaner evidence | Files, types, exceptions, modules, logs, DB transactions, tests | Reconstruct a small validator/loader | Bounded ingestion and business generation | Malformed price, partial write or input mutation | Explain error boundaries and safe DB writes | Runnable code, rejection evidence, preserved input and tests |
| DE fundamentals | SQL/Python baseline | Batch/incremental, ETL/ELT, watermark, CDC concepts, idempotency, quality | Test initial/changed/repeated loads | Consistent business-to-analytics movement | Watermark advanced before failed write | Compare CDC/timestamp loading and recovery | Counts reconcile across successful, repeated and failed loads |
| Data modelling | Joins, business keys | Grain, facts/dimensions, star, surrogate keys, SCD1/2 | Model small dated changes and reports | Historical retail analytics | Overlapping SCD2 validity or duplicate facts | Defend grain and history choices | Diagram and key/grain/as-of SQL checks |
| PySpark | Python/SQL, typed DataFrames | Schemas, transformations, joins, windows, partitions, lazy execution, shuffles, plans | Transform unfamiliar data and compare SQL | Processing when measured needs justify it | Skew, cast nulls or join explosion | Explain action, shuffle and measured tuning | Correct output plus plan/runtime evidence |
| Delta Lake | Spark/Parquet, keys | Log, merge, history, schema enforcement/evolution, partitions | Apply inserts/updates twice; inspect history | Reliable incremental analytical tables | Duplicate merge keys or schema mismatch | Compare Delta/Parquet and replay safety | Verified contents, rejected schema, history and rerun |
| Azure fundamentals | Storage/compute/network concepts | Tenant, subscription, group, region, Entra, budgets | Explain ownership and price a tiny experiment | Select one justified cloud slice | Wrong scope/region or unexpected cost | Explain responsibility and cost controls | Architecture/cost/cleanup plan; actual access labelled |
| ADLS Gen2 | Azure identity/storage, formats | Hierarchical namespace, paths, RBAC/ACL, lifecycle | Read/write a small partition; test access | Inspectable source landing/retention | Permission denied or wrong path | Explain namespace, ACL/RBAC and layout | File/count/access evidence or labelled local substitute |
| ADF | Contracts, ADLS, identity | Linked services, datasets, activities, parameters, triggers, runtime, retries, watermarks | Parameterize copy; test success/failure/rerun | Justified ingestion orchestration | Connection/mapping or partial-copy failure | Diagnose activity output and watermark safety | Redacted run evidence and two-load reconciliation |
| Azure Databricks | Spark/Delta, ADLS, identity | Workspace, compute, jobs, parameters, access, cost | Run a bounded parameterized job | Managed Spark slice when justified | Missing permission/library or failed task | Explain compute/job/storage boundaries | Reproducible job/config/logs; cloud gaps explicit |
| Azure SQL Database | SQL, transactions, Azure network | Managed relational DB, connectivity, indexing, transactions | Load/update a small table; verify rollback | Cloud relational sink/serving slice | Timeout, firewall scope or partial transaction | Compare local PostgreSQL and managed SQL | Correct commit/rollback results and diagnostics |
| Key Vault and identity/security | Entra/RBAC, network boundary | Managed identity, least privilege, secret references, rotation | Explain identity flow; test allowed/denied access | Externalized secrets when needed | Expired secret or wrong scope/identity | Separate identity and data-access failures | Redacted access evidence and rotation/revocation procedure |
| Git and Azure DevOps | Git, tests, reproducible runtime | Branch/PR, CI/CD, environments, approvals, rollback, variables | Review/test a change; simulate failed build/rollback | Delivery workflow | Missing dependency or environment mismatch | Explain CI/CD and deployment evidence | Reviewed diff, CI output and rollback rehearsal |
| Azure Monitor/troubleshooting | Runnable pipeline, logs | Correlation, metrics, alerts, latency, isolation | Trace a labelled failure; propose useful alert | Operational investigation | Successful task with incorrect counts | Explain detection, mitigation, cause and prevention | Redacted incident evidence, tested fix and regression |
| Apache Airflow | Python, rerun safety, dependencies | DAG/tasks, data intervals, retries, backfills, connections | Schedule existing slice; bounded historical rerun | Distinct orchestration role from ADF | Wrong interval, duplicate side effect or failed dependency | Explain logical date and retry boundaries | Actual task/backfill results without duplicate business rows |
| dbt Core | SQL, modelling, connection | Sources/ref, staging/marts, tests, docs, incremental, snapshots | Build/test models with small changed input | Tested analytical SQL | Failed unique test, grain or incremental predicate | Explain materializations, tests and SCD options | Build/test logs and full/incremental reconciliation |
| Docker/Compose | CLI, Python dependencies, ports | Images/containers, Dockerfile/cache, network, volumes, health/readiness | Reproduce small loader/database runtime | Reproducible local environment | Service-name connection or startup readiness | Explain persistence, ports and config | Clean startup/recreation with retained data and versions |

## Dependencies and scope

SQL/Python and RDS-001 acceptance precede added project sources. Modelling precedes historical marts. Spark correctness precedes tuning/Delta. Azure identity/storage precede ADF/Databricks integration. Teach security/cost basics at the first cloud experiment, with deeper assessment in week 11. Git/tests apply throughout; delivery integration follows in week 12. Diagnose reported Airflow/dbt familiarity before allocating extensive repeated lessons.

[RRDAP milestones](../projects/rrdap/roadmap.md) own phase state. **30 November stays a stretch for a minimal first flow**, not a reason to rush Azure. Week 6 crosses that date: a local accepted slice can demonstrate progress, with Azure integration continuing in December. January prioritizes a small correct, explainable and recoverable project. Long-term 20-million/day and 300-GB experiments stay conditional and outside required January scope.

Snowflake is secondary selective revision. Synapse and Fabric are optional; change priority only from dated target-job evidence. Kafka, advanced Kubernetes, ML engineering and unrelated technology are outside required scope. Review Hyderabad/India job descriptions weekly within interview time, recording URL/date before changing emphasis. Confirm notice period and availability before joining-date claims; January is an assessment date.

## Tutor workflow

Business problem → independent attempt → observed difficulty → targeted learning → improved implementation → testing → revision. Present purpose, input and acceptance criteria in one bounded task; wait for code/output/reasoning. Give progressive help for demonstrated gaps, then changed input or reconstruction. Avoid trivial repeated confirmation and future architecture spoilers. Implement assigned repository infrastructure directly; preserve learner ownership of active assignments.

Use the five roles, [checkpoint boundaries](../reference/checkpoints.md), [record authority/review rule](../reference/learning-coach.md) and [timer rules](../reference/study-tracking.md). Actual attempts/help save at explicit boundaries; timer timestamps remain immediate. Weekly review compares planned/confirmed hours, actual assessed dimensions, delayed review, independent builds, [interview evidence](interview-preparation.md) and the next gap. Do not add roadmap topics to retention schedules as though studied.

## Official starting references

Azure/Delta overview sources checked during the upgrade on 22 October 2026. Verify version-specific lab instructions when used.

- [ADF overview](https://learn.microsoft.com/en-us/azure/data-factory/introduction)
- [ADLS overview](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction)
- [Azure Databricks overview](https://learn.microsoft.com/en-us/azure/databricks/introduction/)
- [Delta documentation](https://docs.delta.io/)
- [PostgreSQL tutorial](https://www.postgresql.org/docs/current/tutorial.html)
- [Spark SQL guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [Airflow documentation](https://airflow.apache.org/docs/)
- [dbt documentation](https://docs.getdbt.com/docs/introduction)
- [Docker Compose](https://docs.docker.com/compose/)
