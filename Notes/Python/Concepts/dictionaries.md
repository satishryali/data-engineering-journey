# Dictionaries

Purpose: associate a meaningful key with a value, such as a record field and its data.
Use a dictionary for keyed records/lookups and a list for a collection of records.
The existing runnable brand lookup below prints `Ford`. Update examples replace a
value or add a unique key. Common pitfalls include mixing a field name with its value,
overwriting earlier records, and confusing assignment `=` with literal `:` syntax.
Recall tasks are separate in [[revision/questions|Questions]].

Source-note correction, 15 October 2026: corrected ordering, assignment/literal syntax
and `udpate` spelling below. These were source-note errors, not additional observed
learner mistakes. Useful original explanations were preserved; prior wording is in Git.
Reference: https://docs.python.org/3/library/stdtypes.html#mapping-types-dict

- Dictioanaries are used to store the data in key value pairs
- Dictionaries preserve insertion order in modern Python, are mutable and have unique keys.
- Does not allow duplicates refers to that it will overwrite the existing values
- we can use dictionary constructor to actually build the dictionaries.

## Accessing items
- ```python
    thisdict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
    }
    ```
- Accessing a single variable :
- ```python
    x = thisdict["brand"]
    print(x)
    ```
- we can use get method to retrive the variables.
- ```python
    x = thisdict.get("brand")
    ```
- use keys() to get all the key items
- ```python
    x = thisdict.keys()
    print(x)
    ```
- use values() to get all the value items
-   ```python
    x = thisdict.values()
    print(x)
    ```
- use items() to all the items
- ```python
    x = thisdict.items()
    print(x)
    ```

- If Exists or not:
- ```python
    if "brand" in thisdict:
        print("yes")
    ```

## Changing the elements

### Method 1 : Direct Key assignment

- ```python

    thisdict = {"brand" : "Ford" , "year" : 1965}
    thisdict["brand"] = "Mustang" #updates existing one.
    thisdict["Color"] = "Red" # adds new key

    ```

### Method 2 : .update() Method

- ```python

    thisdict = {"brand" : "Ford" , "year" : 2000}
    thisdict.update(year = 1965) #updates existing one.
    thisdict.update({"color": "Red"}) # Adds new key
    thisdict.update(year= 1965, brand = "mustang") #updating multiple keys at a time.
    thisdict.update([("year", 2021)]) # using iterable pairs
    ```

### Same key replaces its value

Use `update()` to change fields in one record. It does not collect separate rows.

```python
order = {"order_id": "1001", "customer_id": "C001"}
order.update({"order_id": "1003", "quantity": "3"})
print(order)
```

Expected output:

```text
{'order_id': '1003', 'customer_id': 'C001', 'quantity': '3'}
```

- Existing key `order_id`: its value is replaced.
- New key `quantity`: it is added.
- Key `customer_id` was not supplied: its value stays unchanged.
- Keys must be unique within one dictionary. Different dictionaries can use the same keys.
- This is overwriting a value. Method overriding in OOP means a child class supplies its own version of a parent's method.

To keep several CSV rows, put each row dictionary into a list with `append()`.
See [Keep all CSV rows](csv-reading.md#keep-all-csv-rows).

Added 24 October 2026 from the learner's questions about repeated keys and keeping several rows. Explained with tutor examples; no independent attempt assessed.

### Method 3 : Dictionary comprehension

- ```python
    {k : v * 2 for k,v in thisdict.items()}
    ```

### Method 4 : Merging  |=

- ```python
    thisdict = {"brand": "Ford", "year": 1964}
    thisdict |= {"year": 2020, "color": "red"}
    ```


## Remove Items :

### Method 1 : using pop

- ```python

    thisdict.pop("brand")
    print(thisdict)

    ```

### Method 2 : Removing Last inserted item

- ```python

    thisdict.popitem()
    print(thisdict)

    ```

### Method 3 : deleting the dict & deleting the item using del

- ```python

    del thisdict #Deleting entire dictionary

    del thisdict["model"] #deleting a single value.

    ```

### Method 4 : clear the data in dictionary

- ```python

    thisdict.clear()
    print(thisdict) # Returns empty dictionary.

    ```


## Looping through Dictionaries

- ```python

    for i in thisdict:
        print(thisdict[i])

    ```

- ```python

    for i in thisdict.keys():
        print(i)

    for i in thisdict.values():
        print(i)

    for i,j in thisdict.items():
        print(i,j)

    ```

## Notebook examples with output

These small examples fill the output gaps in the earlier syntax notes. Each example starts with its own input.

### Duplicate keys and live views

```python
car = {"brand": "Ford", "year": 1964, "year": 2000}
keys = car.keys()
print(car["year"])
car["color"] = "white"
print(list(keys))
print(list(car.values()))
print(list(car.items()))
print("brand" in car)
```

Expected output:

```text
2000
['brand', 'year', 'color']
['Ford', 2000, 'white']
[('brand', 'Ford'), ('year', 2000), ('color', 'white')]
True
```

The later value for a duplicate key wins. `keys()` returns a live view: it reflects later dictionary changes. `values()` gives values; `items()` gives key/value pairs. `in` checks keys here.
The notebook also used `dict(name="john", age=36)` to construct a dictionary with string keys.

### Change a value or build a new dictionary

```python
amounts = {"a": 10, "b": 20}
doubled = {key: value * 2 for key, value in amounts.items()}
print(amounts)
print(doubled)
amounts.update([("a", 30)])
amounts |= {"b": 40, "c": 50}
print(amounts)
```

Expected output:

```text
{'a': 10, 'b': 20}
{'a': 20, 'b': 40}
{'a': 30, 'b': 40, 'c': 50}
```

The comprehension builds a new dictionary; it does not change `amounts`. `update()` and `|=` change the existing dictionary, replacing matching keys and adding new ones. `|=` needs Python 3.9 or later.
By contrast, `amounts = {"a": 1}` assigns a replacement dictionary to the name; it does not add to the earlier one.

### Remove a key, clear contents, or delete a name

```python
car = {"brand": "Ford", "year": 2020, "color": "red"}
print(car.pop("brand"))
print(car.popitem())
print(car)
car.clear()
print(car)
del car
```

Expected output:

```text
Ford
('color', 'red')
{'year': 2020}
{}
```

- `pop(key)` removes a key and returns its value.
- `popitem()` removes and returns the last inserted remaining key/value pair.
- `del car["year"]` would remove just that key if present.
- `clear()` empties the dictionary but keeps the variable.
- `del car` removes the variable name. Using that name afterwards raises `NameError`, as the notebook output shows. It does not prove every reference to the object has disappeared.

Source: [Dictionaries.ipynb](../../../practice/Modules/Dictionaries.ipynb), cells 0-65. These are saved practice outputs, with assistance unknown; no independent or delayed review score is inferred. The `NameError` follows an explicit deletion experiment, so it is not automatically a learner misconception.
