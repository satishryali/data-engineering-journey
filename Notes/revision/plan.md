# Revision plan (generated)

As of 2026-10-28 IST. Refresh at revision planning or checkpoint boundaries.
Source: topic-map + revision queue/history + mistakes. This plan does not record an attempt.

## Coverage

| Count | Meaning |
| ---: | --- |
| 162 | learning sections mapped |
| 9 | sections excluded |
| 40 | topics total |
| 3 | topics assessed |
| 0 | topics practised on delayed review |
| 3 | topics needing help |

Assessed = a scored, non-immediate concept assessment. Delayed practice = an actual answered delayed event;
it can be incorrect or assisted. Neither count means permanent retention. Broad exercise results stay separate.

## Due today

- None.

## Overdue

- **SQL-001**: LEFT JOIN and unmatched rows; due 2026-10-16; last result independent.
- **SQL-002**: Counting orders after LEFT JOIN; due 2026-10-16; last result assisted.
- **SQL-003**: Customer order totals; due 2026-10-16; last result assisted.
- **PY-001**: Python record cleaning; due 2026-10-17; last result assisted.
- **py.records.cleaning**: Record access, accumulation and conversion; due 2026-10-17; last result assisted.
- **py.functions.basics**: Function inputs, local result lists and return; due 2026-10-17; last result assisted.
- **py.csv.read**: Read CSV rows as dictionaries; due 2026-10-17; last result assisted.

## Upcoming reviews

- None.

## Awaiting initial assessment

Dates below are adjustable planning slots, not completed reviews or overdue retention.

| Topic | Initial slot | Prerequisites |
| --- | --- | --- |
| py.dict.access: Dictionary lookup and missing keys | 2026-10-16 | None |
| py.dict.mutate: Updating and iterating dictionaries | 2026-10-17 | py.dict.access |
| py.list.basics: Lists, positions, length and repeated values | 2026-10-18 | None |
| py.list.mutate: Replacing list items and appending | 2026-10-19 | py.list.basics |
| py.list.records: Collecting dictionary records in lists | 2026-10-20 | py.dict.access, py.list.mutate |
| sql.join.preservation: LEFT JOIN preservation | 2026-10-21 | None |
| sql.join.keys: Joining related identifiers | 2026-10-22 | sql.join.preservation |
| sql.count.nulls: COUNT and NULLs | 2026-10-23 | sql.join.preservation |
| sql.group.grain: Customer identity and grouping grain | 2026-10-24 | sql.join.keys |
| sql.sum.nulls: SUM without non-NULL input | 2026-10-25 | sql.count.nulls |
| py.dict.remove: Removing dictionary items | 2026-10-27 | py.dict.access, py.dict.mutate |
| py.modules.main: Imports and the main guard | 2026-10-28 | None |
| py.paths.imports: File paths and module lookup | 2026-10-29 | None |
| py.logging.basics: Logging configuration and named loggers | 2026-10-30 | None |
| py.context.resources: Context managers and resource lifecycle | 2026-10-31 | None |
| pg.cursor.results: Connections, cursors, execute and fetch | 2026-11-01 | None |
| py.logging.shared: Shared logging configuration | 2026-11-02 | py.logging.basics, py.paths.imports |
| de.ingest.seeds: Raw ingestion types and dbt seeds | 2026-11-03 | None |
| vault.kv.read: Vault client and nested KV response | 2026-11-04 | py.dict.access |
| py.str.split: Split strings into pieces | 2026-11-05 | py.list.basics |
| py.csv.write: Write CSV lists and dictionaries | 2026-11-06 | py.csv.read |
| py.files.methods: File reading methods and position | 2026-11-07 | None |
| py.objects.basics: Objects methods and printed representation | 2026-11-08 | None |
| py.random.basics: Random numbers selections and repeatable sequences | 2026-11-09 | py.list.basics |
| py.faker.basics: Faker generators locales and commerce providers | 2026-11-10 | py.dict.access, py.csv.write |
| py.records.summary: Count and total orders by status after a loop | 2026-11-11 | py.list.records, py.csv.read |
| py.decimal.money: Decimal prices and explicit money rounding | 2026-11-12 | py.csv.read |
| py.dataclasses.basics: Dataclass records and generated methods | 2026-11-13 | py.objects.basics |
| py.concurrency.threading: Python multithreading: Thread, start, join and ThreadPoolExecutor | 2026-11-14 | py.functions.basics |
| py.objects.protocols: Object comparison and collection special methods | 2026-11-14 | py.objects.basics |
| ai.model.adaptation: Inference prompting and fine-tuning for a reminder model | 2026-11-15 | None |
| ai.reminders.evaluation: Evaluate reminder fields against a baseline | 2026-11-16 | ai.model.adaptation |
| ai.reminders.dataset: Input target pairs and template data for reminders | 2026-11-17 | ai.reminders.evaluation |
| ai.reminder.model: Reminder models: inference prompting and fine-tuning | 2026-11-18 | None |
| ai.reminder.evaluation: Checking reminder model fields against a baseline | 2026-11-19 | ai.reminder.model |
| ai.reminder.examples: Reminder input and target example pairs | 2026-11-20 | ai.reminder.evaluation |
| py.strings.returned-text: String cleanup and returned case conversions | 2026-11-21 | None |

