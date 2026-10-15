# Exercise 003: customer order totals and missing matches

Status: first prediction assigned 15 October 2026; no attempt yet. Revision item SQL-003.

New small synthetic dataset; earlier orders table has no amount column, so do not assume it does. For later execution, setup.sql creates separate temporary tables revenue_customers and revenue_orders in one PostgreSQL connection. Existing exercise tables remain intact.

Customers (customer_id, name): (1, Asha), (2, Ravi), (3, Meera), (4, Nila), (5, Asha).

Orders (order_id, customer_id, amount):
- (101, 1, 500)
- (102, 1, 200)
- (103, 2, 400)
- (104, 3, 150)
- (105, 1, 300)

First task: predict before execution. Imagine LEFT JOIN from customers to orders and GROUP BY customer ID/name, now using SUM(o.amount) instead of COUNT(o.order_id).

1. What total will customer 1 (Asha) get?
2. Will Nila's SUM(o.amount) return zero or NULL, and why?

Do not add a missing-total replacement or date/status filters yet. Wait for the learner's prediction before supplying hints or a solution.

## Current query task

Initial Nila-zero prediction was corrected with the SUM/NULL rule. Learner then correctly answered COUNT(amount)=0 and SUM(amount)=NULL for two NULL inputs (assisted application).

Write a query using revenue_customers and revenue_orders that returns customer_id, name and total order amount. Preserve every customer, including the two customers named Asha as separate rows. Leave missing totals as NULL for now. Do not add COALESCE, dates or status filters. Share the attempt before execution; setup.sql is available for later verification in the same connection.
