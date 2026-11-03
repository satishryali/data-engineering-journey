# Oracle SQL revision — 3 November 2026

Use SQL to select employees, filter rows and build department reports. These notes collect the topics practised in this chat, with extra detail where NULL, CASE and counting caused confusion.

## Practice table

Run this once in an Oracle practice schema. Do not rerun the inserts unless you have removed the existing practice rows; the primary key prevents duplicate IDs.

```sql
CREATE TABLE employees_practice (
    employee_id NUMBER PRIMARY KEY,
    employee_name VARCHAR2(50),
    department VARCHAR2(30),
    salary NUMBER
);

INSERT ALL
    INTO employees_practice VALUES (101, 'Ravi', 'IT', 45000)
    INTO employees_practice VALUES (102, 'Priya', 'Finance', 55000)
    INTO employees_practice VALUES (103, 'Arun', 'IT', 60000)
    INTO employees_practice VALUES (104, 'Neha', NULL, 50000)
    INTO employees_practice VALUES (105, 'Kiran', 'HR', 48000)
SELECT 1 FROM dual;
COMMIT;
```

Neha has a NULL **department**, not a NULL salary. The later 10,000 / 20,000 / NULL salary example is separate hypothetical data.

All outputs below are **expected output**, not execution verified by the note writer. Without ORDER BY, row order is not guaranteed.

## Select columns and filter rows

SELECT chooses the columns. WHERE keeps rows that meet a condition.

```sql
SELECT employee_name, salary
FROM employees_practice
WHERE salary > 50000;
```

Expected output: Priya — 55000; Arun — 60000.

```sql
SELECT employee_name, salary
FROM employees_practice
WHERE salary > 50000 AND department = 'IT';
```

Expected output: Arun — 60000. Both conditions must be TRUE. Use the actual column name `department`, not `department_name` or `deparment`.

## AND, OR and IN

AND is evaluated before OR. Use parentheses when either department should qualify but the salary condition must apply to both.

```sql
SELECT employee_name, department, salary
FROM employees_practice
WHERE (department = 'IT' OR department = 'Finance')
  AND salary > 50000;
```

Expected output: Priya — Finance — 55000; Arun — IT — 60000.

Without parentheses, `department = 'IT' OR department = 'Finance' AND salary > 50000` also includes Ravi: the salary check applies only to the Finance branch.

For this equality list, IN is a shorter way to express the parenthesized OR:

```sql
WHERE department IN ('IT', 'Finance') AND salary > 50000
```

This is a WHERE-clause fragment to use with the SELECT above.

## Sort rows

```sql
SELECT employee_name, salary
FROM employees_practice
ORDER BY salary DESC;
```

Expected order: Arun 60000, Priya 55000, Neha 50000, Kiran 48000, Ravi 45000. DESC means highest first; ASC means lowest first.

## BETWEEN and LIKE

BETWEEN includes both limits.

```sql
SELECT employee_name, salary
FROM employees_practice
WHERE salary BETWEEN 45000 AND 55000;
```

Expected employees: Ravi, Priya, Neha and Kiran. The original three-row table returned only Ravi and Priya.

```sql
SELECT * FROM employees_practice WHERE employee_name LIKE 'A%';
SELECT * FROM employees_practice WHERE employee_name LIKE '_r%';
```

Expected employees: first query Arun; second query Priya and Arun.

- `%` matches zero or more characters.
- `_` matches exactly one character. `_r%` places `r` in the second position.

## NULL and filtering

NULL means a missing or unknown value. Ordinary comparisons involving NULL return UNKNOWN, even `NULL = NULL` and `NULL <> NULL`.

WHERE keeps only TRUE. It rejects FALSE and UNKNOWN.

| Department | `department <> 'IT'` | Included by that condition? |
| --- | --- | --- |
| IT | FALSE | No |
| Finance | TRUE | Yes |
| NULL | UNKNOWN | No |

Use IS NULL or IS NOT NULL to check for missing values:

```sql
SELECT * FROM employees_practice WHERE department IS NULL;
```

Expected employee: Neha.

```sql
SELECT *
FROM employees_practice
WHERE department <> 'IT' OR department IS NULL;
```

Expected employees: Priya, Neha and Kiran. For Neha, UNKNOWN OR TRUE is TRUE.

`department NOT IN ('IT')` also excludes NULL departments unless you add `OR department IS NULL`. Using AND instead returns no rows: an ordinary department fails IS NULL, and a NULL department produces UNKNOWN AND TRUE.

`NULL` is different from `'Null'`: the latter is text. Keyword spelling such as `NULL` or `NUll` does not change the keyword.

## DISTINCT and counting

DISTINCT removes duplicate combinations of the selected columns. With just department selected:

```sql
SELECT DISTINCT department FROM employees_practice;
```

Expected values: IT, Finance, HR and one NULL — four rows.

```sql
SELECT COUNT(*) AS total_rows,
       COUNT(department) AS department_count,
       COUNT(DISTINCT department) AS unique_department_count
FROM employees_practice;
```

Expected output:

| total_rows | department_count | unique_department_count |
| ---: | ---: | ---: |
| 5 | 4 | 3 |

- COUNT(*) counts rows.
- COUNT(column) counts non-NULL values in that column.
- COUNT(DISTINCT column) counts different non-NULL values.
- SELECT DISTINCT can return one NULL; COUNT(DISTINCT column) ignores NULL.