## Important weak topics

- Exercise SQL-002: assisted. Historical exercise evidence is separate from concept assessment counts.
- Exercise SQL-003: assisted. Historical exercise evidence is separate from concept assessment counts.
- Exercise PY-001: assisted. Historical exercise evidence is separate from concept assessment counts.
- py.dict.access: Unassessed; linked mistakes M-PY-001.
- py.dict.mutate: Unassessed; linked mistakes M-PY-001.
- sql.count.nulls: Unassessed; linked mistakes M-SQL-001.
- sql.join.keys: Unassessed; linked mistakes M-SQL-002.
- sql.group.grain: Unassessed; linked mistakes M-SQL-003.
- sql.sum.nulls: Unassessed; linked mistakes M-SQL-004, M-SQL-005.
- py.records.cleaning: Learning with help; linked mistakes M-PY-002, M-PY-003, M-PY-004, M-PY-005, M-PY-006, M-PY-007, M-PY-008, M-PY-009, M-PY-010.
- py.functions.basics: Learning with help; linked mistakes M-PY-011, M-PY-REM-001.
- py.csv.read: Learning with help; linked mistakes M-PY-012.

## Coverage gaps

- Removed section: Notes/Python/Concepts/special-methods.md / Special methods / __getitem__ - support square brackets / What makes `__getitem__` special
- Neglected topics: py.dict.access, py.dict.mutate, sql.join.preservation, sql.count.nulls, sql.join.keys, sql.group.grain, sql.sum.nulls, py.dict.remove, py.list.basics, py.list.mutate, py.list.records
- Reassessment flags: py.objects.protocols

## Manageable session

Default: 15–20 minutes; one meaningful task at a time, at most one new diagnostic concept.
Check prerequisites first. Teach missing understanding before retention practice. No timer starts from planning.
- sql.join.preservation: prerequisite check; teach if needed, about 10 minutes.
- 37 topics await assessment. One diagnostic per suitable session needs at least 37 sessions; new notes can extend this. Replan missed slots without restarting.

## Topic evidence

