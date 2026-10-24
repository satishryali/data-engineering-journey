# Read a CSV file

Real order records can arrive in files. Read them into dictionaries so the same cleaner can process them.

## Read rows with DictReader

Our practice file has these contents:

```csv
order_id,amount
501,250
502,bad
503,600
504,
505,0
```

Run this from the folder containing `orders.csv`:

```python
import csv

data = []
with open("orders.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        data.append(row)

print(data[0])
print(data[3])
```

Expected output:

```text
{'order_id': '501', 'amount': '250'}
{'order_id': '504', 'amount': ''}
```

- The header supplies the dictionary keys.
- Values are strings, including `order_id`. An empty CSV field becomes `""` here.
- `with open(...)` opens the file and closes it when its block ends.
- `"r"` means read. `encoding="utf-8"` tells Python how to read text characters.
- `newline=""` lets the CSV reader handle line endings.
- A relative path is resolved from the current working folder. If the file is elsewhere, supply the correct relative path. The learner's original notebook uses an absolute Windows path; that path needs changing on another computer.

## Keep all CSV rows

We need a list of dictionaries to keep several orders. Each dictionary holds one row; the list holds all the rows.

The learner's [completed orders CSV](../../../practice/Python%20Oops/Oops/completed_orders_v1.csv) currently contains three data rows:

```csv
order_id,customer_id,quantity,unit_price,total_amount
1001,C001,2,250,500
1003,C003,3,100,300
1004,C001,1,450,450
```

Run from the repository root:

```python
import csv

orders = []
with open("practice/Python Oops/Oops/completed_orders_v1.csv",
          "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        orders.append(row)

print(len(orders))
print(orders[0])
print([row["order_id"] for row in orders])
```

Expected output:

```text
3
{'order_id': '1001', 'customer_id': 'C001', 'quantity': '2', 'unit_price': '250', 'total_amount': '500'}
['1001', '1003', '1004']
```

- `orders = []` is outside the loop so we keep earlier rows.
- `DictReader` uses the first row as column names. It returns a new dictionary for each data row.
- `orders.append(row)` adds that whole dictionary as one list item.
- All three dictionaries have an `order_id` key. Their values stay separate because they belong to different dictionaries.
- The file has three data rows, not five. With five data rows, the same code collects five dictionaries. The header does not count.
- Values stay strings. Collecting rows does not convert amounts to numbers.

Using `orders = {}` and `orders.update(row)` repeatedly would leave one dictionary with the last row's field values for this file. Use `append()` on a list to keep all rows. See [Same key replaces its value](dictionaries.md#same-key-replaces-its-value).

Added 24 October 2026 from the learner's question about keeping five CSV rows. File contents inspected; collection code supplied by the tutor, with no learner execution or independent understanding assessed. Recall task is separate in [Notebook recall questions](../../revision/notebook-questions.md).

## Import names must match

Use either `import csv` with `csv.DictReader(file)`, or `from csv import DictReader` with `DictReader(file)`.

Mixing these forms can depend on an old notebook import. Our practice needed this correction; see the checkpoint's saved CSV review for the actual attempt.

## Pass records to the cleaner

```python
valid_result, rejected_result = clean_orders(data)
```

The function must already be defined. Saved learner output on 16 October 2026 shows valid IDs `501`, `503`, `505` with integer amounts `250`, `600`, `0`; rejected IDs `502`, `504` keep their original amounts and reasons. IDs stay strings because this cleaner only converts amounts.

This read-and-clean exercise was completed with guidance. The specific valid/rejected-orders writing and read-back task remains pending. Later general CSV writing practice is recorded in [CSV writing](csv-writing.md).

## A comma inside a value

The new notebook compared splitting text with using a CSV reader. This row has three fields; the comma inside the quoted name belongs to the name.

```python
import csv

line = '102,"Priya, Reddy",Bangalore'
print(line.split(","))
print(next(csv.reader([line])))
```

Expected output:

```text
['102', '"Priya', ' Reddy"', 'Bangalore']
['102', 'Priya, Reddy', 'Bangalore']
```

`split(",")` cuts at every comma. `csv.reader` understands the quotes and keeps the name together. The notebook's `data_incor.csv` is valid quoted CSV despite its filename.

## Reader versus DictReader

```python
import csv

lines = ["id,name,salary", "1,Ravi,60000"]
print(list(csv.reader(lines)))
print(list(csv.DictReader(lines)))
```

Expected output:

```text
[['id', 'name', 'salary'], ['1', 'Ravi', '60000']]
[{'id': '1', 'name': 'Ravi', 'salary': '60000'}]
```

- `reader` returns each row as a list, including the header.
- With no supplied field names, `DictReader` uses the first row as keys and returns the data rows as dictionaries.
- Under these defaults, values remain strings. For example, the employee notebook's `is_active` value is the string `'False'`, not the boolean `False`.

Source: [csv-module.ipynb](../../../practice/Modules/csv-module.ipynb), cells 9-13, 26 and 34-35. Its saved outputs show both formats. Assistance and independent understanding have not been assessed from these files.
Reference: [Python CSV documentation](https://docs.python.org/3/library/csv.html).
