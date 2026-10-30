# JSON

JSON is a text format used to share data between programs. An API can send JSON to Python, Java or another language. Each program reads the text into its own data structures.

Python's `json` module is included with Python. Import it with `import json`.

## JSON and dictionaries

A Python dictionary is an object in a running Python program. JSON is text that can be kept in memory, saved in a file or sent over a network.

```json
{
  "customer_id": 101,
  "name": "Anu",
  "active": true,
  "phone": null,
  "orders": [{"order_id": 1, "amount": 250}]
}
```

- `{}` holds a JSON object: names paired with values.
- `[]` holds an array: a list of values.
- Names and text use double quotes. No trailing comma after the last entry.
- Python uses `True`, `False` and `None`; JSON uses `true`, `false` and `null`.
- Other languages have structures similar to dictionaries, such as maps.
- The JSON library converts the format. Your code still checks the expected fields and values.

| JSON value | Default Python result |
| --- | --- |
| Object `{...}` | `dict` |
| Array `[...]` | `list` |
| String | `str` |
| Integer number | `int` |
| Decimal number | `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

Loading JSON does not always give a dictionary. The result depends on the JSON value.

## Four main functions

| Function | Input | Result |
| --- | --- | --- |
| `loads(text)` | JSON string | Python object |
| `dumps(data)` | Python object | JSON string |
| `load(file)` | Open file containing JSON | Python object |
| `dump(data, file)` | Python object and open output file | Writes JSON to the file |

The `s` helps us remember **string**. `dump()` writes to a file; its return value is `None`.

## loads - read a string

Read a customer and total the nested orders.

```python
import json

text = """{
  "name": "Anu",
  "orders": [
    {"order_id": 1, "amount": 250},
    {"order_id": 2, "amount": 400}
  ]
}"""
data = json.loads(text)
print(type(data))
print(type(data["orders"]))
print(data["name"])
total_amount = 0
for order in data["orders"]:
    print(order["order_id"], order["amount"])
    total_amount += order["amount"]
print(total_amount)
```

Expected output:

```text
<class 'dict'>
<class 'list'>
Anu
1 250
2 400
650
```

`data["orders"]` selects the list. Each loop item is one dictionary. Reset the total before the loop so a notebook rerun does not keep adding to an old total.

## dumps - create a string

Create readable JSON text with sorted keys and readable Tamil characters.

```python
import json

customer = {"name": "அனு", "customer_id": 101, "active": True}
text = json.dumps(customer, indent=2, sort_keys=True, ensure_ascii=False)
print(text)
print(type(text))
```

Expected output:

```text
{
  "active": true,
  "customer_id": 101,
  "name": "அனு"
}
<class 'str'>
```

| Option | What it changes |
| --- | --- |
| `indent=2` | Adds line breaks and two spaces for each level |
| `sort_keys=True` | Sorts object keys when writing |
| `ensure_ascii=False` | Keeps characters such as Tamil readable rather than using Unicode escapes |
| `allow_nan=False` | Rejects `NaN` and infinity with `ValueError`; standard JSON does not support these numbers |

These options work with both `dump()` and `dumps()`. Unicode escapes from the default `ensure_ascii=True` still preserve the text; they are another way to write it.

## dump and load - save and read a file

Run this in a practice folder. Mode `"w"` creates the output or replaces its contents.

```python
import json

customer = {"name": "Anu", "balance": 250.75}
with open("customer_example.json", "w", encoding="utf-8") as file:
    json.dump(customer, file, indent=2, allow_nan=False)

with open("customer_example.json", "r", encoding="utf-8") as file:
    loaded_customer = json.load(file)

print(loaded_customer["name"])
print(loaded_customer["balance"])
```

Expected output:

```text
Anu
250.75
```

- `encoding="utf-8"` belongs to `open()`, not `json.dump()`.
- JSON does not need the CSV-specific `newline=""` setting.
- The output file stays on disk after the program ends.
- Changing the dictionary later does not update the file. Save again to store the change.

## read versus load

The same file can give text or a parsed Python object, depending on how we read it.

```python
import json