| Topic | State | Last actual review | Next review | Evidence / help |
| --- | --- | --- | --- | --- |
| py.dict.access | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| py.dict.mutate | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| py.context.resources | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| pg.cursor.results | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| py.logging.basics | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| py.paths.imports | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| py.modules.main | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| vault.kv.read | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| py.logging.shared | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| de.ingest.seeds | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| sql.join.preservation | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| sql.count.nulls | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| sql.join.keys | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| sql.group.grain | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| sql.sum.nulls | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| py.records.cleaning | Learning with help | 2026-10-16 | 2026-10-17 | tools/python/exercises/001-record-cleaning/attempts/011-copy-cleaner-fresh-input.ipynb; help=True, notes=None, hints=None |
| py.dict.remove | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| py.list.basics | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| py.list.mutate | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| py.list.records | Unassessed | 2026-10-16 | None | tools/python/exercises/001-record-cleaning/attempts/005-payment-list-loop.ipynb; help=None, notes=None, hints=None |
| py.functions.basics | Learning with help | 2026-10-16 | 2026-10-17 | tools/python/exercises/001-record-cleaning/attempts/012-function-and-csv-pause.ipynb; help=True, notes=None, hints=None |
| py.csv.read | Learning with help | 2026-10-16 | 2026-10-17 | tools/python/exercises/001-record-cleaning/attempts/012-function-and-csv-pause.ipynb; help=True, notes=None, hints=None |
| py.str.split | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| py.csv.write | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| py.files.methods | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| py.objects.basics | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| py.random.basics | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| py.faker.basics | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| py.records.summary | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| py.decimal.money | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| py.dataclasses.basics | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| py.objects.protocols | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| py.concurrency.threading | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| ai.model.adaptation | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| ai.reminders.evaluation | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| ai.reminders.dataset | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| ai.reminder.model | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| ai.reminder.evaluation | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| ai.reminder.examples | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |
| py.strings.returned-text | Unassessed | None | None | No concept assessment; help=None, notes=None, hints=None |

## Source sections and exclusions

A section is direct content under a Markdown heading (or a preamble); code-fence headings are ignored.
Related sections share topic IDs. Empty container headings are not counted.

- [Notes/.gitignore](../../Notes/.gitignore): Image, asset or machine-readable view; learning is mapped from its explanation note.
- [Notes/.obsidian/app.json](../../Notes/.obsidian/app.json): App configuration; no learning coverage.
- [Notes/.obsidian/appearance.json](../../Notes/.obsidian/appearance.json): App configuration; no learning coverage.
- [Notes/.obsidian/core-plugins.json](../../Notes/.obsidian/core-plugins.json): App configuration; no learning coverage.
- [Notes/.obsidian/graph.json](../../Notes/.obsidian/graph.json): App configuration; no learning coverage.
- [Notes/.obsidian/workspace.json](../../Notes/.obsidian/workspace.json): App configuration; no learning coverage.
- [Notes/AI/Index.md](../../Notes/AI/Index.md): Index, vault setup or curriculum administration; no assessed lesson content.
- [Notes/AI/recall-questions.md](../../Notes/AI/recall-questions.md): Answer-free retrieval prompts; explanations mapped from AI notes.
- [Notes/AI/reminder-input-practice.md](../../Notes/AI/reminder-input-practice.md)
  - Collecting reminder inputs: py.strings.returned-text
  - Collecting reminder inputs / Read and clean text: py.strings.returned-text
  - Collecting reminder inputs / A string method returns new text: py.strings.returned-text
  - Collecting reminder inputs / Sources and next step: Sources, provenance and pending task links; no extra concept.
- [Notes/AI/reminder-model-basics.md](../../Notes/AI/reminder-model-basics.md)
  - A small model for reminders: ai.reminder.model
  - A small model for reminders / Running and fine-tuning: ai.reminder.model
  - A small model for reminders / Check the answer before training: ai.reminder.evaluation
  - A small model for reminders / Create input and answer pairs: ai.reminder.examples
  - A small model for reminders / Sources and session evidence: Sources, provenance and pending task links; no extra concept.
- [Notes/New Syntax/README.md](../../Notes/New%20Syntax/README.md): Index, vault setup or curriculum administration; no assessed lesson content.
- [Notes/New Syntax/dictionary-copy.md](../../Notes/New%20Syntax/dictionary-copy.md)
  - Copy a dictionary before changing it: py.dict.mutate, py.records.cleaning
