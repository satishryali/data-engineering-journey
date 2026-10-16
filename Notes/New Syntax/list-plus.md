# Join lists using +

Use `+` to join two lists and make a new list. This is useful when we want extra test records without adding them to the original list.

## A small example

```python
payments = [
    {"order_id": 202, "amount": "1200"},
    {"order_id": 203, "amount": "450"},
]

test_payments = payments + [{"order_id": 205, "amount": "bad"}]

print(payments)
print(test_payments)
```

Output verified by running:

```text
[{'order_id': 202, 'amount': '1200'}, {'order_id': 203, 'amount': '450'}]
[{'order_id': 202, 'amount': '1200'}, {'order_id': 203, 'amount': '450'}, {'order_id': 205, 'amount': 'bad'}]
```

- `{"order_id": 205, "amount": "bad"}` is one dictionary.
- `[{"order_id": 205, "amount": "bad"}]` is a list containing that dictionary.
- `payments + [...]` joins the two lists, keeping their order.
- `test_payments =` stores the new list under a new name.
- The original `payments` list still has two records. The new list has three.
- `"bad"` is just text here. This line does not convert amounts to numbers.

## Why the square brackets matter

Both sides of `+` must be lists in this example.

```python
payments + {"order_id": 205, "amount": "bad"}
```

This raises `TypeError`: it tries to join a list and a dictionary. Wrap the dictionary in `[]` to make it a one-item list.

Use [`append()`](../Python/Concepts/lists.md#adding-an-item-using-append) when you want to add a record to the existing list instead.

The new list reuses the existing dictionaries; it does not make separate copies of them. Changing a field in one of those shared dictionaries can be seen through both lists.

Related: [Lists](../Python/Concepts/lists.md).

Added from the tutor's example on 16 October 2026. Reference preparation; not an assessed learner attempt.
