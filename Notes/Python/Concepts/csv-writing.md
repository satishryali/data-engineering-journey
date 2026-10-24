# Write CSV files

Use a CSV writer to save rows from Python into a file. It handles commas and quotes inside values for us.

## Write lists as rows

This small employee example follows the notebook. Run it in a scratch folder: mode `"w"` creates a file or replaces its existing contents.

```python
import csv

with open("employees_example.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "name", "salary"])
    writer.writerow([1, "Satish", 50000])
    writer.writerows([[2, "Ravi", 60000], [3, "Priya", 55000]])

with open("employees_example.csv", "r", newline="", encoding="utf-8") as file:
    print(file.read(), end="")
```

Expected output:

```csv
id,name,salary
1,Satish,50000
2,Ravi,60000
3,Priya,55000
```

- `writerow()` writes one row. Pass a list of values.
- `writerows()` writes several rows. Pass a collection of rows.
- `csv.writer` does not add a header automatically. The first `writerow()` above writes it.
- Read the saved file after the writing block ends, so the writer's file has been closed.

## Write dictionaries as rows

Use `DictWriter` when each record already has field names.

```python
import csv

fields = ["id", "name", "salary"]
with open("employee_dict_example.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerow({"salary": 60000, "name": "Ravi", "id": 2})

with open("employee_dict_example.csv", "r", newline="", encoding="utf-8") as file:
    print(list(csv.DictReader(file)))
```

Expected output:

```text
[{'id': '2', 'name': 'Ravi', 'salary': '60000'}]
```

- `fieldnames` sets the column order, even if the dictionary uses a different order.
- `writeheader()` writes the field names as the first row.
- The default reader returns strings. Writing an integer does not preserve its Python type in CSV.

## Open two files in one with statement

When copying CSV rows, we need the input and output files open together. Put a comma between the two context managers. A context manager handles setup and cleanup; for these files, it closes them when the block ends, including if an error occurs.

Create `input.csv` in a scratch folder with this small input:

```csv
id,name,salary
2,Ravi,60000
3,Priya,55000
```

Run this code from that folder. Use different input and output paths: `"w"` replaces an existing output file's contents.

```python
import csv

with (
    open("input.csv", "r", newline="", encoding="utf-8") as source,
    open("output.csv", "w", newline="", encoding="utf-8") as destination,
):
    reader = csv.DictReader(source)
    writer = csv.DictWriter(destination, fieldnames=reader.fieldnames)
    writer.writeheader()
    for row in reader:
        writer.writerow(row)
```

Expected contents of `output.csv` after the block ends:

```csv
id,name,salary
2,Ravi,60000
3,Priya,55000
```

- `source` reads the existing file; `destination` writes the copied rows.
- Both files stay open inside the block. The input must have a header for this example.
- `reader.fieldnames` supplies the input column names to the writer.
- Parentheses let us spread the statement over several lines (Python 3.9+).
- Files open from left to right and close in reverse order: destination, then source.

For the earlier example that writes a file and then reads that same file, keep the two `with` blocks separate. The first block finishes writing and closes the file before the second reads it. Opening that same path in `"w"` while reading it would erase its existing contents.

Added 24 October 2026 from the learner's question about two context managers. Tutor explanation; no independent attempt assessed. Recall task is in [Notebook recall questions](../../revision/notebook-questions.md).

## Why newline matters

Use `newline=""` when opening a file for the CSV module. This lets the CSV module handle line endings.

The notebook's files give a real comparison:

| File | Bytes between rows | What was observed |
| --- | --- | --- |
| `employees.csv` | `\r\r\n` | Extra carriage return from writing without `newline=""` on Windows |
| `employees_w_n.csv` | `\r\n` | Normal CSV row ending with `newline=""` |

`\r` means carriage return and `\n` means line feed. Extra row endings can appear as blank lines when another program reads the file. `newline=""` does not remove CSV row endings.

## Notebook evidence

Source: [csv-module.ipynb](../../../practice/Modules/csv-module.ipynb), cells 27-37 (zero-based).
The employee files and `product_data_dict.csv` contain saved rows. `product_data.csv` is currently empty, although cell 36 contains executed-looking writer code. That cell alone does not verify the current file contents.

These examples explain the studied syntax; they do not complete the deferred valid/rejected-orders task or RDS-001. Help used during the notebook work is unknown.

Related: [CSV reading](csv-reading.md), [file methods](file-methods.md).
For grouping and running totals, see [Count orders and write the summary after the loop](../Logic/order-summary-after-loop.md).
Reference: [Python CSV documentation](https://docs.python.org/3/library/csv.html).