- [Notes/New Syntax/list-plus.md](../../Notes/New%20Syntax/list-plus.md)
  - Join lists using +: py.list.basics
  - Join lists using + / A small example: py.list.basics, py.list.records
  - Join lists using + / Why the square brackets matter: py.list.basics
- [Notes/New Syntax/string-split.md](../../Notes/New%20Syntax/string-split.md)
  - Split text using split(): py.str.split
  - Split text using split() / Split at a chosen separator: py.str.split
  - Split text using split() / Split on spaces: py.str.split
  - Split text using split() / Limit the splits: py.str.split
  - Split text using split() / CSV files: py.csv.read
- [Notes/Python/Concepts/Hashicorp_vault.md](../../Notes/Python/Concepts/Hashicorp_vault.md)
  - Step 1 : importing hvac: vault.kv.read
  - Step 2 : creating your logger object: py.logging.basics
  - Step 3 : Define where the vault lives and your secret token: vault.kv.read
  - Initialize the Vault Client: vault.kv.read
  - Check if the connection is acutally working or not: vault.kv.read
  - Step 6 : Know your secrets path & Mount Point: vault.kv.read
  - Step 7 : Connect to the vault and fetch the secrets: vault.kv.read
- [Notes/Python/Concepts/Logging.md](../../Notes/Python/Concepts/Logging.md)
  - Notes / Logging Module: py.logging.basics, py.paths.imports
  - When you are not sure about the error using logging.exception in the except section.: py.logging.basics
- [Notes/Python/Concepts/csv-reading.md](../../Notes/Python/Concepts/csv-reading.md)
  - Read a CSV file: py.csv.read
  - Read a CSV file / Read rows with DictReader: py.csv.read
  - Read a CSV file / Keep all CSV rows: py.csv.read, py.list.records, py.list.mutate
  - Read a CSV file / Import names must match: py.csv.read
  - Read a CSV file / Pass records to the cleaner: py.csv.read
  - Read a CSV file / A comma inside a value: py.csv.read
  - Read a CSV file / Reader versus DictReader: py.csv.read
- [Notes/Python/Concepts/csv-writing.md](../../Notes/Python/Concepts/csv-writing.md)
  - Write CSV files: py.csv.write
  - Write CSV files / Write lists as rows: py.csv.write
  - Write CSV files / Write dictionaries as rows: py.csv.write
  - Write CSV files / Open two files in one with statement: py.context.resources, py.csv.read, py.csv.write
  - Write CSV files / Why newline matters: py.csv.write
  - Write CSV files / Notebook evidence: py.csv.write
- [Notes/Python/Concepts/dataclasses.md](../../Notes/Python/Concepts/dataclasses.md)
  - Dataclasses: py.dataclasses.basics
  - Dataclasses / Create an order: py.dataclasses.basics
  - Dataclasses / Why use it when dictionaries exist: py.dataclasses.basics
  - Dataclasses / Type hints do not convert values: py.dataclasses.basics
  - Dataclasses / The same display with a regular class: py.dataclasses.basics
  - Dataclasses / Sources and learning status: Source provenance and assessment status; no additional concept.
- [Notes/Python/Concepts/decimal-money.md](../../Notes/Python/Concepts/decimal-money.md)
  - Decimal for prices and totals: py.decimal.money
  - Decimal for prices and totals / Import and create a Decimal: py.decimal.money
  - Decimal for prices and totals / Convert the CSV price directly: py.decimal.money
  - Decimal for prices and totals / Round to two decimal places: py.decimal.money
  - Decimal for prices and totals / Learning evidence: Source-code observations, links and pending assessment; no additional concept coverage.
