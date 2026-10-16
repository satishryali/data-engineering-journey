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

## Import names must match

Use either `import csv` with `csv.DictReader(file)`, or `from csv import DictReader` with `DictReader(file)`.

Mixing these forms can depend on an old notebook import. Our practice needed this correction; see the checkpoint's saved CSV review for the actual attempt.

## Pass records to the cleaner

```python
valid_result, rejected_result = clean_orders(data)
```

The function must already be defined. Saved learner output on 16 October 2026 shows valid IDs `501`, `503`, `505` with integer amounts `250`, `600`, `0`; rejected IDs `502`, `504` keep their original amounts and reasons. IDs stay strings because this cleaner only converts amounts.

This read-and-clean exercise was completed with guidance. Writing the result files is the next task; it has not been demonstrated yet.
