# Copy a dictionary before changing it

Use `.copy()` when we need to change an output record without changing the original input.

```python
original = {"order_id": 101, "amount": "500"}
cleaned = original.copy()
cleaned["amount"] = int(cleaned["amount"])

print(original)
print(cleaned)
```

Expected output:

```text
{'order_id': 101, 'amount': '500'}
{'order_id': 101, 'amount': 500}
```

`cleaned = original` gives the same dictionary another name. Updating either name changes that same dictionary. It does not make a copy.

`.copy()` creates a separate outer dictionary. The strings and integers used here are suitable for this pattern. Nested lists or dictionaries would still be shared; this is not a copy of every nested object.

Copying now does not undo earlier changes. If an earlier notebook run changed the input, recreate the original input before checking preservation.

Explained and practised with guidance on 16 October 2026. Related: [dictionary notes](../Python/Concepts/dictionaries.md). Actual observed copy/mutation gaps are recorded as M-PY-008 and M-PY-009 in the [mistake index](../revision/mistakes.md).