- [Notes/Python/Concepts/dictionaries.md](../../Notes/Python/Concepts/dictionaries.md)
  - Dictionaries: py.dict.access
  - Dictionaries / Accessing items: py.dict.access
  - Dictionaries / Changing the elements / Method 1 : Direct Key assignment: py.dict.mutate
  - Dictionaries / Changing the elements / Method 2 : .update() Method: py.dict.mutate
  - Dictionaries / Changing the elements / Same key replaces its value: py.dict.mutate, py.list.records
  - Dictionaries / Changing the elements / Method 3 : Dictionary comprehension: py.dict.mutate
  - Dictionaries / Changing the elements / Method 4 : Merging  |=: py.dict.mutate
  - Dictionaries / Remove Items : / Method 1 : using pop: py.dict.remove
  - Dictionaries / Remove Items : / Method 2 : Removing Last inserted item: py.dict.remove
  - Dictionaries / Remove Items : / Method 3 : deleting the dict & deleting the item using del: py.dict.remove
  - Dictionaries / Remove Items : / Method 4 : clear the data in dictionary: py.dict.remove
  - Dictionaries / Looping through Dictionaries: py.dict.mutate
  - Dictionaries / Notebook examples with output: py.dict.mutate
  - Dictionaries / Notebook examples with output / Duplicate keys and live views: py.dict.access
  - Dictionaries / Notebook examples with output / Change a value or build a new dictionary: py.dict.mutate
  - Dictionaries / Notebook examples with output / Remove a key, clear contents, or delete a name: py.dict.remove
- [Notes/Python/Concepts/faker.md](../../Notes/Python/Concepts/faker.md)
  - Generate practice data with Faker: py.faker.basics
  - Generate practice data with Faker / Create a generator: py.faker.basics
  - Generate practice data with Faker / Build customer dictionaries: py.faker.basics
  - Generate practice data with Faker / Add the commerce provider: py.faker.basics
  - Generate practice data with Faker / Check a method argument before using it: py.faker.basics
  - Generate practice data with Faker / What the product loop has done: py.faker.basics
  - Generate practice data with Faker / Sources: py.faker.basics
- [Notes/Python/Concepts/file-methods.md](../../Notes/Python/Concepts/file-methods.md)
  - Work with an open file: py.files.methods
  - Work with an open file / Read and return to the start: py.files.methods
  - Work with an open file / A method versus a method call: py.files.methods
  - Work with an open file / Look up available methods: py.files.methods
  - Work with an open file / Read bytes and control printed newlines: py.files.methods
- [Notes/Python/Concepts/functions.md](../../Notes/Python/Concepts/functions.md)
  - Functions: py.functions.basics
  - Functions / Input and return: py.functions.basics
  - Functions / Fresh lists for each call: py.functions.basics
- [Notes/Python/Concepts/lists.md](../../Notes/Python/Concepts/lists.md)
  - Lists: py.list.basics
  - Lists / Why we use lists: py.list.basics
  - Lists / Accessing items: py.list.basics
  - Lists / Changing an item: py.list.mutate
  - Lists / Adding an item using append: py.list.mutate
  - Lists / Adding an item using append / Starting with an empty list: py.list.mutate
  - Lists / Finding how many items we have: py.list.basics
  - Lists / Repeated values are allowed: py.list.basics
  - Lists / Keeping dictionaries inside a list: py.list.records
  - Lists / Common mistake with append: py.list.mutate
  - Lists / Common mistake with append / Wrong way: py.list.mutate
  - Lists / Common mistake with append / Correct way: py.list.mutate
  - Lists / Things to remember: py.list.basics, py.list.mutate
  - Lists / Questions for later: Recall navigation or source/administrative metadata; examples above are mapped.
  - Lists / Reference: Recall navigation or source/administrative metadata; examples above are mapped.
