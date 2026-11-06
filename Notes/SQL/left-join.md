# LEFT JOIN

## Why we need it

Sometimes we need every row from one table, even when there is no related row in
another table. A `LEFT JOIN` keeps all rows from the left table and adds matching
values from the right table.

For example, a customer report may need to show customers who have not placed an
order yet.

## Small input

This example creates temporary named results for one query. It does not create
permanent database tables.

```sql
WITH customers(customer_id, customer_name) AS (
    VALUES (1, 'Asha'), (2, 'Nila')
), orders(order_id, customer_id) AS (
    VALUES (101, 1), (102, 1)
)
```

- Asha has two orders.
- Nila has no order.

## Keep every customer

```sql
WITH customers(customer_id, customer_name) AS (
    VALUES (1, 'Asha'), (2, 'Nila')
), orders(order_id, customer_id) AS (
    VALUES (101, 1), (102, 1)
)
SELECT c.customer_name, o.order_id
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
ORDER BY c.customer_id, o.order_id;
```

**Expected output**

| customer_name | order_id |
| --- | ---: |
| Asha | 101 |
| Asha | 102 |
| Nila | NULL |

The table before `LEFT JOIN` is the left table: `customers`. Therefore both
customers remain in the result. Nila has no matching order, so the right-table
column `order_id` is `NULL`.

## One row for each match

The join does not combine all orders into one cell. It returns one row for each
matching pair.

If one customer has three orders, that customer appears in three joined rows.
This is important before using `COUNT`, `SUM` or `DISTINCT`.

## Count real orders

After a `LEFT JOIN`, `COUNT(*)` and `COUNT(o.order_id)` mean different things.

```sql
WITH customers(customer_id, customer_name) AS (
    VALUES (1, 'Asha'), (2, 'Nila')
), orders(order_id, customer_id) AS (
    VALUES (101, 1), (102, 1)
)
SELECT c.customer_name,
       COUNT(o.order_id) AS order_count
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY c.customer_id;
```

**Expected output**

| customer_name | order_count |
| --- | ---: |
| Asha | 2 |
| Nila | 0 |

- `COUNT(o.order_id)` counts non-`NULL` order IDs, so it counts actual orders.
- `COUNT(*)` counts joined rows. Nila still has one preserved joined row, so
  `COUNT(*)` would return `1` for Nila.

## Put conditions in ON or WHERE

The location of a condition changes the result.

### Condition in ON: keep every customer

```sql
SELECT c.customer_name, o.order_id
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
   AND o.order_id = 101;
```

This keeps every customer, but only order `101` is allowed to match. Customers
without that order receive `NULL` for the order columns.

### Condition in WHERE: remove unmatched rows

```sql
SELECT c.customer_name, o.order_id
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
WHERE o.order_id = 101;
```

This returns only Asha with order `101`. Nila is removed because `NULL = 101`
is not true. A `WHERE` condition on a right-table column can make a `LEFT JOIN`
behave like an inner join for that condition.

## Find customers without orders

When the right-side key is never `NULL` for a real order, use `IS NULL`:

```sql
SELECT c.customer_id, c.customer_name
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

**Expected output**

| customer_id | customer_name |
| ---: | --- |
| 2 | Nila |

## Common mistakes

- Joining customer names instead of stable IDs can match the wrong rows when two
  customers have the same name.
- Using `COUNT(*)` when the goal is to count orders counts the preserved customer
  row too. Use `COUNT(o.order_id)` when order IDs are non-`NULL`.
- Adding a right-table filter in `WHERE` can remove customers with no match. Put
  the filter in `ON` when those customers must stay.
- Repeated keys can multiply rows. Check the relationship before adding
  `DISTINCT` to hide duplicates.
- `NULL = NULL` is not true in SQL. Use `IS NULL` to test for missing values.

## Remember

- `LEFT JOIN` keeps every row from the table on the left.
- Matching rows from the right are added.
- No match means right-table columns are `NULL`.
- One left row can produce several output rows when several right rows match.

Related note: [SQL learning notes](learning-notes.md).

Reference: [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN).
