# Objects and printing

An object can hold related values and methods that work with those values. The notebook used an employee to explore why printing an object differs from asking it for a value.

## Create an employee

```python
class Employee:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

employee = Employee("Ravi")
print(employee.get_name())
```

Expected output:

```text
Ravi
```

- `class Employee` defines a kind of object.
- `Employee("Ravi")` creates an instance: one employee object.
- `__init__` sets its starting values.
- `self` refers to the instance receiving the method call.
- `self.name` stores a value on that instance. This stored value is called an attribute.
- `get_name()` returns that value.

Without a custom display method, `print(employee)` shows a default object description containing its class name and an address-like value. That value changes between runs; it is not the employee's data.

## Choose what print displays

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def get_salary(self):
        return self.salary

    def __str__(self):
        return f"Employee : {self.name}, Salary : {self.salary}"

employee = Employee("Ravi", 45000)
print(employee)
print(employee.get_salary())
```

Expected output:

```text
Employee : Ravi, Salary : 45000
45000
```

`__str__` returns readable text used by `print(employee)`. Return a string from it; printing inside it is not a replacement for returning the string. `get_salary()` returns the salary separately.

## The difference between `__str__` and `__repr__`

Python provides two display methods because end users and developers need different information:

* **`__str__`**: For end users. Should be readable and friendly (e.g. `Satish`).
* **`__repr__`**: For developers and debugging. Should be exact and show what object it is (e.g. `Customer(name='Satish')`).

```python
class Customer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Customer(name={self.name!r})"

customer = Customer("Satish")
print(str(customer))
print(repr(customer))
```

Expected output:

```text
Satish
Customer(name='Satish')
```

### Where Python automatically uses `__repr__`

Even if `__str__` exists, Python automatically uses `__repr__` in several places:

1. **Inside lists and collections**: Printing a list of objects calls `__repr__` on every item so you know what types are inside.
2. **In Jupyter notebooks**: For a simple class, a bare variable commonly shows its representation. Rich display methods can provide other formats.
3. **In debugging and logging**: Inspectors often use the representation. In logging, `%r` requests it; `%s` requests the string form.

```python
customers = [Customer("Satish"), Customer("Ravi")]
print(customers)
```

Expected output:

```text
[Customer(name='Satish'), Customer(name='Ravi')]
```

If `__repr__` is missing, the list uses each object's default representation. If it returns only `self.name`, the list looks like `[Satish, Ravi]` without string quotes, making the object type unclear.

### How `print()` chooses between them

When you call `print(obj)`:

1. Python checks for `__str__`. If it exists, it uses it.
2. If `__str__` is **missing**, Python **falls back to `__repr__`**.
3. If neither exists, it prints a default object description with an address-like value `<Customer object at 0x...>`.

### Choose a useful representation

A useful `__repr__` makes data objects easier to inspect. Add a custom `__str__` when you need a different display for people; there is no required order for writing these methods.

If you only write `__repr__`, both `print(obj)` and `print([obj])` work cleanly. If you only write `__str__`, lists and debuggers will fall back to the raw memory address.

This is also why `@dataclass` generates `__repr__` automatically for you: developers inspect data objects constantly during ETL and debugging.

## Measure length with `__len__`

Why we need it: Python's built-in `len(obj)` doesn't know what "length" means for your custom object. Defining `__len__` lets you write the logic.

```python
class OrderBatch:
    def __init__(self, batch_id, orders):
        self.batch_id = batch_id
        self.orders = orders

    def __len__(self):
        # We decide the logic: count the items in the list
        return len(self.orders)

batch = OrderBatch("B1", ["order-101", "order-102", "order-103"])
print(len(batch))
```

Expected output:

```text
3
```

- `len(batch)` calls `batch.__len__()` behind the scenes.
- **Rule:** `__len__` must return a whole integer $\ge 0$. Returning a float, negative number, or `None` raises an error.
- **Bonus:** Defining `__len__` gives your object automatic True/False checks (`if batch:` is `True` when length > 0, and `False` when empty).

## Indexing, looping and searching with `__getitem__`

Why we need it: To access an object using square brackets `batch[0]` like a list or dictionary.

```python
class OrderBatch:
    def __init__(self, orders):
        self.orders = orders

    def __getitem__(self, position):
        return self.orders[position]

batch = OrderBatch(["order-A", "order-B", "order-C"])
print(batch[1])
```

Expected output:

```text
order-B
```

- `batch[1]` calls `batch.__getitem__(1)`.

### Three superpowers unlocked by `__getitem__`

When you define `__getitem__`, Python automatically unlocks three features without any extra code:

1. **`for` loops work automatically:**
   ```python
   for order in batch:
       print(order)
   ```
   Expected output:
   ```text
   order-A
   order-B
   order-C
   ```
   *How it works:* Python starts at index `0`, then `1`, then `2`, and stops when `IndexError` is hit.

2. **`in` checks work automatically:**
   ```python
   print("order-B" in batch)
   ```
   Expected output:
   ```text
   True
   ```
   Python uses `__getitem__` to scan items until it finds a match.

3. **Slicing works:**
   ```python
   print(batch[0:2])
   ```
   Expected output:
   ```text
   ['order-A', 'order-B']
   ```
   Python passes the slice `0:2` directly into `__getitem__`.

Source: [csv-module.ipynb](../../../practice/Modules/csv-module.ipynb), cells 15 and 19-20, and [dataclass.ipynb](../../../practice/Dataclass/dataclass.ipynb). Saved output shows the name and custom employee display. This is a basic example, not an assessed OOP exercise or a requirement to use classes in RDS-001.
Reference: [Python object string representation](https://docs.python.org/3/reference/datamodel.html#object.__str__), [object.__repr__](https://docs.python.org/3/reference/datamodel.html#object.__repr__), and [emulating container types](https://docs.python.org/3/reference/datamodel.html#emulating-container-types).

## Separate practice examples

See [special methods](special-methods.md) for one small example per method and [dataclasses](dataclasses.md) for generated creation, representation and equality methods. `repr(value)` calls the representation method; `f"{value!r}"` requests that representation inside an f-string.

The notebook's `print(str(obj))` where obj is a list still shows each customer's representation: the outer object is the list. Saved date output also contrasts `2026-10-26` with `datetime.date(2026, 10, 26)`. These outputs were inspected, not rerun.