- [Notes/Python/Concepts/multithreading.md](../../Notes/Python/Concepts/multithreading.md)
  - Multithreading: py.concurrency.threading
  - Multithreading / Why we need multithreading: py.concurrency.threading
  - Multithreading / Running a background task with `threading.Thread`: py.concurrency.threading
  - Multithreading / Running a background task with `threading.Thread` / Output verified by running in notebook: py.concurrency.threading
  - Multithreading / Running a background task with `threading.Thread` / How the important lines work:: py.concurrency.threading
  - Multithreading / Why `target=slow_task` has no parentheses `()`: py.concurrency.threading
  - Multithreading / Waiting for results with `t.join()`: py.concurrency.threading
  - Multithreading / Waiting for results with `t.join()` / Real data pipeline example: CSV copy and read-back: py.concurrency.threading
  - Multithreading / Waiting for results with `t.join()` / Why `t.join()` matters here:: py.concurrency.threading
  - Multithreading / Managing multiple workers with `ThreadPoolExecutor`: py.concurrency.threading
  - Multithreading / Managing multiple workers with `ThreadPoolExecutor` / Expected output:: py.concurrency.threading
  - Multithreading / Python's Global Interpreter Lock (GIL): py.concurrency.threading
- [Notes/Python/Concepts/objects-and-printing.md](../../Notes/Python/Concepts/objects-and-printing.md)
  - Objects and printing: py.objects.basics
  - Objects and printing / Create an employee: py.objects.basics
  - Objects and printing / Choose what print displays: py.objects.basics
  - Objects and printing / The difference between `__str__` and `__repr__`: py.objects.basics
  - Objects and printing / The difference between `__str__` and `__repr__` / Where Python automatically uses `__repr__`: py.objects.basics
  - Objects and printing / The difference between `__str__` and `__repr__` / How `print()` chooses between them: py.objects.basics
  - Objects and printing / The difference between `__str__` and `__repr__` / Choose a useful representation: py.objects.basics
  - Objects and printing / Measure length with `__len__`: py.objects.basics
  - Objects and printing / Indexing, looping and searching with `__getitem__`: py.objects.basics
  - Objects and printing / Indexing, looping and searching with `__getitem__` / Three superpowers unlocked by `__getitem__`: py.objects.basics
  - Objects and printing / Separate practice examples: py.objects.basics
- [Notes/Python/Concepts/random.md](../../Notes/Python/Concepts/random.md)
  - Use the random module: py.random.basics
  - Use the random module / Generate numbers: py.random.basics
  - Use the random module / Choose from a list: py.random.basics
  - Use the random module / Repeat a sequence with seed: py.random.basics
  - Use the random module / Shuffle a list: py.random.basics
- [Notes/Python/Concepts/special-methods.md](../../Notes/Python/Concepts/special-methods.md)
  - Special methods: py.objects.protocols
  - Special methods / __init__ - store starting values: py.objects.basics
  - Special methods / __repr__ - describe an object: py.objects.basics
  - Special methods / __str__ - display readable text: py.objects.basics
  - Special methods / __eq__ - compare with ==: py.objects.protocols
  - Special methods / __lt__ - compare with <: py.objects.protocols
  - Special methods / __gt__ - compare with >: py.objects.protocols
  - Special methods / __len__ - support len: py.objects.protocols
  - Special methods / __getitem__ - support square brackets: py.objects.protocols
  - Special methods / __iter__ - support a for loop: py.objects.protocols
  - Special methods / __enter__ - enter a with block: py.context.resources
  - Special methods / __exit__ - leave a with block: py.context.resources
  - Special methods / Sources and learning status: Source provenance and assessment status; no additional concept.
- [Notes/Python/Concepts/with(Context_Manager).md](../../Notes/Python/Concepts/with%28Context_Manager%29.md)
  - using with (Automatic Cleanup): py.context.resources
- [Notes/Python/Database Connections/Exeucting Commands.md](../../Notes/Python/Database%20Connections/Exeucting%20Commands.md)
  - Execution of Commands in Postgres: pg.cursor.results
