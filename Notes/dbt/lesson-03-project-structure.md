# Lesson 3: Project structure and starter models

The project holds SQL transformations, settings, descriptions, and tests together so we can understand and maintain the pipeline.

## Files and folders

| Location | Purpose |
| --- | --- |
| `dbt_project.yml` | Project name, selected profile, paths, and default configuration |
| `models/` | SQL models and related YAML definitions |
| `seeds/` | Small reference CSV files |
| `snapshots/` | Historical-change definitions |
| `tests/` | Standalone SQL tests |
| `macros/` | Reusable Jinja/SQL logic |
| `analyses/` | SQL dbt can compile without building it as a model |
| `target/` | Generated compiled SQL and artifacts |
| `logs/` | Run logs |

Some folders can be empty or generated later. SQL describes how to produce data. YAML describes settings, documentation, and tests.

## Project name, folder name, and version

The inspected project is located at:

```text
TESTING/
  dbt_practice/             <- Parent practice folder
    airbnb_dbt/            <- Project folder
      dbt_project.yml
```

Its project file contains:

```yaml
name: airbnb_dbt
version: '1.0.0'
profile: airbnb_dbt
```

- `name` is the internal project name. It does not point to a folder.
- `version` labels your project's release. It is separate from the installed dbt version and does not increase automatically.
- `profile` selects connection settings from `profiles.yml`.

You can rename the project folder to `airbnb_practice` and keep `name: airbnb_dbt`. Run dbt from the renamed project folder. `dbt debug` will check the configuration; it will not adjust the YAML name to match the folder.

The folder name, internal project name, profile name, and database name are separate things, even when several use the same text.

## Load one small CSV seed

Seeds make small reference data available as database tables. For example, create `seeds/country_codes.csv`:

```csv
code,country
IN,India
GB,United Kingdom
```

From the project folder, run:

```powershell
dbt seed --select country_codes
```

Expected behaviour: dbt loads only this seed as a table named `country_codes` in the default destination schema, unless seed configuration changes it. The table has two data rows. The selector is the filename without `.csv`.

`dbt seed` loads all enabled seeds. For several files, use a selection such as `dbt seed --select "country_codes full_moon_dates"`.

There is no single universal KB/MB limit for local PostgreSQL seeds. Available memory, adapter behaviour, and database limits affect what is practical. Seeds are intended for small reference files that change infrequently; they are not a bulk loader for large transaction datasets. The CSV example above was not executed during this save.

## Analyses are saved investigation queries

Use `analyses/` when you want to keep a query for answering a question without making it a model table or view.

For example, save `analyses/count_starter_rows.sql`:

```sql
select count(*) as row_count
from {{ ref('my_first_dbt_model') }}
```

Run `dbt compile` to turn the Jinja reference into ordinary SQL. The generated query will be under:

```text
target/compiled/airbnb_dbt/analyses/count_starter_rows.sql
```

Copy that compiled query into pgAdmin and execute it to get an answer. The referenced model must already exist when you execute the query. If the unchanged starter model has been built, the expected count is `2`.

dbt compiles analysis SQL; it does not execute the analysis or create its result table. A model is for a dataset dbt builds. An analysis is a query you keep for investigation. This example is an explanation, not a saved learner query or verified database result.

## Where target and logs appear

`target/` is a generated folder inside the project, beside `dbt_project.yml`. It was absent when the learner's project folder was inspected during this conversation.

After a successful `dbt compile`, the default layout includes:

```text
airbnb_dbt/
  dbt_project.yml
  models/
  target/
    compiled/
```

You do not need to create `target/` by hand. Edit your source files in `models/` and `analyses/`; dbt regenerates the compiled files. Commands such as `dbt run` and `dbt test` also write artifacts, including `target/run_results.json` with execution summaries. `logs/dbt.log` holds detailed logs.

The `target/` folder is on your computer. Your output tables and views are in PostgreSQL. Also, `target: dev` in the profile means a selected connection; it is separate from this folder.

## First starter model and materialization

The inspected first model contains:

```sql
{{ config(materialized='table') }}

with source_data as (
    select 1 as id
    union all
    select null as id
)
select *
from source_data
-- where id is not null
```