Related earlier work: [counting orders after a LEFT JOIN](learning-notes.md#15-october-2026--counting-orders-after-left-join-sql-002).

## GROUP BY and HAVING

GROUP BY combines rows with the same department into one report group. HAVING filters those groups.

```sql
SELECT department, COUNT(*) AS employee_count
FROM employees_practice
GROUP BY department;
```

Expected output:

| department | employee_count |
| --- | ---: |
| IT | 2 |
| Finance | 1 |
| HR | 1 |
| NULL | 1 |

Five input rows produce four groups. NULL departments form a group too. Replacing COUNT(*) with COUNT(department) makes the NULL group's count zero; the group still exists. With three NULL-department rows, that group would have COUNT(*) = 3 and COUNT(department) = 0.

```sql
SELECT department, COUNT(*) AS employee_count
FROM employees_practice
GROUP BY department
HAVING COUNT(*) > 1;
```

Expected output: IT — 2.

## WHERE before grouping

WHERE filters individual employees first. GROUP BY groups the remaining employees. HAVING then filters the groups.

```sql
SELECT department, COUNT(*) AS employee_count
FROM employees_practice
WHERE salary > 50000
GROUP BY department
HAVING COUNT(*) >= 2;
```

Expected output: no rows. Only Priya and Arun qualify, and they belong to different departments.

An alternative approach also works: filter salaries inside an inline view, then group its result. An inline view means a query used inside FROM.

```sql
SELECT department, COUNT(*) AS employee_count
FROM (SELECT * FROM employees_practice WHERE salary > 50000)
GROUP BY department
HAVING COUNT(*) >= 2;
```

## AVG and NVL

AVG ignores NULL values. NVL(value, replacement) supplies a replacement when the value is NULL.

This standalone example uses different data from employees_practice:

```sql
WITH sample_salaries AS (
    SELECT 10000 AS salary FROM dual
    UNION ALL SELECT 20000 FROM dual
    UNION ALL SELECT CAST(NULL AS NUMBER) FROM dual
)
SELECT AVG(salary) AS average_known_salary,
       AVG(NVL(salary, 0)) AS average_with_zero
FROM sample_salaries;
```

Expected output: 15000 and 10000.

- AVG(salary): (10000 + 20000) / 2.
- AVG(NVL(salary, 0)): (10000 + 20000 + 0) / 3.

Replacing unknown values with zero changes the meaning of the average. Use it only when zero is the intended business treatment.

## CASE and condition order

CASE chooses a value for each row. It uses the first TRUE condition and finishes with END.

```sql
SELECT employee_name, salary,
       CASE
           WHEN salary >= 60000 THEN 'High'
           WHEN salary >= 50000 THEN 'Medium'
           WHEN salary < 50000 THEN 'Low'
           ELSE 'Unknown'
       END AS salary_band
FROM employees_practice;
```

Expected bands: Ravi Low, Priya Medium, Arun High, Neha Medium, Kiran Low. A NULL salary would reach Unknown.

The second condition needs no upper bound: salaries of 60000 or more already matched High. Putting `salary >= 50000` first would label both 60000 and 70000 Medium.

`salary >= 50000 AND salary < 50000` can never be TRUE. An explicit Medium range would be `salary >= 50000 AND salary < 60000`.

If ELSE is omitted, unmatched rows return NULL. Do not omit END or leave a comma immediately before FROM.

## Count only matching rows

Conditional aggregation means choosing values with CASE and then combining those values with COUNT or SUM. It lets one report contain different measures.

```sql
SELECT
    COUNT(CASE WHEN salary >= 60000 THEN 1 END) AS high_salary_count,
    COUNT(CASE WHEN salary < 60000 OR salary IS NULL THEN 1 END)
        AS other_salary_count
FROM employees_practice;
```

Expected output: high_salary_count = 1, other_salary_count = 4.

CASE supplies 1 for a qualifying employee and NULL otherwise. COUNT ignores those NULL results. A NULL salary belongs to the second count explicitly.

Do not use `ELSE 0` inside COUNT when counting only matches: zero is non-NULL, so COUNT counts it too. A text value such as `ELSE 'Unknown'` also cannot stand for an ignored row, and mixing numeric and character CASE results can produce a datatype error.

## SUM with CASE: follow each row

```sql
SELECT SUM(CASE WHEN salary >= 60000 THEN 1 ELSE 0 END)
       AS high_salary_count
FROM employees_practice;
```

Expected output: 1.

| Employee | CASE result |
| --- | ---: |
| Ravi | 0 |
| Priya | 0 |
| Arun | 1 |
| Neha | 0 |
| Kiran | 0 |

SUM adds the values: 0 + 0 + 1 + 0 + 0 = 1. COUNT with the same CASE would count all five values, including the zeros.

For three qualifying employees and two others: SUM gets 1 + 1 + 1 + 0 + 0 = 3. For two qualifying employees and four others, it gets 2.

This version is also valid:

```sql
SELECT SUM(CASE WHEN salary >= 60000 THEN 1 END) AS high_salary_count
FROM employees_practice;
```

It also returns 1 for our data. With employees present but no matches, it returns NULL because every CASE result is NULL. Adding ELSE 0 returns zero in that situation. On an empty table, SUM returns NULL even with ELSE 0; COUNT returns zero.

## Add matching salaries

Use the actual salary as the CASE result when the goal is money totals rather than employee counts.

Example query:

```sql
SELECT SUM(CASE WHEN department = 'IT' THEN salary END) AS it_total_salary
FROM employees_practice;
```

Expected output: 105000. Ravi contributes 45000; Arun contributes 60000; the other rows contribute NULL, which SUM ignores.

Compare: THEN 1 counts matching employees when summed; THEN salary adds their salary amounts.

## Sources and practice

Source used during this revision: [Oracle Basics](https://www.oracletutorial.com/oracle-basics/).
Related reference: [earlier SQL notes](learning-notes.md).

For practice, attempt a query first, consult the missing concept, then close the note and reconstruct the query. Try a changed example before a later review.
