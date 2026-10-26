# Special methods

Special methods let normal Python operations work with your objects. Their names have double underscores at both ends, so people call them dunder or magic methods. Each example below stands alone. Outputs are expected, not freshly executed.

## __init__ - store starting values

Python calls this after creating the object, to set its starting values.

```python
class Order:
    def __init__(self, quantity):
        self.quantity = quantity

order = Order(3)
print(order.quantity)
```

Expected output:

```text
3
```

`Order(3)` passes 3 to `__init__`. `self` refers to this particular order.

## __repr__ - describe an object

Use this to inspect an object while debugging.

```python
class Order:
    def __repr__(self):
        return "Order(quantity=3)"

order = Order()
print(repr(order))
```

Expected output:

```text
Order(quantity=3)
```

`repr(order)` calls `__repr__`. This tiny example returns fixed text; it does not store a quantity. The method must return a string.

## __str__ - display readable text

Use this to choose the text shown by print.

```python
class Order:
    def __str__(self):
        return "This order contains 3 units"

order = Order()
print(order)
```

Expected output:

```text
This order contains 3 units
```

`print(order)` uses `__str__`. Return the text; do not replace return with print inside the method.

## __eq__ - compare with ==

Choose which values make two objects equal.

```python
class Order:
    quantity = 3

    def __eq__(self, other):
        return self.quantity == other.quantity

first = Order()
second = Order()
second.quantity = 5
print(first == second)
```

Expected output:

```text
False
```

This compares 3 == 5. It assumes both operands are Order objects. Without a custom equality method, two separate instances of an ordinary class do not become equal just because their attributes match.

## __lt__ - compare with <

Choose what less than means for your objects.

```python
class Order:
    quantity = 3

    def __lt__(self, other):
        return self.quantity < other.quantity

first = Order()
second = Order()
second.quantity = 5
print(first < second)
```

Expected output:

```text
True
```

This compares 3 < 5. The notebook used > inside __lt__, so first < second with quantities 10 and 20 returned False. Python follows the method body; it does not correct the comparison for us. Both operands here are assumed to be Order objects.

## __gt__ - compare with >

This is the greater-than partner of __lt__.

```python
class Order:
    quantity = 3

    def __gt__(self, other):
        return self.quantity > other.quantity

first = Order()
second = Order()
second.quantity = 5
print(second > first)
```

Expected output:

```text
True
```

This compares 5 > 3. Prefer the normal operator to a direct call such as second.__gt__(first). These comparison examples use a simple class default; assigning second.quantity gives that object its own value.

## __len__ - support len

Return how many items the object represents.

```python
class Batch:
    def __init__(self, orders):
        self.orders = orders

    def __len__(self):
        # Custom logic: count the items in the list
        return len(self.orders)

batch = Batch(["order-A", "order-B", "order-C"])
print(len(batch))
```

Expected output:

```text
3
```

- `len(batch)` calls `__len__` in the background.
- Python has no default way to calculate length for your custom object, so you must write the counting logic inside `__len__`.
- **Strict rule:** The return value must be an integer $\ge 0$. The notebook returned `-1` and hit `ValueError: __len__() should return >= 0`. Returning a float, negative integer, or `None` raises an error.
- **Truthiness:** Defining `__len__` also gives your object automatic boolean checks (`if batch:` evaluates to `True` when length $> 0$, and `False` when empty).

## __getitem__ - support square brackets

Read an item by its position, loop over items, and check membership.

```python
class Batch:
    def __init__(self, rows):
        self.rows = rows

    def __getitem__(self, position):
        return self.rows[position]

batch = Batch(["order-A", "order-B"])
print(batch[1])
```

Expected output:

```text
order-B
```

`batch[1]` passes 1 to `__getitem__`. Positions start at 0, so position 1 is the second item.

**What makes `__getitem__` special:**

Writing `__getitem__` automatically gives your class three features without any extra code:

1. **`for` loops work automatically:**
   ```python
   for row in batch:
       print(row)
   ```
   Expected output:
   ```text
   order-A
   order-B
   ```
   Python calls `batch[0]`, then `batch[1]`, and stops when it hits `IndexError`.
2. **`in` membership checks work automatically:**
   ```python
   print("order-A" in batch)  # True
   print("order-Z" in batch)  # False
   ```
   Python scans through the items using `__getitem__` until it finds a match.
3. **Slicing works:**
   ```python
   print(batch[0:1])  # ['order-A']
   ```
   Python converts `0:1` into a `slice` object and passes it to `__getitem__`.

Best practice: Store `self.rows` on the instance in `__init__` rather than recreating the list inside `__getitem__` on every lookup.

## __iter__ - support a for loop

Give Python a way to obtain items one at a time.

```python
class Batch:
    def __iter__(self):
        return iter(["order-A", "order-B"])

for row in Batch():
    print(row)
```

Expected output:

```text
order-A
order-B
```

`iter(...)` returns an iterator: an object that supplies items one at a time. We reuse the list iterator.

## __enter__ - enter a with block

A context manager supports with. Both methods are required in this example; focus on __enter__.

```python
class Session:
    def __enter__(self):
        print("Entering")
        return "ready"

    def __exit__(self, exc_type, exc_value, traceback):
        pass

with Session() as value:
    print(value)
```

Expected output:

```text
Entering
ready
```

__enter__ runs before the block. Its returned value becomes value. This example does not start a study timer or open a resource.

## __exit__ - leave a with block

Focus on the cleanup step when the block finishes.

```python
class Session:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Leaving")
        return False

with Session():
    print("Inside")
```

Expected output:

```text
Inside
Leaving
```

__exit__ runs when leaving the block, including when its body raises an exception. The three arguments describe the exception, or are None on normal exit. Returning False lets an exception continue. If __enter__ itself fails, this context manager's __exit__ is not called.

## Sources and learning status

The learner requested one small example per method. Repository notebook cells 9516b0c9, f0cfef02, 7e3383d1, 64b57fa9, 04f64e9c, a0504000 and 4a8f5aaa contain related practice and saved outputs; assistance is unknown. The iteration and context-manager examples were explained in conversation; no learner execution was inspected for them. No scored assessment is recorded. These notes explain the saved comparison/length behaviour without editing the attempt or claiming a verified correction.

Related: [objects and printing](objects-and-printing.md), [dataclasses](dataclasses.md), [with and cleanup](with(Context_Manager).md). Reference: [Python data model](https://docs.python.org/3/reference/datamodel.html#special-method-names).