Materialization means how dbt builds the model result in PostgreSQL.

Read `{{ config(materialized='table') }}` as: "For this model, save the query result as a database table." `config()` sets model options. dbt reads this Jinja instruction before PostgreSQL executes the generated SQL.

| Setting | Behaviour |
| --- | --- |
| `table` | Stores the query's resulting rows |
| `view` | Stores a query definition that reads underlying data when queried |

Expected first-model rows: `1` and `NULL`. The filter is commented out, so it does not remove the null. The inline table configuration overrides the project's example-folder view default.

For the file `my_first_dbt_model.sql`, the default result name is `my_first_dbt_model`. If the destination schema is `analytics`, the table is `analytics.my_first_dbt_model`. A configured alias or custom schema can change the location/name. A table stores the rows produced at build time; it does not automatically recalculate when source data changes. A view runs its saved query when read.

This model SQL contains Jinja configuration and should be run through dbt, not pasted unchanged into a PostgreSQL query editor. Plain SQL inside the model can be inspected separately.

## Second starter model

```sql
select *
from {{ ref('my_first_dbt_model') }}
where id = 1
```

`ref()` points to the first model and tells dbt about the dependency. Expected second-model output: one row with `id = 1`.

## Why schema.yml exists

The example YAML describes models and declares tests:

```yaml
version: 2

models:
  - name: my_first_dbt_model
    description: "A starter dbt model"
    columns:
      - name: id
        description: "The primary key for this table"
        data_tests:
          - unique
          - not_null
```

`version: 2` identifies the properties-file format. It is not the installed dbt version, PostgreSQL version, or a model version.

The filename `schema.yml` does not create a PostgreSQL schema. The same contents can be placed in a suitably located file named `models.yml`.

The primary-key description is text for readers. It does not create a database primary-key constraint.

## Unique and not-null tests

| Test | What it checks | Expected result for `1`, `NULL` |
| --- | --- | --- |
| `unique` | No duplicate non-null values | Pass: `1` occurs once; nulls are excluded |
| `not_null` | No missing values | Fail: one null exists |

Use both when an ID must always be present and unique. Tests report problems; they do not remove or repair records. Declaring tests is not the same as executing them.

The inspected YAML applies both tests to the second starter model too. No test execution was supplied during these lessons. Predictions above are expected behaviour, not verified run results.

## Where test results are stored

Run data tests using:

```powershell
dbt test
```

By default, the terminal shows statuses such as PASS and FAIL, and local artifacts record execution summaries. The terminal does not normally print every failing data row. Failing records are not normally saved as permanent database tables.

To save the failing records for investigation:

```powershell
dbt test --store-failures
```

Unless overridden by test configuration, dbt stores failing rows in database tables. The default audit schema is based on the profile schema, for example `analytics_dbt_test__audit`. The user needs permission to create/access it. A later run replaces the saved failures for the same test; this is not a full historical results log.

These commands are reference examples. No tests or database writes were executed during this save.

## Learning evidence and references

The learner identified the second model's dependency. They asked about materialized, version, and the YAML file's purpose; the tutor explained these. After explanation, the learner correctly predicted not_null failure and unique success. This is immediate guided practice, not delayed retention or independent model implementation. No mistake record is inferred merely from asking these questions.

[Materializations](https://docs.getdbt.com/docs/build/materializations), [dbt projects](https://docs.getdbt.com/docs/build/projects).

[Project name](https://docs.getdbt.com/reference/project-configs/name), [Project version](https://docs.getdbt.com/reference/project-configs/version), [Seed selection](https://docs.getdbt.com/reference/commands/seed), [Analyses](https://docs.getdbt.com/docs/build/analyses), [Compile](https://docs.getdbt.com/reference/commands/compile), [Store test failures](https://docs.getdbt.com/reference/resource-configs/store_failures).

Follow-up saved on 4 November 2026: the learner asked about project/folder names, renaming, seed size and selection, test output, analyses, the missing target folder, and the meaning of materialized. The tutor explained these and inspected the real project name/folder layout. Examples are explained material, not an independent learner implementation or a scored review.
