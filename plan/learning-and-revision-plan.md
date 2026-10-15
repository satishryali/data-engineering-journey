# Data engineering learning and revision plan

Prepared: 15 October 2026. Timezone: Asia/Kolkata (IST).
Baseline/startup: 15–18 October 2026. Sixteen full learning weeks: 19 October 2026–7 February 2027.
Goal: prepare to compete for suitable India data engineering roles by February 2027. A role or salary outcome is not guaranteed. Notice period is 90 days; learner is considering resignation on 30 November 2026. Resignation and last working date are not confirmed; February remains a target. Apply early enough for actual availability.

## Starting position and priorities

Five years of software experience: four in support and one in development. Reported familiarity: PL/SQL, Python, Git, Power BI, PostgreSQL and Snowflake. Practical proficiency is not assumed. The first SQL attempt showed correct join keys, use of SUM and status filtering, but gaps in unmatched-row preservation, grouping and PostgreSQL date filtering. Python, dbt and pipeline baseline work is not yet demonstrated. No project completion has been recorded.

Priorities: reliable SQL/Python implementation; dbt; Airflow; practical intermediate Docker; PySpark fundamentals; one Azure concept per week. Git, debugging, testing, documentation and communication accompany project work. Power BI remains optional presentation work. Do not add Kafka, Kubernetes, multiple cloud providers or certifications to this schedule without a specific hiring reason.

## Weekly budget: 50 study hours

The learner confirmed six hours per weekday and ten per weekend day. Breaks, meals and sleep are outside these study-hour targets. These hours are a target to evaluate against actual logs, not evidence of learning or a requirement to make up missed hours.

| Activity | Hours/week |
|---|---:|
| SQL and Python implementation | 14 |
| Current technology and project work, including guided explanations and Git | 16 |
| Spaced retrieval, corrections and reconstruction | 10 |
| Azure learning and practice | 3 |
| Independent assessments and feedback | 3 |
| Job research, interview explanations and applications | 3 |
| Weekly checkpoint and planning | 1 |
| Total | 50 |

SQL/Python split starts approximately equally and adapts to demonstrated gaps. Current-technology hours move from basic project work to dbt, Airflow and PySpark as prerequisites improve. Assessments use small unfamiliar variations, not just the same memorised examples.

## Daily routine

Each weekday: two hours SQL/Python, two hours current project/technology, one hour revision, one rotating hour below.

| Day | Rotating hour |
|---|---|
| Monday | Azure concept and a small example |
| Tuesday | Job requirements, experience stories, resume or targeted applications |
| Wednesday | Azure hands-on exercise or architecture exercise |
| Thursday | Interview practice or targeted applications |
| Friday | Independent mixed assessment and feedback |

Saturday (10 hours): two hours SQL/Python; three hours project; two hours revision; one hour Azure recall/application; one hour assessment; one hour job preparation.

Sunday (10 hours): two hours SQL/Python; three hours project; three hours cumulative revision/reconstruction; one hour independent assessment; one hour planning.

The known reminder anchors remain 7 a.m., 1 p.m., 8:30 p.m. IST. The original six-hour daily windows do not themselves fit six study hours plus breaks. Exact additional clock slots have not been supplied: use these duration blocks and move or extend blocks around actual availability. Do not invent extra reminders or assume work attendance. A practical starting pattern is 45–50 minutes work followed by 10–15 minutes away, with longer breaks between major blocks; this is an adjustable convenience, not a scientifically optimal timer.

Keep revision early enough that it is not routinely dropped. On long weekend days, distribute sessions across the day. If concentration or completion declines, reduce new material and use a smaller sustainable plan; never sacrifice sleep or accumulate catch-up debt to protect the hour target.

## Evidence-informed learning cycle

1. Retrieve before reading: attempt a question, prediction, query or explanation without the prior solution.
2. Learn one small missing idea. Use a worked example when stuck, then hide it and reconstruct the step.
3. Implement and run the code. Check output against a hand-calculated small dataset.
4. Explain why it works and what can fail. Syntax documentation is allowed in realistic coding practice; record whether the solution itself was consulted.
5. Solve a changed version. Mix related skills after initial practice; do not overwhelm the first introduction with many topics.
6. Record evidence and schedule a later retrieval attempt.