- [Notes/Python/Database Connections/postgres_connection.md](../../Notes/Python/Database%20Connections/postgres_connection.md)
  - Postgres Connection / Install the PostgreSQL Driver: pg.cursor.results
  - Postgres Connection / Import psycopg2: pg.cursor.results
  - Postgres Connection / Define Connection Parameters: pg.cursor.results
  - Postgres Connection / Open the connection: pg.cursor.results
  - Postgres Connection / Create a cursor: pg.cursor.results
  - Postgres Connection / Execute a Query and Fetch Results: pg.cursor.results
  - Postgres Connection / Close the connection: pg.cursor.results
  - Postgres Connection / Best Practice: pg.cursor.results, py.context.resources
- [Notes/Python/Index.md](../../Notes/Python/Index.md): Index, vault setup or curriculum administration; no assessed lesson content.
- [Notes/Python/Lessons/Doubts/Connection.md](../../Notes/Python/Lessons/Doubts/Connection.md)
  - If you wanted to check whether the connection is closed or not using a simple statement you can use this: pg.cursor.results
- [Notes/Python/Lessons/Errors & Resolutions/index.md](../../Notes/Python/Lessons/Errors%20%26%20Resolutions/index.md): Index, vault setup or curriculum administration; no assessed lesson content.
- [Notes/Python/Lessons/Errors & Resolutions/path.md](../../Notes/Python/Lessons/Errors%20%26%20Resolutions/path.md)
  - PATH ERROR: py.paths.imports
- [Notes/Python/Lessons/Images/image-1.png](../../Notes/Python/Lessons/Images/image-1.png): Image, asset or machine-readable view; learning is mapped from its explanation note.
- [Notes/Python/Lessons/Pending Tasks/Pending.md](../../Notes/Python/Lessons/Pending%20Tasks/Pending.md)
  - Pending Tasks: py.logging.shared
- [Notes/Python/Lessons/Understandings.md](../../Notes/Python/Lessons/Understandings.md)
  - Key Findings: py.modules.main
- [Notes/Python/Lessons/tips.md](../../Notes/Python/Lessons/tips.md)
  - Tips to follow when creating dbt models,transformations or anything: de.ingest.seeds
  - Interesting Topics: py.modules.main, py.context.resources, py.logging.basics, vault.kv.read
  - Path :: py.paths.imports
- [Notes/Python/Logic/collect-function-results-write-once.md](../../Notes/Python/Logic/collect-function-results-write-once.md)
  - Collect function results and write once: py.functions.basics, py.list.records
  - Collect function results and write once / Why only the last result remained: py.functions.basics, py.list.records, py.csv.write
  - Collect function results and write once / Keep one dictionary per input file: py.functions.basics, py.list.records, py.dict.mutate
  - Collect function results and write once / Return one result and collect it outside: py.functions.basics, py.list.records, py.csv.write
  - Collect function results and write once / All writing can be inside a function: py.functions.basics, py.list.records, py.csv.write
  - Collect function results and write once / Append versus a fresh report: py.csv.write, py.files.methods
  - Collect function results and write once / Evidence and next attempt: Actual source context and pending assignment; no additional learning concept.
- [Notes/Python/Logic/order-summary-after-loop.md](../../Notes/Python/Logic/order-summary-after-loop.md)
  - Count orders and write the summary after the loop: py.records.summary
  - Count orders and write the summary after the loop / Groups come from the status values: py.records.summary
  - Count orders and write the summary after the loop / Count first, write after the loop: py.records.summary
  - Count orders and write the summary after the loop / Trace the running totals: py.records.summary
  - Count orders and write the summary after the loop / Keep separate orders before summarising: py.list.records, py.records.summary
  - Count orders and write the summary after the loop / Learning context: Provenance and pending-practice status; no additional concept coverage.
