# Split text using split()

Use `split()` when one string contains several pieces of information and you want a list of those pieces. The original string stays unchanged.

## Split at a chosen separator

A separator is the text marking where to split, such as a comma.

Syntax: `text.split(separator, maxsplit)`

Both arguments are optional. `maxsplit` limits how many splits are made; leaving it out splits at every matching separator.

```python
order = "501,250"
parts = order.split(",")
print(parts)
print(order)
```

Expected output:

```text
['501', '250']
501,250
```

- `split(",")` cuts at commas and returns a list.
- Both pieces are still strings. Splitting does not convert `"250"` into an integer.

## Split on spaces

```python
text = "  order   ready  "
print(text.split())
print(text.split(" "))
```

Expected output:

```text
['order', 'ready']
['', '', 'order', '', '', 'ready', '', '']
```

- `split()` without a separator groups whitespace, including spaces, tabs and newlines. It ignores whitespace at the ends.
- `split(" ")` splits at each single space. Repeated or end spaces produce empty strings.

## Limit the splits

```python
record = "501,250,paid"
print(record.split(",", 1))
```

Expected output:

```text
['501', '250,paid']
```

`1` means make at most one split. The rest stays together.

## CSV files

Use `csv.reader` or `csv.DictReader` for actual CSV files. A quoted value can contain a comma, so `split(",")` can cut one value into separate pieces incorrectly.

Prepared at the learner's request on 17 October 2026. Later inspected practice: [csv-module.ipynb](../../practice/Modules/csv-module.ipynb), cells 1-8, has saved output for comma splitting and `maxsplit=1`. Cells 9-13 compare splitting with quoted CSV reading; see [CSV reading](../Python/Concepts/csv-reading.md). Assistance is unknown; this is not a scored independent assessment.
