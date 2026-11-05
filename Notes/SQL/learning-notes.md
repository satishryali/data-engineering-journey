# sql learning notes

Purpose: preserve the entities being reported, then count the intended matches. Useful
for customer activity reports that must include customers without orders. The original
`exercises/` references below refer to `tools/sql/exercises/` in the learning repository.

Runnable PostgreSQL example (no persistent table changes):

```sql
WITH customers(customer_id, name) AS (VALUES (1, 'Asha'), (2, 'Nila')),
orders(order_id, customer_id) AS (VALUES (101, 1), (102, 1))
SELECT c.customer_id, c.name, COUNT(o.order_id) AS order_count
FROM customers AS c
LEFT JOIN orders AS o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY c.customer_id;
```

Expected rows: `(1, Asha, 2)` and `(2, Nila, 0)`. Pitfalls: COUNT(*) includes the
preserved unmatched row; shared names do not establish customer identity. Recall
questions are separate in [[revision/questions|Questions]]. This is a note based on
previously studied SQL, not a new assessed retrieval result.
Reference: https://www.postgresql.org/docs/current/functions-aggregate.html

## 15 October 2026 — LEFT JOIN preservation (SQL-001)

- INNER JOIN excludes customers with no matching order; LEFT JOIN from customers preserves them.
- With no matching right-table row, the selected order columns are NULL. A matching order whose other fields are NULL is a different case.
- One customer can occupy multiple joined rows when several orders match: Asha has orders 101 and 102.
- Evidence: independent original query and changed-input predictions/explanations; supplied PostgreSQL output includes Meera 104 and Nila NULL.
- Accuracy point: reconstruction used cusotmer_id; corrected after tutor spelling help. Preserve that distinction from independent join reasoning.
- Early retrieval due 16 October; see exercises/001-join-preservation/attempt.sql. Initial success is not proof of retained mastery.

## 15 October 2026 — counting orders after LEFT JOIN (SQL-002)

- COUNT(*) counts joined rows in each group, including a preserved unmatched customer row.
- COUNT(o.order_id) counts non-NULL order IDs. Nila therefore has zero actual orders even though her joined row exists.
- Group by customer ID and name to keep distinct customers separate even if names match.
- Learner supplied correct output: Asha 2, Ravi 1, Meera 1, Nila 0. Row order may vary without ORDER BY.
- Implementation required a hint on COUNT/NULL behaviour. CASE/COALESCE are unnecessary for this count; the extra non-NULL ON condition is redundant for this schema.
- Reconstruction needed join-key feedback; duplicate-name grouping needed a hint. Learner then supplied correct name-only and ID/name comparison outputs.
- Group by name alone merges different customers sharing a name. Group by customer ID and name keeps them separate; include ID in SELECT to distinguish displayed rows.
- Initial practice complete with assistance; early unaided practice due 16 October. Do not mark independent implementation mastery yet.

For each actual lesson record:
- Problem encountered:
- Why the first approach failed:
- Technique and reason:
- Small example or file link:
- Edge case / limitation:
- What I can do without help:
- Revision item ID:

## SQL joins: a small reference

We use a join when the information we need is split across tables. For example,
customers hold names and orders hold purchases. Join their customer IDs to show
each purchase beside the customer's name.

These are prepared reference examples, not an assessed learner attempt. SQL below
uses PostgreSQL syntax. All shown results are **Expected output**, not run results.

### Small input

Use this `WITH` block before each customer/order query below. It creates temporary
named results for that one query; it does not create database tables.

```sql
WITH customers(customer_id, name) AS (
    VALUES (1, 'Asha'), (2, 'Nila')
), orders(order_id, customer_id) AS (
    VALUES (101, 1), (102, 1), (103, 3)
)
```

Asha has two orders. Nila has none. Order 103 has no matching customer in this
sample. It illustrates unmatched data; a foreign key would normally prevent an
order from referring to a missing customer.

### INNER JOIN: keep matching pairs

```sql
SELECT c.name, o.order_id
FROM customers AS c
INNER JOIN orders AS o ON c.customer_id = o.customer_id
ORDER BY o.order_id;
```

**Expected output**

