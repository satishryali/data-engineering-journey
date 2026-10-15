-- Prediction for Nila's COUNT(*) result:
-- Reason:
-- No attempt or solution yet. Preserve predictions before execution.

-- First prediction submitted 15 October 2026, independent (no hint):
-- "asha 2"
-- "ravi 1"
-- "meera 1"
-- "Nila 1,"
-- "count(*) count the no of rows which are related to the existing cusotmer"
-- Tutor feedback: all counts correct. COUNT(*) counts joined rows per group,
-- including Nila's single preserved row with NULL order_id, not actual orders.
-- Next: learner modifies the counting expression to count actual orders,
-- returning zero for Nila while keeping every customer. No solution given.

-- Actual-order-count attempt, learner submitted 15 October 2026 (unfinished):
select c.name,case when (coalesce(o.order_id, 0) > 0 then count(o.order_id) else COALESCE(o.order_id,0) from customers c left join orders o on c.customer_id = o.customer_id and o.order_id is not null group by c.name;
-- Learner: "i have tried but not able to complete"
-- Tutor hint: COUNT(column) ignores NULL; COUNT(*) counts joined rows.
-- Learner already included COUNT(o.order_id), which is the needed expression.
-- Remove CASE, COALESCE and the extra ON filter for this task. CASE syntax is
-- incomplete, but repairing it is unnecessary here. No full corrected query given.
-- Next: learner rewrites the query simply and predicts all four counts.

-- Revised query submitted 15 October 2026 after COUNT/NULL hint:
select c.name,count(o.order_id) from customers c left join orders o on c.customer_id = o.customer_id and o.order_id is not null group by c.customer_id,c.name;
-- Learner: "DONE"
-- Correct by inspection; assisted because tutor explained counting expression.
-- Remaining right-side non-NULL ON condition is redundant for this primary-key
-- order_id but harmless here. It does not remove unmatched customers.
-- Actual output and learner's explanation for Nila's count pending.

-- Learner supplied actual output, 15 October 2026:
-- name,count
-- Meera,1
-- Nila,0
-- Asha,2
-- Ravi,1
-- Explanation: "as we are reading the whole row in previuosly like count(*) but we are specifally counting the count(o.order_id) that is the reason"
-- Correct output and distinction. Tutor made non-NULL behaviour explicit;
-- no ORDER BY means this returned row order is valid. Implementation remains
-- assisted due to earlier hint. Next: hide earlier queries and reconstruct
-- simply without CASE/COALESCE or the redundant ON filter, explaining Nila's zero.

-- Reconstruction submitted 15 October 2026 (wrong join key preserved):
select c.name,count(o.order_id) from customers c left join orders o on c.customer_id = o.order_id group by c.customer_id,c.name;
-- Learner explanation: "nila gets 0 because we are only counting the no of order id assoicated to nila since there are no order id's we will get zero"
-- Counting explanation correct. Tutor identified customer-ID/order-ID mismatch:
-- sample IDs 1-4 versus 101-104 would yield no matches and all zero counts.
-- No execution output supplied for this incorrect reconstruction.

-- Learner corrected after join-key feedback:
select c.name,count(o.order_id) from customers c left join orders o on c.customer_id = o.customer_id group by c.customer_id,c.name;
-- Correct by inspection; reconstruction assisted on join key.
-- Next: hypothetical order (105, 1); predict Asha and Nila order counts and why.

-- Changed-example prediction, 15 October 2026, independent (no new hint):
-- "ahsa 3 and nila 0 , since asha is already having two orders, adding this new order results in 3 orders for asha and 0 for nila( we are not adding anythign)"
-- Correct counts/reason. Next: insert (105, 1) once in existing connection,
-- rerun latest corrected query and share actual output/error.

-- Changed-example output supplied by learner, 15 October 2026:
-- Meera 1
-- Nila  0
-- Asha  3
-- Ravi  1
-- Matches independent prediction. Earlier implementation/reconstruction hints
-- remain recorded. Next: hypothetical customer (5, 'Asha') with no orders;
-- predict whether grouping only by c.name gives one Asha row or two and why.

-- Grouping check, learner's initial prediction (15 October 2026):
-- "it will return two because this is hte new asha row which we are inserting now and there are no duplicate checks or primary keys in the table, this we are treating as new line"
-- Incorrect: confuses separate stored rows with output groups. Setup has
-- customer_id PRIMARY KEY; new ID 5 is distinct and names are not unique.
-- Tutor hint: GROUP BY c.name uses the name as its grouping key, and both
-- customers have the same key Asha. Ask learner to reconsider group count
-- and order count. No full query/output solution supplied; no row inserted yet.

-- Learner correction after grouping-key hint, 15 October 2026:
-- "if we use the c.name in the group by we are having 1, c.customer_id,c.name then 2,"
-- "3 as usal in the first scneario and 3, 0 in the second scenario"
-- Correct: one Asha group/count 3 by name; two groups/counts 3 and 0 by ID/name.
-- Grouping explanation assisted after earlier incorrect prediction; not
-- independent mastery. Next: insert customer (5, 'Asha') once and compare
-- actual output of name-only versus ID/name grouping. Include customer_id
-- in the ID/name version's SELECT to distinguish the two Asha customers.

-- Duplicate-name queries/output supplied by learner, 15 October 2026:
select c.name,count(o.order_id) from customers c left join orders o on c.customer_id = o.customer_id group by c.name;
-- Asha 3; Ravi 1; Nila 0; Meera 1
select c.name,count(o.order_id) from customers c left join orders o on c.customer_id = o.customer_id group by c.customer_id,c.name;
-- Meera 1; Nila 0; Asha 3; Asha 0; Ravi 1
-- Both correct. Learner omitted requested customer_id in SELECT but group
-- identity is correct; tutor noted adding ID makes duplicate names distinguishable.
-- Initial practice completed with COUNT/NULL, join-key and grouping hints.
-- Early unaided reconstruction due 16 October; independent mastery not recorded.