- [Notes/README.md](../../Notes/README.md): Index, vault setup or curriculum administration; no assessed lesson content.
- [Notes/SQL/learning-notes.md](../../Notes/SQL/learning-notes.md)
  - sql learning notes: sql.count.nulls, sql.join.keys, sql.group.grain
  - sql learning notes / 15 October 2026 — LEFT JOIN preservation (SQL-001): sql.join.preservation
  - sql learning notes / 15 October 2026 — counting orders after LEFT JOIN (SQL-002): sql.count.nulls, sql.join.keys, sql.group.grain
- [Notes/Welcome.md](../../Notes/Welcome.md): Index, vault setup or curriculum administration; no assessed lesson content.
- [Notes/learning-and-revision-plan.md](../../Notes/learning-and-revision-plan.md): Index, vault setup or curriculum administration; no assessed lesson content.
- [Notes/revision/README.md](../../Notes/revision/README.md): Revision instructions, generated view or answer-free prompts; original explanations are mapped.
- [Notes/revision/ai-reminder-questions.md](../../Notes/revision/ai-reminder-questions.md): Revision instructions, generated view or answer-free prompts; original explanations are mapped.
- [Notes/revision/list-questions.md](../../Notes/revision/list-questions.md): Revision instructions, generated view or answer-free prompts; original explanations are mapped.
- [Notes/revision/mistakes.md](../../Notes/revision/mistakes.md): Revision instructions, generated view or answer-free prompts; original explanations are mapped.
- [Notes/revision/notebook-questions.md](../../Notes/revision/notebook-questions.md): Revision instructions, generated view or answer-free prompts; original explanations are mapped.
- [Notes/revision/plan.md](../../Notes/revision/plan.md): Revision instructions, generated view or answer-free prompts; original explanations are mapped.
- [Notes/revision/questions.md](../../Notes/revision/questions.md): Revision instructions, generated view or answer-free prompts; original explanations are mapped.
- [Notes/revision/reviews.jsonl](../../Notes/revision/reviews.jsonl): Image, asset or machine-readable view; learning is mapped from its explanation note.
- [Notes/revision/topics.json](../../Notes/revision/topics.json): Image, asset or machine-readable view; learning is mapped from its explanation note.
- [tools/airflow/notes.md](../../tools/airflow/notes.md): Empty lesson template; no substantive learning content yet.
- [tools/azure/notes.md](../../tools/azure/notes.md): Empty lesson template; no substantive learning content yet.
- [tools/data-modelling/notes.md](../../tools/data-modelling/notes.md): Empty lesson template; no substantive learning content yet.
- [tools/dbt/notes.md](../../tools/dbt/notes.md): Empty lesson template; no substantive learning content yet.
- [tools/docker/notes.md](../../tools/docker/notes.md): Empty lesson template; no substantive learning content yet.
- [tools/git/notes.md](../../tools/git/notes.md): Empty lesson template; no substantive learning content yet.
- [tools/pipeline-reliability/notes.md](../../tools/pipeline-reliability/notes.md): Empty lesson template; no substantive learning content yet.
- [tools/plsql/notes.md](../../tools/plsql/notes.md): Empty lesson template; no substantive learning content yet.
- [tools/postgresql/notes.md](../../tools/postgresql/notes.md): Empty lesson template; no substantive learning content yet.
- [tools/powerbi/notes.md](../../tools/powerbi/notes.md): Empty lesson template; no substantive learning content yet.
- [tools/pyspark/notes.md](../../tools/pyspark/notes.md): Empty lesson template; no substantive learning content yet.
- [tools/python/notes.md](../../tools/python/notes.md): Links to canonical vault explanations; no duplicate coverage.
- [tools/shell/notes.md](../../tools/shell/notes.md): Empty lesson template; no substantive learning content yet.
- [tools/snowflake/notes.md](../../tools/snowflake/notes.md): Empty lesson template; no substantive learning content yet.
- [tools/sql/notes.md](../../tools/sql/notes.md): Links to canonical vault explanations; no duplicate coverage.