Retrieval and spacing are supported by learning research. These studies do not validate this exact 50-hour timetable, this particular technology order or a guaranteed career result. Exact revision dates, block lengths and readiness thresholds below are practical rules that will be adapted.

## Revision scheduling

Use [the shared five-role review rule](../reference/learning-coach.md): stages 0–4 are 1, 3, 7, 14 and 30 days from the actual latest scored assessment date in IST. Initial assessment on 19 October gives 20 October; independent score-3 delayed retrieval on 20 October advances to a three-day interval, due 23 October. Immediate correction does not move a delayed date; unknown assistance cannot advance independence. Existing valid historical due dates remain unchanged. These are adjustable heuristics; the table describes interval-stage task variations, not fixed offsets from the original learning date.

| Review | Exercise |
|---|---|
| Next day | Rebuild the small solution without looking at it; explain the key choice |
| Around day 3 | Change the inputs or add one edge case |
| Around day 7 | Combine it with a related skill and debug an error |
| Around day 14 | Use it in the project or compare two possible approaches |
| Around day 30 | Solve an unfamiliar version and explain the tradeoff |

At the next checkpoint boundary, log actual attempts, dates, variation, correctness, help used and evidence in revision-history.csv, and update revision-queue.csv using the shared rule. Timer events remain immediate. Only schedule assessed work; do not mark all planned topics as learned.

- Independent and correct: progress to a more demanding variation or later review. Keep occasional mixed review after the 30-day checkpoint.
- Correct after a hint or solution: record assisted, teach the gap and review the next day. Do not record independent mastery.
- Incorrect or unable to start: record needs_guidance, use a smaller example, then try a reconstruction. Schedule another attempt the next day.
- Ambiguous question or faulty answer key: repair the assessment before judging the learner.
- Late or missed review: use the actual attempt date, prioritise a few important weak items, and reschedule the rest. Do not force a large review backlog or restart the course.
- A repeated independent success on different days plus a new variation is a useful readiness signal, not a scientifically validated pass mark.

When reviews exceed the revision budget, pause additions and combine related items into one meaningful task. Keep individual retrieval tasks small: one skill, one question or one short pipeline behaviour, not 'revise Python'.

## Sixteen-week curriculum

Dates are targets; actual demonstrated skill determines advancement. If foundations take longer, reduce later Spark depth or optional deployment scope rather than compressing every topic. Keep Azure practical work within the three-hour weekly allocation. If cloud access or budget is unavailable, use a local equivalent plus a clearly labelled architecture exercise; do not claim a deployment occurred.

