# Python 001 — first reviewed block, 15 October 2026

Keep this feedback separate from attempt.py. No full solution provided.

## Evidence and help

The reviewed draft used result dictionaries, an outer loop over orders and an inner `for order_id, amount in i.items()` loop. It compared `order_id > 0`, assigned repeatedly to the same dictionary key and caught every Exception. Tutor ran the then-current file without editing it; observed valid_orders={} and invalid_orders={'order_id': ' 300 '}.

Tutor explained three issues:

1. items() yields key/value pairs. Here order_id is a field-name string, not the numeric order ID. Use a single record loop and retrieve fields by key.
2. Assigning the same dictionary key overwrites previous records. Use lists to accumulate valid/rejected records.
3. Convert amount using int(), handle ValueError and avoid broad exceptions hiding unrelated bugs.

## Latest draft at pause

Learner added valid_list/invalid_list but retained the inner items loop, now comparing amount > 0. The draft also uses `res = valid_orders['order_id'] = amount` followed by `res.items()`, catches Exception and prints valid_orders inside the loop. Snapshot preserved in attempts/002-pause-draft.py; active attempt.py left unchanged.

This latest draft has not been run/reviewed with learner yet; do not claim a successful cleaner. No function/returned valid/rejected outputs or rejection reasons demonstrated. Latest status needs_guidance; early practice due 16 October, no success anchor.

## Next on resume

Review the learner's current draft, obtain actual output/error and help with record versus key/value iteration and conversion before evaluating the whole cleaner. Keep assistance targeted; use a small worked example only if needed, then have learner reconstruct. Do not overwrite attempt.py or return to unrelated trivial quizzes. Preserve the complete practical-task goal from README.md and batch the next records at task/pause/handoff.
