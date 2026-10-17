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
Reference: [Python CSV documentation](https://docs.python.org/3/library/csv.html).
