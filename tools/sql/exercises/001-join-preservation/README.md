# Exercise 001: preserve customers without orders

Status: initial learning completed 15 October 2026. Learner supplied correct LEFT JOIN, predictions/explanations and changed-example output; reconstruction needed a column-spelling correction. Revision item SQL-001; early retrieval due 16 October. See attempt.sql for preserved attempts, help and output. Long-term mastery not assessed.

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

## Changed example 1 — assigned 15 October 2026

Keep the same three customers and the same query. Imagine adding one order:
orders (order_id, customer_id) now contains (101, 1), (102, 1), (103, 2), (104, 3).

Before running anything, predict:

1. How many rows does your LEFT JOIN query return now?
2. What is Meera's order_id now, and why?

This is a hypothetical change; setup.sql has not been modified. Record the prediction before checking output.

## Changed example 2 — assigned 15 October 2026

Start from changed example 1 (including order 104 for Meera). Imagine adding customer (4, Nila) but no order for her. Keep the same LEFT JOIN query.

Before changing or running anything, predict the output row count and Nila's order_id, explaining why. This additional customer has not been added to setup.sql.