| name | order_id |
| --- | --- |
| Asha | 101 |
| Asha | 102 |

`c` and `o` are short table names, called aliases. `ON` states how rows match.
Use the related customer IDs, not the order ID or a name that might repeat.
One row is returned for **each matching pair**: two orders mean two Asha rows.

### LEFT JOIN: keep every customer

```sql
SELECT c.name, o.order_id
FROM customers AS c
LEFT JOIN orders AS o ON c.customer_id = o.customer_id
ORDER BY c.customer_id, o.order_id;
```

**Expected output**

| name | order_id |
| --- | --- |
| Asha | 101 |
| Asha | 102 |
| Nila | NULL |

The left table is the table before `LEFT JOIN`. Nila stays in the result even
without a matching order. The order columns contain NULL, meaning no value here.
Order 103 is not included because this join preserves customers.

### RIGHT JOIN and FULL OUTER JOIN

Using the same input:

```sql
SELECT c.name, o.order_id
FROM customers AS c
RIGHT JOIN orders AS o ON c.customer_id = o.customer_id
ORDER BY o.order_id;
```

**Expected output:** Asha / 101, Asha / 102, NULL / 103.

`RIGHT JOIN` keeps every row from the right table: orders here. You can express
the same result by starting with orders and using `LEFT JOIN customers`.

```sql
SELECT c.name, o.order_id
FROM customers AS c
FULL OUTER JOIN orders AS o ON c.customer_id = o.customer_id
ORDER BY c.customer_id NULLS LAST, o.order_id;
```

**Expected output:** Asha / 101, Asha / 102, Nila / NULL, NULL / 103.

`FULL OUTER JOIN` keeps matching pairs plus unmatched rows from both tables.
It is useful for comparing two sources and finding missing records.

### CROSS JOIN: every combination

```sql
WITH sizes(size) AS (VALUES ('S'), ('M')),
colours(colour) AS (VALUES ('Blue'), ('Red'))
SELECT s.size, c.colour
FROM sizes AS s
CROSS JOIN colours AS c
ORDER BY s.size, c.colour;
```

**Expected output:** M / Blue, M / Red, S / Blue, S / Red.

There is no match condition. Two sizes times two colours gives four combinations.
Check the row count before using this with large tables.

### Self join: use the same table twice

```sql
WITH employees(employee_id, name, manager_id) AS (
    VALUES (1, 'Ravi', NULL::integer), (2, 'Priya', 1)
)
SELECT e.name AS employee, m.name AS manager
FROM employees AS e
LEFT JOIN employees AS m ON e.manager_id = m.employee_id
ORDER BY e.employee_id;
```

**Expected output:** Ravi / NULL, Priya / Ravi.

`e` means the employee row and `m` means the manager row from the same table.
A self join is a way to use a table twice; INNER or LEFT still decides which
unmatched rows remain.

### Filtering after LEFT JOIN

Using the customer/order input again, compare these two queries:

```sql
SELECT c.name, o.order_id
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id AND o.order_id = 101
ORDER BY c.customer_id;
```

**Expected output:** Asha / 101, Nila / NULL.
The extra `ON` condition chooses which orders match. Every customer still stays.

```sql
SELECT c.name, o.order_id
FROM customers AS c
LEFT JOIN orders AS o ON c.customer_id = o.customer_id
WHERE o.order_id = 101
ORDER BY c.customer_id;
```

**Expected output:** Asha / 101 only.
`WHERE` filters the joined result. Nila's NULL order ID does not satisfy `= 101`,
so her row disappears. Use `WHERE o.order_id IS NULL` instead when the goal is
to find customers without any order; here it returns Nila / NULL because actual
order IDs in this input are non-NULL.

### Remember

- Equality joins do not match NULL to NULL: `NULL = NULL` is unknown, not true.
- Repeated join keys can multiply rows. If a key occurs twice on each side,
  that key produces four matching pairs. Check the keys before adding DISTINCT.
- After LEFT JOIN, `COUNT(o.order_id)` counts non-NULL order IDs; `COUNT(*)`
  also counts the preserved unmatched row. See SQL-002 above.
- Results need `ORDER BY` if their displayed order matters.

Reference: [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN).
