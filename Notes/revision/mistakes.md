# Mistake index (generated)

Source: `tracking/mistakes.json`. Do not edit this view.

| ID | Kind | Status | Distinct attempts | Observed behaviour | Follow-up |
| --- | --- | --- | ---: | --- | --- |
| M-SQL-001 | conceptual | practising | 1 | Unfinished CASE/COALESCE logic around actual-order counts. | Reconstruct actual-order counts unaided on a changed dataset. |
| M-SQL-002 | conceptual | practising | 1 | Joined customer_id to order_id during reconstruction. | Explain and choose matching keys on a changed schema before querying. |
| M-SQL-003 | conceptual | practising | 1 | Predicted two Asha groups when grouping only by name. | Predict duplicate-name outputs and explain grouping grain without a hint. |
| M-SQL-004 | conceptual | practising | 1 | Predicted zero for Nila SUM with no non-NULL input. | Delayed COUNT/SUM prediction on unmatched and all-NULL inputs. |
| M-SQL-005 | debugging_approach | open | 1 | Malformed VALUES-derived INSERT into an older exercise table. | Run the supplied exercise setup in one connection and report its result before totals query. |
| M-PY-001 | conceptual | practising | 2 | Treated items() field-name/value pairs as whole records and compared mismatched types. | Complete the saved one-record refresher, then reconstruct on a changed record. |
| M-PY-002 | debugging_approach | practising | 1 | Repeated assignment to one dictionary key overwrote rejected records. | After foundations, trace two rejected records and verify both remain. |
| M-PY-003 | debugging_approach | open | 1 | Later draft assigns an amount into input order_id and calls value() on the result. | Review actual output/type after the currently selected dictionary prerequisite. |
