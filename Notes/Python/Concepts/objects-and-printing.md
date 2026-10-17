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

Source: [csv-module.ipynb](../../../practice/Modules/csv-module.ipynb), cells 15 and 19-20. Saved output shows the name and custom employee display. This is a basic example, not an assessed OOP exercise or a requirement to use classes in RDS-001.
Reference: [Python object string representation](https://docs.python.org/3/reference/datamodel.html#object.__str__).
