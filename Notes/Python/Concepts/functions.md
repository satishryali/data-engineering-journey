# Functions

Use a function when we want to run the same steps with different input.

## Input and return

```python
def double_amount(amount):
    result = amount * 2
    return result

print(double_amount(25))
print(double_amount(10))
```

Expected output:

```text
50
20
```

- `amount` is the parameter: the name the function uses for its input.
- `double_amount(25)` passes `25` into that parameter.
- `return` sends a result back to the caller. It does not print it.
- Use the parameter inside the function, rather than a particular notebook variable.

## Fresh lists for each call

In our cleaner, create `valid_orders = []` and `rejected_orders = []` inside the function, before its loop. Each call then starts with empty lists.

```python
def collect_items(items):
    result = []
    for item in items:
        result.append(item)
    return result

print(collect_items([1, 2]))
print(collect_items([]))
```

Expected output:

```text
[1, 2]
[]
```

Our cleaner returns two lists with `return valid_orders, rejected_orders`. Capture them using `valid_result, rejected_result = clean_orders(orders)`.

For collecting results from several calls, see [Collect function results and write once](../Logic/collect-function-results-write-once.md). Each call can return its own result while the caller keeps them together.

Practice on 16 October 2026: function corrections needed guidance about the parameter, fresh lists and return. Saved notebook output confirms changed input, empty input and original five-order results. Independent reconstruction is still pending.
