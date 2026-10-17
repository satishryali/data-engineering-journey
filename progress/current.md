# Current tutoring checkpoint - RRDAP, 17 October 2026 (IST)

## Current state

RRDAP replaces RetailFlow at explicit learner request. Active phase 1 and **RDS-001 Product Catalogue**, in progress: Faker/commerce CSV-generation practice found in projects/rrdap/Test/datafaker.ipynb. PostgreSQL loading and SQL acceptance verification remain pending; no task completion or new proficiency score claimed.

Study timer **paused at 21:27:54 IST**. **RDS-20261017T205651** closed: **20:56:51-21:27:54 = 31m03s**. Confirmed today **6h39m08s**; ten-hour target remaining **3h20m52s**. Partial week confirmed **11h09m05s / 32h baseline**. RRDAP confirmed closed time **2h44m34s**; prior RetailFlow/Python time separate. No running timer; breaks and old uncertain 15 October interval excluded. No new learner submission or assessment in this chat; exact next task unchanged. Excel refreshed for 17 October.

## Exact next task

RDS-001: Propose an approach or independently implement the 1,000-product PostgreSQL catalogue, then submit code and SQL verification against the six acceptance criteria.

Read [RDS-001](../projects/rrdap/tasks/RDS-001.md), [project checkpoint](../projects/rrdap/checkpoint.md) and [RRDAP workflow](../reference/rrdap.md). PostgreSQL is available per learner report; task connection is not yet verified. Learner generator notebook and product_data.csv now inspected: 1,000 nonempty data records plus extra blank rows. Price-method positional argument does not set a range; documented in Notes/Python/Concepts/faker.md. Learner files preserved; no PostgreSQL implementation verified.

## Teaching and evidence

One tutor coordinates the five roles. Business requirement -> independent design/implementation -> observed difficulty -> learner investigation/improvement -> help as needed -> comparison/verification -> notes/revision. Do not reveal future pain points or prescribe unnecessary tools. Teach syntax directly when asked. Verify current acceptance, separate essential fixes from optional improvements, and accept simple safe correct work. Tool changes follow measured current implementation, investigation, improvement and fair same-workload comparisons. Never invent failures or force frameworks.

Earlier guided Python evidence remains in tools/python/exercises/001-record-cleaning/attempts/012-function-and-csv-pause.ipynb and its review note: dictionary/list/conversion/error handling, copy/input preservation, clean_orders, changed/repeated/empty inputs and CSV reading. No independent delayed retention. Requested split() reference is saved; no learner split attempt assessed. Practice notebooks inspected on 17 October for the requested notes: dictionary operations, CSV reading/writing, file methods, basic objects and random. Saved outputs are evidence of practice; help and independent understanding remain unknown. The employee CSV files confirm the newline difference; product_data.csv is currently empty despite its saved write cell. No acceptance result or scored review inferred.

Notebook-based notes saved on 17 October: [Python index](../Notes/Python/Index.md) links the updated dictionary/CSV reading notes and new CSV writing, file methods, objects and random notes. Small examples executed in scratch space; recall prompts saved separately. Four new concepts mapped with adjustable initial diagnostic slots, no scored assessment or changed retention dates. Timer stays paused; RDS-001 and the deferred orders task remain pending.

## Preserved and deferred work

RetailFlow is superseded with its files, synthetic input, RF-001 requirement and setup history retained; no RF implementation was submitted or verified. Prior Python valid/rejected CSV writing/read-back and SQL-003 implementation remain unfinished. Historical attempt.py is not the current working solution.

Existing SQL-001/002/003 due dates remain 16 October; relevant Python assisted reviews due 17 October. Choose bounded retrieval from actual queue/history, not the whole backlog. No scored RRDAP review or retention due date exists. Keep existing valid intervals/stages and do not reset skills on a project change.

## Project, lab and target

[RRDAP roadmap](../projects/rrdap/roadmap.md): ten high-level phases; first working operational-to-reporting flow by **30 November 2026** is a stretch goal. Remaining effort unestimated; RetailFlow's 200-250 hours is not a validated RRDAP estimate. Future 20-million-record/day and up-to-300-GB targets depend on measurements; no large data generation or service installation occurred. Multiple independent sources must eventually describe one consistent fictional business; introduce only current necessary entities/tools.

[Reported lab](../projects/rrdap/README.md) records home Ubuntu server, WSL2 laptop, additional desktop, K3s/Spark experiments and Google storage. Hardware/free capacity, desktop RAM/availability, cluster/service state and account access are unverified. Protect data/resources/credentials; restore in isolation. Retain existing sustainable weekly budgets, one Azure concept weekly and Docker within project hours. Prior employment and reported tool familiarity are separate from DE project evidence; career outcomes not promised.

The reported SQL-versus-dbt experiment was not found in this checkout; external location/branch/commit unknown. Inspect when available and relevant, preserving work. No commit/push/publish authorised. Update this file, START-HERE.md and project checkpoint together at explicit save boundaries; no background agents/reminders.

Faker notes follow-up, 17 October: inspected projects/rrdap/Test/datafaker.ipynb and its product_data.csv, which is distinct from the empty practice/Modules/product_data.csv. Saved basic/customer/provider outputs and CSV evidence documented; small note examples executed separately. Assistance unknown. Price argument and extra newline findings documented without changing the learner code. PostgreSQL catalogue acceptance still pending; timer unchanged and paused.
