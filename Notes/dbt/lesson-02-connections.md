# Lesson 2: Connections and profiles

dbt needs the server address, database, login, and output location before it can build models.

## Project selects a profile

The project file `dbt_project.yml` contains:

```yaml
profile: airbnb_dbt
```

dbt looks for the matching `airbnb_dbt` profile in the connection file. On this laptop that file is `C:/Users/SATISH/.dbt/profiles.yml`, outside the project.

## Profile selects a target

Example structure only. Do not replace a working password with the placeholder.

```yaml
airbnb_dbt:
  target: dev
  outputs:
    dev:
      type: postgres
      host: 192.168.1.195
      port: 5432
      user: postgres
      pass: YOUR_PASSWORD
      dbname: airbnb_dbt
      schema: raw
      threads: 1
```

| Setting | Meaning |
| --- | --- |
| `airbnb_dbt` | Profile matched by the project |
| `target: dev` | Select `outputs.dev` |
| `type` | Adapter; the component that lets dbt work with PostgreSQL |
| `host` / `port` | Database server address and listening port |
| `user` / `pass` | Login credentials |
| `dbname` | Database to connect to |
| `schema` | Default destination for dbt models |
| `threads` | Maximum model-execution threads dbt can use |

Read the settings as a process: find the profile, choose its target, load the PostgreSQL adapter, contact the host and port, log in, open the database, and build models in the destination schema. `threads: 1` allows one model at a time. Higher values allow independent models to run together; dependencies still have to finish first.

The profile name and database name happen to both be `airbnb_dbt`. They are separate settings and can have different names.

Changing `target` to `practice` requires a `practice:` entry under `outputs` with its connection settings.

## Multiple connections and the default

Define `target:` once in a profile. Put each available connection under `outputs`:

```yaml
airbnb_dbt:
  target: dev
  outputs:
    dev:
      # Complete development connection settings go here.
    stg:
      # Complete staging connection settings go here.
    prod:
      # Complete production connection settings go here.
```

This shows the structure only; the comments are not working connection details.

| Command | Connection selected |
| --- | --- |
| `dbt run` | `dev`, the configured default |
| `dbt run --target stg` | `stg` for this command |
| `dbt run --target prod` | `prod` for this command |

The command option does not edit the default in the file. dbt does not run all three connections or choose randomly.

If `prod` is missing under `outputs`, `dbt run --target prod` fails before building models. It does not fall back to `dev`. A `prod` entry with missing required connection fields also fails validation.

Names such as `dev`, `stg`, and `practice` are labels you choose. They do not create databases. Do not repeat `target: dev`, `target: stg`, and `target: prod` in the same profile: these are duplicate YAML keys, not three selections.

## Database and schema

```text
PostgreSQL server
  -> database: airbnb_dbt
     -> schema: raw
        -> table: raw_hosts
```

Changing only `schema: raw` to `schema: analytics` does not change the server or database. It changes the default output location. The source data can stay in `raw` while models write to `analytics`.

The profile schema does not select all source tables. Sources are declared separately in a later lesson. During a model run, dbt can create a missing destination schema if the login has permission. Editing YAML alone or running `dbt debug` does not create that model schema.

| Object | What happens in this PostgreSQL setup? |
| --- | --- |
| Database | Must already exist so dbt can connect |
| Destination schema | dbt can create it if needed and permitted |
| Model table or view | dbt creates it according to the model's materialization |
| Existing source table | Must already be available for the model to read |

An object is a general name for something in a database, such as a schema, table, or view. dbt does not automatically create every kind of database object.

## Source and destination use the connection

The connection settings tell dbt how to access PostgreSQL. Your model's SQL tells it which input to read. The same connection normally reads the source and writes the result.

For example, with `dbname: airbnb_dbt` and `schema: analytics`:

```text
Database: airbnb_dbt
raw.raw_hosts -> model SQL -> analytics.clean_hosts
    source                      destination
```

The source stays in `raw`. The profile's `schema: analytics` sets the default output location. Model settings can change that destination.

Source declarations name existing tables. This is an illustrative definition, not a verified source declaration in the learner's project:

```yaml
# models/sources.yml
version: 2

sources:
  - name: airbnb
    schema: raw
    tables:
      - name: raw_hosts
```

A model can read that table using:

```sql
select *
from {{ source('airbnb', 'raw_hosts') }}
```

`airbnb` matches the source label in YAML. `raw_hosts` matches its table entry. dbt resolves this to the existing `raw.raw_hosts` table in the connected database. The source declaration does not create or load the input table.

For this PostgreSQL project, source definitions are not a second login to another server. Data from an outside system normally needs to be loaded into the connected database first, unless separate database integration has been set up.

## What dbt debug checks

Run from the project directory with the project's virtual environment activated:

```powershell
cd C:\Users\SATISH\GIT\TESTING\dbt_practice\airbnb_dbt
dbt debug
```

It checks configuration, relevant dependencies, and the database connection. The inspected log showed a small connection query:

```sql
select 1 as id;
```

Expected query result: one row with `id = 1`. A successful connection check reports:

```text
Connection test: [OK connection ok]
All checks passed!
```

This does not build transformation models or prove all required table permissions/data are correct. Earlier errors included a wrong password and invoking debug from the parent folder. The project-local log later recorded a successful connection check at 18:38:48 on 4 November 2026; no fresh check was run during this note save.

`dbt debug` checks settings; it does not rewrite `dbt_project.yml` after a folder rename.

## Learning evidence and references

The learner correctly explained the matching `practice` output and that changing the schema keeps the same server. Tutor added the creation/permission condition. No profile-edit exercise or new database execution was verified. Keep real credentials outside notes and Git.

[dbt debug](https://docs.getdbt.com/reference/commands/debug), [PostgreSQL setup](https://docs.getdbt.com/docs/local/connect-data-platform/postgres-setup).

[Profile and target selection](https://docs.getdbt.com/docs/local/profiles.yml), [Sources](https://docs.getdbt.com/docs/build/sources), [Schema creation](https://docs.getdbt.com/docs/build/sql-models).

Follow-up saved on 4 November 2026: the learner asked about each connection field, multiple targets, missing targets, custom target names, object creation, and source selection. The learner restated that the profile schema is the destination. Explanations and examples were tutor-supplied; no new connection edit, source query, or model execution was demonstrated.
