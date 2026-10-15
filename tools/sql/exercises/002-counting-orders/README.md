# Exercise 002: count orders per customer

Status: initial practice completed 15 October 2026 with assistance on COUNT/NULL behaviour, join keys and grouping grain. Correct outputs supplied, including duplicate-name comparison. Early unaided reconstruction due 16 October. Revision item SQL-002; independent mastery not recorded. See attempt.sql for evidence.

Continue with the same PostgreSQL temporary tables from exercise 001, now including Meera's order 104 and Nila with no orders. If a fresh connection is needed, use this folder's setup.sql once.

Customers: (1, Asha), (2, Ravi), (3, Meera), (4, Nila).
Orders (order_id, customer_id): (101, 1), (102, 1), (103, 2), (104, 3).

Goal: eventually return one row per customer with their number of orders, including zero when no order matches. Start with a prediction about this candidate query; do not run it first:

```sql
SELECT c.name, COUNT(*) AS order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;
```

What number will this query return for Nila: 0 or 1? Explain what is being counted. Wait for feedback before modifying the query. Hints and solution have not been supplied.

Prediction received: Asha 2, Ravi 1, Meera 1, Nila 1, all correct. Tutor clarified that COUNT(*) counts the joined rows in each group, including a preserved unmatched row.

Next task: change only the counting expression so the query counts actual orders, returning zero for Nila and keeping every customer. Predict the four counts. No replacement expression or hint has been provided yet.

## Current step — changed example

The learner implemented and ran correct order counts after a COUNT/NULL hint, then reconstructed with a wrong join key and corrected it after feedback. Attempts and output are preserved in attempt.sql.

Keep the current four customers and four orders. Imagine adding order (105, 1), another order for Asha. Using the latest corrected query, predict Asha's and Nila's order counts and explain why. Do not change/run the data before predicting. No hint or answer provided for this variation.

Learner independently predicted Asha 3 and Nila 0 with correct reasoning. Current next step: insert order (105, 1) once in the same connection, rerun the latest corrected query and share actual output/error. Skip the insert if already performed; do not rerun setup over the current temporary tables.

Changed output received and correct: Meera 1, Nila 0, Asha 3, Ravi 1.

## Grouping check — assigned 15 October 2026

Imagine a different customer (5, Asha) with no orders, alongside the existing customer (1, Asha). Do not add this row yet. If the counting query groups only by c.name instead of customer ID and name, will it return one Asha row or two? Explain. No answer or hint supplied yet.

After a grouping-key hint, learner correctly predicted one Asha group/count 3 with name-only grouping and two Asha groups/counts 3 and 0 with ID/name grouping. Current task: insert (5, 'Asha') once in the existing connection and compare actual output of both versions. Add c.customer_id to SELECT in the ID/name version so the two customers are distinguishable. Skip insertion if already performed. Preserve attempts and outputs; setup.sql remains the original four-customer baseline.
