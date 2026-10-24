# Count orders and write the summary after the loop

We want one final summary row for each status. This is processing logic: decide which group an order belongs to, keep running totals, and write the result after all orders have been counted.

## Groups come from the status values

The CSV does not need a column named `group`. Orders with the same `status` belong to the same group.

Small input:

```csv
status,quantity,unit_price
completed,2,100
cancelled,1,50
completed,3,100
```

There are two completed orders and one cancelled order. For each order, its amount is `quantity * unit_price`.

## Count first, write after the loop

This complete example uses the small input above. It keeps the example in memory so we can focus on the logic without creating files.

```python
import csv
from io import StringIO

source = StringIO("status,quantity,unit_price\n"
                  "completed,2,100\n"
                  "cancelled,1,50\n"
                  "completed,3,100\n")
orders = list(csv.DictReader(source))

completed_count = 0
completed_total = 0
cancelled_count = 0
cancelled_total = 0

for order in orders:
    amount = int(order["quantity"]) * int(order["unit_price"])
    if order["status"] == "completed":
        completed_count += 1
        completed_total += amount
    elif order["status"] == "cancelled":
        cancelled_count += 1
        cancelled_total += amount

destination = StringIO()
writer = csv.DictWriter(destination,
                        fieldnames=["status", "order_count", "total_amount"])
writer.writeheader()
writer.writerow({"status": "completed",
                 "order_count": completed_count,
                 "total_amount": completed_total})
writer.writerow({"status": "cancelled",
                 "order_count": cancelled_count,
                 "total_amount": cancelled_total})
print(destination.getvalue(), end="")
```

Expected output:

```csv
status,order_count,total_amount
completed,2,500
cancelled,1,50
```

- `StringIO` behaves like a text file kept in memory. Real file reading/writing is covered in [CSV reading](../Concepts/csv-reading.md) and [CSV writing](../Concepts/csv-writing.md).
- Set the counters to zero before the loop. Setting them to zero inside the loop would lose earlier totals.
- `+=` adds to the previous value: `completed_count += 1` means `completed_count = completed_count + 1`.
- One order row adds `1` to its order count. Adding quantities counts items instead: the completed orders contain five items, but only two orders.
- The two `writerow()` calls run after the loop finishes. In your file-writing code, they must still be inside the output files' `with` block so the file stays open.
- This example handles `completed` and `cancelled`. Other status values do not enter either branch.

## Trace the running totals

| Step | Completed count | Completed total | Cancelled count | Cancelled total |
| --- | ---: | ---: | ---: | ---: |
| Before the loop | 0 | 0 | 0 | 0 |
| First row: completed, amount 200 | 1 | 200 | 0 | 0 |
| Second row: cancelled, amount 50 | 1 | 200 | 1 | 50 |
| Third row: completed, amount 300 | 2 | 500 | 1 | 50 |

Only after the third row do we have the final totals. Writing the completed summary inside its `if` branch would save intermediate rows: first `completed,1,200`, then `completed,2,500`.

The indentation controls when the writing happens:

```text
inside the output files' with block:
    for each order:
        update the matching count and total
    write the completed summary
    write the cancelled summary
```

Use fixed status text such as `"completed"` when writing a final group row. The loop variable describes only the last order visited.

## Keep separate orders before summarising

Use a list of row dictionaries and `append(row)` to keep all orders. Repeated `update(row)` calls on one dictionary overwrite earlier values; looping over that dictionary visits keys, not order rows.

See [Keep all CSV rows](../Concepts/csv-reading.md#keep-all-csv-rows) for the collection example. A list named `completed_orders` still contains all statuses if every input row was appended without filtering.

## Learning context

Added 24 October 2026 from the learner's summary questions and reviewed snapshots. Earlier attempts wrote running summaries inside the loop; one attempt used a single dictionary and was later reverted to a list. The tutor supplied the final counting-and-writing pattern after explanations did not resolve the difficulty. This is assisted explanation, not independently demonstrated understanding or delayed retention.

The latest supplied snapshot reads the two output files. Its saved output shows completed order amounts `500`, `300`, `450` and cancelled amounts `800`, `1200`. Those imply an expected summary of `completed,3,1250` and `cancelled,2,2000`, assuming each row is one order. No summary output or revised summary implementation was supplied, so the final summary is still unverified.

Next practice: reconstruct the summary on changed input and show the output, stating any help used. Keep recall prompts separate in [Notebook recall questions](../../revision/notebook-questions.md).
