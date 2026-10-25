# Collect function results and write once

We want one fresh CSV containing the results for several input files. Count each file separately, keep its final result, then write the collected results once.

## Why only the last result remained

Opening a file with `"w"` clears its old contents. Earlier code opened the same summary file in each `load()` call and wrote only that call's result:

```text
First call:  erase the page, write the first result
Second call: erase the page, write the second result
Third call:  erase the page, write the third result
```

Also, `results = []` inside a function creates a fresh empty list each time that line runs. It does not automatically contain earlier calls' results.

## Keep one dictionary per input file

Finish counting one input before building its result dictionary. Building it inside the order loop collects intermediate counts for that file.

Use a list to keep separate results:

```python
results = []
results.append({"input": "first.csv", "completed": 3})
results.append({"input": "second.csv", "completed": 2})
print(results)
```

Expected output:

```text
[{'input': 'first.csv', 'completed': 3}, {'input': 'second.csv', 'completed': 2}]
```

Repeated `update()` calls on one dictionary would replace the matching `input` and `completed` values. They would not preserve two rows. See [Dictionary updates](../Concepts/dictionaries.md#same-key-replaces-its-value).

## Return one result and collect it outside

`return` sends a value back to the caller. `print()` displays a value. Writing a CSV saves it to a file. These are three separate actions.

This small example uses two lists of status values so we can focus on the function calls. It is a tutor example, not a replacement for the learner's CSV-report function.

```python
import csv
from io import StringIO

def count_orders(filename, statuses):
    completed = 0
    cancelled = 0
    pending = 0
    for status in statuses:
        if status == "completed":
            completed += 1
        elif status == "cancelled":
            cancelled += 1
        elif status == "pending":
            pending += 1
    return {"input": filename, "completed": completed,
            "cancelled": cancelled, "pending": pending}

results = []
first = count_orders("first.csv", ["completed", "cancelled"])
second = count_orders("second.csv", ["pending", "completed", "completed"])
print(first)
print(second)
results.append(first)
results.append(second)

output = StringIO()
writer = csv.DictWriter(output,
                        fieldnames=["input", "completed", "cancelled", "pending"])
writer.writeheader()
writer.writerows(results)
print(output.getvalue(), end="")
```

Expected output:

```text
{'input': 'first.csv', 'completed': 1, 'cancelled': 1, 'pending': 0}
{'input': 'second.csv', 'completed': 2, 'cancelled': 0, 'pending': 1}
input,completed,cancelled,pending
first.csv,1,1,0
second.csv,2,0,1
```

- Each call starts fresh counters. The second dictionary contains only the second input's counts.
- The caller keeps both dictionaries in one list. The counting function does not use that list or any global variables.
- `StringIO` holds text in memory. For a real combined report, open the destination in `"w"` once, after collecting results, and write the header and rows inside its `with` block.
- `DictWriter.writerow()` takes one dictionary. `writerows()` takes a collection of dictionaries, not lists of field values.
- The original three reports can still be generated inside the per-file function before it returns. The combined report collects its returned counts separately.

## All writing can be inside a function

A batch means a group of input files processed together. If all writing should happen inside functions, use this arrangement:

```text
process_files(filenames):
    create one empty results list
    for each filename:
        call load(filename)
        append its returned dictionary
    open the combined report once
    write the header and all collected dictionaries
```

`load()` handles one input. `process_files()` handles the collection of inputs. The results list belongs to the batch; the counters belong to each input. The list can be local to `process_files()`, so this does not require a global list.

## Append versus a fresh report

`"a"` adds new rows to the end of an existing file, including rows from earlier runs. It does not remove duplicate results. A header should only be written if the file is empty; `file.tell() == 0` checks that position when opened in append mode.

`"w"` gives a fresh report. It is suitable when we have collected all the rows we want to save and write them together once. Use the approach that matches whether the output is a history or the current batch's report.

## Evidence and next attempt

Saved 25 October 2026 from the learner's questions about lost rows, repeated appending and function-local lists. The learner requested a simple explanation of the logic rather than a mode-switch workaround. Earlier examples and fixes were tutor-supplied; independent reconstruction remains unverified.

The latest supplied code puts `results = []` outside `load()` and uses `results.append(result)` inside it, then rewrites the full list with `writerows(results)`. This can retain all three results when run from the list initialisation through all calls. It rewrites the growing list three times. If only the calls are repeated without resetting the list, earlier results remain in memory.

That version relies on a global list and has no `return result` or outside print, so it does not yet meet the original function-return task. The attached output snapshot is empty; no execution success or acceptance is inferred. Its `pending_total += 1` counts pending rows, not their monetary amount; that variable is not currently written to the reports.

Next task: keep the original three reports, return a fresh counts dictionary from each call, print it outside, and collect the results for one combined write. Expected counts from the task are `3/2/0`, `2/1/0`, `1/1/1` for the three inputs respectively; these are acceptance targets, not verified output. See [Recall questions](../../revision/notebook-questions.md) for separate practice.
