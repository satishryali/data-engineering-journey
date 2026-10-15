# Python 001: dictionary records and cleaning baseline

Assigned 15 October 2026; no attempt yet. Revision item PY-001.

## Active task — clean five order records

The initial printing/type prediction below was assigned but not attempted. Learner requested less fragmented practice; use this bounded practical task instead. No Python proficiency assumed. Attempt it as a whole; hints and solutions stay separate.

```python
orders = [
    {"order_id": 101, "amount": "500"},
    {"order_id": 102, "amount": "200"},
    {"order_id": 103, "amount": "bad"},
    {"order_id": 104, "amount": ""},
    {"order_id": 105, "amount": " 300 "},
]
```

Write clean_orders(orders), returning two lists: valid_orders and rejected_orders.

- Valid amounts must become integers; surrounding spaces are allowed.
- A bad or blank amount must be rejected without stopping processing of later records.
- Valid records retain order_id and the converted amount. Rejected records retain order_id, original amount and a short reason.
- Leave the original input records unchanged.

In one submission: briefly predict which IDs will be accepted/rejected, provide your attempted function, run it and share both returned lists (or the exact error). Documentation for syntax is allowed; say if you consult a complete solution. Do not reveal the implementation before the attempt. Review function logic, output, help used and reasoning, then choose one changed example based on evidence.

## Earlier prompt — unattempted, replaced

Start with one small prediction. Do not run before predicting.

```python
orders = [
    {"order_id": 101, "amount": "500"},
    {"order_id": 102, "amount": "200"},
    {"order_id": 103, "amount": "bad"},
]

for order in orders:
    print(order["amount"])
```

1. What will this print?
2. Are the amount values strings or integers?

Wait for the prediction before assigning code changes. Later steps will introduce numeric conversion and validation, then extend the sample; they are not assigned or completed yet. Preserve attempts in attempt.py, with tutor hints/solutions separate. No familiarity or proficiency assumed from experience or SQL progress.
