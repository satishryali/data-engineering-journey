-- Write your prediction and query here. No solution has been provided.
-- Predicted INNER JOIN row count:
-- Will Meera appear? Why?
-- Modified query:
-- Predicted Meera order_id and explanation:

-- First prediction submitted in chat, 15 October 2026 (no hint for this prediction):
-- "3 rows will appear, asha, asha, ravi"
-- "No meera will not appear because there is meera custoemr_id there in the orders table, means meera didn't order anything"
-- Tutor feedback: row count and names correct. Explanation interpreted as a typo:
-- there is NO matching customer_id = 3 in orders. Confirm through the next attempt.
-- Next learner attempt: change the query to preserve all customers;
-- predict Meera's order_id. Query not yet submitted; no solution provided.

-- Second attempt submitted in chat, 15 October 2026, without a hint:
SELECT c.name, o.order_id
FROM customers c
Left JOIN orders o
    ON c.customer_id = o.customer_id;

-- Learner explanation (preserved):
-- "meera order id is null becuase meera didn't ordered anything, so she wont be there in the orders table,"
-- Tutor feedback: correct preservation query and NULL explanation by inspection.
-- Expected row count is four; execution/output not yet supplied.
-- Next: reconstruct the query without looking, then a changed-input prediction.

-- Reconstruction submitted in chat, 15 October 2026 (preserve typo):
select c.name, o.order_id from customers c left join orders o on c.cusotmer_id = o.customer_id;
-- Learner: "my join preservers rows from left table which is customers."
-- Feedback: independent join logic and preserved-side explanation correct.
-- Column-name typo c.cusotmer_id would prevent execution; tutor pointed it out
-- and supplied the correct spelling c.customer_id. Corrected resubmission pending.

-- Corrected reconstruction submitted by learner, 15 October 2026:
select c.name, o.order_id from customers c left join orders o on c.customer_id = o.customer_id;
-- Correct by inspection; spelling correction was assisted. Execution not supplied.
-- Next: changed-input prediction from README.md; no answer given yet.

-- Changed example 1 prediction, 15 October 2026, independent (no hint):
-- "4 rows"
-- "meera order id : 104 because we found a match record with her customer id in orders table"
-- Feedback: correct count and match reasoning. Actual PostgreSQL output pending.
-- This file preserves multiple historical attempts, including a typo;
-- run only the latest corrected SELECT when verifying, not the entire file.

-- PostgreSQL output supplied by learner for changed example 1, 15 October 2026:
-- Asha   101
-- Asha   102
-- Ravi   103
-- Meera  104
-- Matches prediction and expected output. No tutor execution on server performed.
-- Next: changed example 2 prediction, adding customer (4, 'Nila') with no order.

-- Changed example 2 prediction, 15 October 2026, independent (no hint):
-- "5 rows with Nila,"
-- "Null"
-- Correct count and unmatched order_id. Requested explanation not yet supplied.
-- Next: explain why Nila remains despite having no matching order; then verify output.

-- Changed example 2 explanation submitted by learner, 15 October 2026:
-- "Becuase we are using left join it will include all the rows from teh left table and keep it null if they dont have any value in the right table"
-- Correct independent explanation of preservation. Tutor refined wording:
-- NULLs on the right occur when there is no matching row, rather than merely
-- an empty value in an existing row. Actual Nila output still pending.

-- Changed example 2 actual output supplied by learner, 15 October 2026:
-- Asha  101
-- Asha  102
-- Ravi  103
-- Meera 104
-- Nila  NULL
-- Matches independent prediction/explanation. Initial learning completed with
-- independent join reasoning and changed examples; reconstruction spelling help
-- remains recorded. Early retrieval due 16 October; not a claim of mastery.