with open("customer_example.json", encoding="utf-8") as file:
    text = file.read()
with open("customer_example.json", encoding="utf-8") as file:
    data = json.load(file)
print(type(text))
print(type(data))
```

Expected output:

```text
<class 'str'>
<class 'dict'>
```

`read()` returns the file's text. `json.load()` reads and parses the JSON. Parsing means reading the format and building Python values from it. Python has no separate built-in `json` data type.

## Read decimal numbers as Decimal

Use `parse_float=Decimal` with `load()` or `loads()` when decimal numbers should become `Decimal` objects.

```python
import json
from decimal import Decimal

order = json.loads('{"order_id": 101, "amount": 19.95}', parse_float=Decimal)
print(order["amount"])
print(type(order["amount"]))
print(type(order["order_id"]))
```

Expected output:

```text
19.95
<class 'decimal.Decimal'>
<class 'int'>
```

This option changes decimal-number parsing, not integer parsing. The default JSON writer cannot write `Decimal` directly. Choose a representation first, such as a string; a string will be loaded back as a string. See [Decimal notes](decimal-money.md).

## Invalid JSON

A trailing comma makes this JSON invalid.

```python
import json

text = '{"name": "Anu",}'
try:
    data = json.loads(text)
except json.JSONDecodeError as error:
    print("Invalid JSON at line:", error.lineno)
```

Expected output:

```text
Invalid JSON at line: 1
```

`JSONDecodeError` is an exception, not a conversion function. Valid JSON can still contain missing fields or wrong business values; parsing alone does not validate an order.

## CSV to JSON practice

CSV readers normally return strings. Convert the numeric fields before saving if the JSON should contain numbers.

Input: [orders.csv](../../../practice/json/orders.csv), four orders with columns `order_id,customer_name,amount,status`.

The completed learner approach is shown below. Run from a scratch folder containing a copy of `orders.csv`; this writes `orders_example.json`.

```python
import csv
import json

orders = []
with open("orders.csv", "r", newline="", encoding="utf-8") as file:
    for row in csv.DictReader(file):
        orders.append({
            "order_id": int(row["order_id"]),
            "customer_name": row["customer_name"],
            "amount": float(row["amount"]),
            "status": row["status"],
        })
with open("orders_example.json", "w", encoding="utf-8") as file:
    json.dump(orders, file, indent=2, ensure_ascii=False, allow_nan=False)
with open("orders_example.json", "r", encoding="utf-8") as file:
    loaded_orders = json.load(file)
print("Record count:", len(loaded_orders))
```

Expected output:

```text
Record count: 4
```

The JSON contains a top-level array of four objects. The learner counted with a loop and printed `4`; `len()` was a tutor-supplied shorter alternative. `float` meets this exercise's requirement; see the Decimal note when exact money handling is needed.

## Practice evidence and links

Saved 30 October 2026 from this conversation and [json.ipynb](../../../practice/json/json.ipynb), cells 0-16 (zero-based), plus [orders.json](../../../practice/json/orders.json).

Saved outputs show nested access and a total of 650, file write/read, an invalid-JSON exception, and the four-record CSV conversion with numeric fields. The tutor supplied starter examples, prompts and feedback. The learner wrote the conversion task; additional help/notes used are unknown. This is guided practice evidence, not a scored independent or delayed assessment. `parse_float=Decimal` was explained; the saved learner cell uses default float parsing, so Decimal use is not demonstrated there. Defining `float("nan")` alone does not demonstrate the rejection option.

The changed-customer exercise (add order 3 and save a new file) was assigned but not verified. The current CSV conversion is complete. Next optional task: inspect missing fields and invalid values before moving to pandas. RDS-001 remains pending separately.

Related: [CSV reading](csv-reading.md), [CSV writing](csv-writing.md), [dictionaries](dictionaries.md), [API requests](api-requests.md). Recall: [JSON questions](../../revision/json-questions.md).

Reference: [Python json documentation](https://docs.python.org/3/library/json.html).
