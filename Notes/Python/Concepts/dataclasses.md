# Dataclasses

A dataclass gives records with known fields one shared definition. It saves repeated class code when passing records between ETL functions. Dictionaries remain useful for raw CSV rows, JSON with changing keys and small lookups.

## Create an order

```python
from dataclasses import dataclass

@dataclass
class Order:
    order_id: int
    status: str
    quantity: int

order = Order(order_id=1001, status="completed", quantity=3)
print(order)
print(order.quantity)
```

Expected output:

```text
Order(order_id=1001, status='completed', quantity=3)
3
```

- `class Order` defines a kind of record. `order` is one instance.
- `order.quantity` reads its quantity attribute. A dictionary uses `order["quantity"]`.
- `@dataclass` normally generates `__init__`, `__repr__` and `__eq__`. These create, describe and compare records.
- It does not generate a custom `__str__`. Printing falls back to its generated representation.

## Why use it when dictionaries exist

These dictionaries have different keys, and both are valid:

```python
first = {"order_id": 1001, "quantity": 3}
second = {"order_id": 1002, "qty": 4}
```

A shared dataclass makes the accepted constructor fields clear. With the Order definition above, `Order(order_id=1002, status="pending", qty=4)` raises `TypeError` because `qty` is unexpected. This checks constructor arguments; it does not validate the supplied field values.

Use a dataclass when several functions handle the same kind of record with known fields. A possible ETL flow is raw dictionary → conversion and validation → Order object → processing. Dataclasses are optional; a small ETL task can work well with dictionaries.

## Type hints do not convert values

The saved notebook supplied `order_id="1001"` despite declaring `order_id: int`. Its saved output retained quotes:

```text
Order(order_id='1001', status='completed', quantity=3)
```

That is evidence that the value stayed a string. A type hint describes the intended type; a plain dataclass does not enforce it at runtime. Convert CSV text explicitly, for example `int("1001")`. Invalid text such as `int("abc")` raises `ValueError`. Business checks, such as a positive quantity, also need your code.

## The same display with a regular class

```python
class Order:
    def __init__(self, order_id, quantity):
        self.order_id = order_id
        self.quantity = quantity

    def __repr__(self):
        return f"Order(order_id={self.order_id!r}, quantity={self.quantity!r})"

order = Order(1001, 3)
print(order)
```

Expected output:

```text
Order(order_id=1001, quantity=3)
```

Here we wrote the creation and display methods ourselves. This class does not yet define field-based equality. `!r` asks for a value's representation; strings include quotes. See [objects and printing](objects-and-printing.md) and [special methods](special-methods.md).

## Sources and learning status

Prepared from the learner's questions and [repository notebook](../../../practice/Dataclass/dataclass.ipynb), including saved dataclass outputs. Attached snapshots could not be read because filesystem access was denied; they were not edited. Saved notebook output was inspected, not rerun. Help and independent understanding are unknown; no assessment or retention success is claimed.

References: [Python dataclasses](https://docs.python.org/3/library/dataclasses.html) and [PEP 557 motivation](https://peps.python.org/pep-0557/#rationale).
