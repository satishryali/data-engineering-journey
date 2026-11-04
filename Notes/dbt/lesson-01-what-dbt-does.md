# Lesson 1: What dbt does

We need to turn raw data into clean tables that reports can use. dbt helps organise those SQL transformations and build them in the database.

## The three tools

| Tool | Responsibility |
| --- | --- |
| dbt | Reads configuration, prepares SQL, manages model dependencies, and submits SQL to PostgreSQL |
| PostgreSQL | Stores the data, executes SQL, and stores the resulting tables or views |
| Airflow | Schedules/triggers the pipeline, controls task order, tracks failures, and manages retries |

In our setup, dbt runs on the laptop. PostgreSQL runs on the home server. Airflow is planned for later; no working DAG has been verified.

dbt manages the order of its models. Airflow coordinates larger steps such as extract, load, dbt build, and notification.

## Extract, load, transform

| Step | Meaning | Example |
| --- | --- | --- |
| Extract | Get source data | Download Airbnb files |
| Load | Put it into a database | Load files into PostgreSQL |
| Transform | Prepare useful datasets | Clean prices and count listings per host |

This order is called ELT. Our main dbt work is the transformation step. dbt seeds can load small reference CSVs, but the general source-ingestion pipeline is separate.

## A small transformation

Goal: count listings and calculate their average price per host. This standalone PostgreSQL query uses imaginary data, not our unverified source columns.

```sql
with listings(listing_id, host_id, price) as (
    values (101, 10, '$100.00'),
           (102, 10, '$150.00'),
           (103, 20, '$80.00')
)
select
    host_id,
    count(*) as listing_count,
    avg(replace(price, '$', '')::numeric(10, 2))::numeric(10, 2) as average_price
from listings
group by host_id
order by host_id;
```

Expected output:

| host_id | listing_count | average_price |
| --- | --- | --- |
| 10 | 2 | 125.00 |
| 20 | 1 | 80.00 |

`replace` removes the dollar sign. The numeric cast makes prices numbers. Grouping produces one row per host. In a dbt model, dbt manages the SQL; PostgreSQL performs the calculation.

## Why use dbt with SQL

dbt helps organise SQL models, run them in dependency order, test results, and document how datasets relate. Its text files can be tracked in Git.

If PostgreSQL is stopped, dbt cannot rebuild the report. The data can still exist on disk, but it is inaccessible until the database is available. A previously exported report may remain available elsewhere.

## Learning evidence and references

The learner explained the roles of dbt, PostgreSQL, and Airflow, and correctly predicted that dbt cannot rebuild when PostgreSQL is off. Tutor clarified that PostgreSQL executes the SQL and stopped services do not imply deleted data. No independent implementation or delayed recall was assessed.

[dbt projects](https://docs.getdbt.com/docs/build/projects).
