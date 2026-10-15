# Exercise 001: preserve customers without orders

Status: assigned; no solution submitted. Revision item SQL-001.

## Input

customers: (1, Asha), (2, Ravi), (3, Meera).
orders (order_id, customer_id): (101, 1), (102, 1), (103, 2).

Run setup.sql in a PostgreSQL session to create temporary sample tables. They live only in that connection; keep the same session for your query. No permanent tables are modified.

## Prediction before execution

```sql
SELECT c.name, o.order_id
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;
```

1. How many rows will this produce?
2. Does Meera appear? Why?
3. Modify the query so every customer appears; predict Meera's order_id.

Write your attempt in attempt.sql. Check the result only after your prediction. Completion requires a correct query plus an explanation of unmatched rows; then the tutor assigns a changed input. No totals, dates or status filters yet.
