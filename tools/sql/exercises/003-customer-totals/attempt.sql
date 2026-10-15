-- Prediction for customer 1 SUM(amount):
-- Prediction for Nila SUM(amount) and why:
-- No attempt or solution supplied yet.

-- First prediction, learner submitted 15 October 2026 without hints:
-- "1000"
-- "0 for nila"
-- "because we are adding amounts to asha as she has some orders but nila dont have any"
-- Asha total correct; Nila SUM prediction incorrect. Tutor explained PostgreSQL
-- SUM returns NULL when no non-NULL inputs exist, unlike COUNT(column)'s zero.
-- Next small check: predict COUNT(amount) and SUM(amount) for two NULL inputs.
-- No missing-total replacement expression or full query provided.

-- Smaller NULL comparison after tutor rule explanation, 15 October 2026:
-- Learner: "(0), null"
-- Correct: COUNT(amount)=0; SUM(amount)=NULL for two NULL inputs.
-- Assisted immediate application; no independent mastery inferred.
-- Next: write grouped customer total query using revenue_customers and
-- revenue_orders; include customer ID/name and preserve unmatched customers.
-- Leave missing SUM totals NULL; no COALESCE solution provided yet.

-- Insertion failure supplied by learner, 15 October 2026 (preserved):
insert into orders(amount) select val from (values(500),(200),(300) where not exists (select 1 from orders where customer_id = 1));
-- PostgreSQL error: syntax error at or near "where"
-- LINE 1: ...(amount) select val from (values(500),(200),(300) where not ...
-- Elapsed reported by client: 00:00:00.001 (not a study interval).
-- Diagnosis: VALUES-derived table needs closing parenthesis and alias/column
-- name before outer WHERE. But this targets old orders, which has no amount
-- in our setup; INSERT would add orders rather than attach amounts to existing
-- records and omits required IDs. Do not run a syntax-only fix on old tables.
-- Next: run exercise 003 setup.sql, which creates/inserts separate revenue_*
-- tables with amounts and IDs; share setup result/error before SUM query.
