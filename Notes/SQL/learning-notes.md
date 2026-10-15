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