| Week | Main focus | One Azure concept | Evidence to demonstrate |
|---|---|---|---|
| 1: 19 Oct–25 Oct | SQL joins, grouping, NULLs; Python loops, dictionaries, functions; Git | Regions, subscriptions and resource groups | Keep unmatched customers; calculate revenue correctly; clean five Python records; save work in Git |
| 2: 26 Oct–01 Nov | SQL dates, CTEs and introductory windows; Python files, exceptions and tests | Identity and least-privilege access | Write a dated report and a CSV validator; explain expected outputs and errors |
| 3: 02 Nov–08 Nov | Table grain, keys, facts/dimensions; Python-to-PostgreSQL loading; first dbt model | Blob storage and Data Lake Storage concepts | Load a small dataset and build a reporting model with a stated row grain |
| 4: 09 Nov–15 Nov | dbt sources, ref, staging, tests and documentation | Storage permissions and identity-based access | Build documented model dependencies; demonstrate a failing data-quality test |
| 5: 16 Nov–22 Nov | Deduplication, changed records, incremental dbt and repeatable runs | Compute choices for Python jobs | Rerun and update a load without duplicate orders; explain handling of corrections |
| 6: 23 Nov–29 Nov | SQL query plans and dbt materializations; selected Snowflake implementation; Docker images and Dockerfile | Secrets and configuration | Explain one query plan and view/table choice; build and run a Python image with explicit dependencies and .dockerignore |
| 7: 30 Nov–06 Dec | Python API ingestion, modules, logging; shell; Docker Compose, networks and volumes | Networking basics and connectivity | Handle a paginated sample/API response; connect Python and PostgreSQL services by name and preserve data across container recreation |
| 8: 07 Dec–13 Dec | Airflow tasks, dependencies, schedules and data intervals; Docker health checks and logs | Connecting storage, compute and warehouse | Orchestrate the existing pipeline; distinguish startup order from readiness and diagnose a deliberately unhealthy service |
| 9: 14 Dec–20 Dec | Airflow retries, backfills and safe recovery; Docker reproducibility and troubleshooting | CSV, JSON and Parquet choices | Recover and backfill without double counting; recreate the local environment from the repository and debug a connection or configuration fault |
| 10: 21 Dec–27 Dec | Integrate Azure storage with existing project; deploy one small job if access permits | Data lake paths, layers and partitioning | Read/write a small cloud dataset or demonstrate the equivalent locally and document access needs |
| 11: 28 Dec–03 Jan | PySpark DataFrames, schemas, casting and NULL handling | Scheduling and event triggers | Transform the orders dataset and write Parquet; compare output to SQL |
| 12: 04 Jan–10 Jan | PySpark joins, aggregation and window functions | Logs, metrics and alerts | Deduplicate changed records deterministically; diagnose a deliberately failed job |
| 13: 11 Jan–17 Jan | Spark lazy execution, partitions, shuffles and basic plan reading | Reruns, recovery and retained input data | Explain a shuffle and a partition decision; validate pipeline totals across implementations |
| 14: 18 Jan–24 Jan | Integration, schema changes and an unfamiliar second dataset | Cost estimation, budgets and resource cleanup | Handle a schema-change scenario and produce a runbook with cost assumptions |
| 15: 25 Jan–31 Jan | Independent rebuild, SQL/Python interviews and project explanations | Reproducible deployment and configuration | Rebuild a pipeline slice from a brief; complete a mock interview and improve the resume |
| 16: 01 Feb–07 Feb | Readiness assessment, targeted gap repair and ongoing applications | Architecture review and troubleshooting | Demonstrate, explain and repair the pipeline without step-by-step guidance; record remaining gaps |

## Practical intermediate Docker

Requested addition: 15 October 2026. Allocate an initial three hours per week in weeks 6–9 (12 hours total) inside the existing 16 project/technology hours, not in addition to the 50-hour budget. Reuse Docker in later project work and use the normal revision queue after actual attempts. This is an initial teaching allocation, not a promise of mastery in 12 hours. If it takes longer, simplify optional project scope instead of adding more technologies or cutting essential revision.

| Week | Docker focus | Demonstration |
|---|---|---|
| 6 | Images versus containers; Dockerfile; build/run/tag; dependencies; .dockerignore; build cache; runtime configuration | Package the Python loader and explain which changes rebuild which layers; keep credentials out of the image |
| 7 | Compose services; service-name networking; published ports; bind mounts versus named volumes | Connect Python and PostgreSQL; demonstrate what happens to data when a container is recreated and a named volume is retained |
| 8 | Health checks and readiness; logs; exec/inspect; lifecycle; basic resource inspection | Explain that starting a container does not mean its application is ready; diagnose a failing local dependency |
| 9 | Reproducible startup, image versions and configuration; safe cleanup; debugging | Rebuild from the repository, restart services and repair a connection/configuration fault without unintentionally deleting persisted data |

Intermediate readiness means writing and explaining the Dockerfile and Compose configuration, choosing appropriate persistence, diagnosing common faults and reproducing the environment with documentation. Docker is a project skill, not a standalone certification track. Kubernetes, orchestration-cluster administration and advanced image optimisation are outside this deadline. No Docker software or containers are installed or started by adding this plan.

## Project and job-search strategy

Build one growing orders/customer pipeline: Python ingestion into PostgreSQL; validated SQL and dbt models; selected models in Snowflake if access exists; Airflow orchestration; Azure storage/compute integration; a PySpark processing component when introduced. Every component needs a reason, not just a place in the diagram. Use small, inspectable data before larger files. An optional second unfamiliar dataset checks transfer without starting another large project.

Introduce realistic problems progressively: NULLs and malformed amounts; duplicate IDs; customer rows without orders; changed orders; retries; partial failures; historical reloads; schema changes; permissions and cost. Preserve a small expected-output example and a runbook. Local educational demos must not be described as production experience.

Begin resume and experience-story work in week 1. Review target job descriptions weekly. Start targeted applications when the existing background and demonstrated work fit a role; aim to begin during November rather than waiting for every technology. Account for the confirmed 90-day notice period and tentative 30 November resignation; verify actual availability when known. A 15 LPA offer is a goal, not an assessment promise.

## Week 1 daily tasks

| Day | Core work and project application |
|---|---|
| Monday | LEFT JOIN and unmatched rows; Python loop over dictionaries; reproduce the sample data and make a Git checkpoint |
| Tuesday | GROUP BY at customer grain, SUM and COALESCE; functions and return values; build a revenue report |
| Wednesday | Date ranges and ON-versus-WHERE behaviour; integer conversion and exceptions; reject malformed records |
| Thursday | Valid-record deduplication; functions, sets and dictionaries; reconcile counts with a hand calculation |
| Friday | Independent SQL and Python baseline variants; fix the two largest gaps; practise explaining a troubleshooting example |
| Saturday | Combine validation with file handling or database loading if ready; reconstruct this week's work; Azure example and assessment |
| Sunday | Mixed recall, unfamiliar edge cases, project explanation, checkpoint and next-week adjustment |

All daily tasks are conditional on the previous step being understood. In the startup days 15–18 October, begin the current LEFT JOIN correction and Python baseline; do not wait until Monday. If completed early, week 1 becomes harder variations rather than repeating identical questions. No completed sessions or successes are assumed.

## Today's starting point

Read progress/current.md and START-HERE.md for the latest learner-selected task. The old initial LEFT JOIN prompt is historical and must not restart assessment. At this setup the pending task remains PY-002's dictionary read/update/print attempt; SQL totals and the full cleaner remain deferred. Selecting a task does not start a timer.

## How the assistant maintains this plan

From the repository root, read plan/learning-and-revision-plan.md, plan/weekly-learning-plan.csv, tracking/revision-queue.csv, tracking/revision-history.csv, tracking/study-log.csv and progress/current.md when available. Use the plan as a curriculum, never as proof of completion. Select the actual next task from learner evidence and queued review dates. Update revision records after actual attempts. Do not invent reminders, results, attended sessions or job outcomes.

Use reference/study-tracking.md for time accounting. Start/stop messages record reported study intervals; silence is not proof of concentration. Daily summaries show confirmed time separately from active or uncertain intervals. A weekly summary reports hours, independent versus assisted results, remaining weaknesses, project evidence and next actions. When asked in a different chat without file access, request the latest checkpoint rather than pretending to have these records.

## Research and official references

- Karpicke and Blunt (2011), retrieval practice and meaningful learning: https://pubmed.ncbi.nlm.nih.gov/21252317/
- Karpicke and Bauernschmidt (2011), spaced retrieval and relative schedules: https://pubmed.ncbi.nlm.nih.gov/21574747/
- Karpicke and Roediger (2010), feedback and expanding versus equal intervals: https://pubmed.ncbi.nlm.nih.gov/19966244/
- PostgreSQL tutorial: https://www.postgresql.org/docs/current/tutorial.html
- dbt quickstarts: https://docs.getdbt.com/docs/get-started-dbt
- Airflow concepts: https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/
- Azure core data concepts: https://learn.microsoft.com/en-us/training/paths/azure-data-fundamentals-explore-core-data-concepts/
- Docker Compose quickstart: https://docs.docker.com/compose/gettingstarted/
- Docker build practices: https://docs.docker.com/build/building/best-practices/
- Compose readiness and startup: https://docs.docker.com/compose/how-tos/startup-order/
