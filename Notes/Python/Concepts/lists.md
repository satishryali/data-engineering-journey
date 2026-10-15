# Lists

- Lists are used to store multiple items in one variable.
- We can keep the items in order, change them and add new items.
- Lists allow repeated values.
- We use square brackets `[]` to create a list.

## Why we use lists

- Suppose we have three fruits. Instead of making a separate variable for each
  fruit, we can keep all three in one list.

```python
fruits = ["apple", "banana", "mango"]
print(fruits)
```

Output:

```text
['apple', 'banana', 'mango']
```

## Accessing items

- Each item has a position. In Python, this position is called an index.
- The first item is at position `0`, the second at `1` and the third at `2`.

```python
fruits = ["apple", "banana", "mango"]

print(fruits[0])  # First item
print(fruits[1])  # Second item
print(fruits[2])  # Third item
```

Output:

```text
apple
banana
mango
```

## Changing an item

- We can use its position to replace an existing item.

```python
fruits = ["apple", "banana", "mango"]
fruits[1] = "orange"  # Replace banana
print(fruits)
```

Output:

```text
['apple', 'orange', 'mango']
```

- Here we changed one item. We did not add another item to the list.

## Adding an item using append

- `append()` adds one item at the end of the list.

```python
fruits = ["apple", "banana"]
fruits.append("mango")
print(fruits)
```

Output:

```text
['apple', 'banana', 'mango']
```

### Starting with an empty list

- We can create an empty list and add items when we get them.

```python
files = []
files.append("customers.csv")
files.append("orders.csv")
print(files)
```

Output:

```text
['customers.csv', 'orders.csv']
```

## Finding how many items we have

- `len()` tells us the number of items in the list.

```python
numbers = [10, 20, 30]
print(len(numbers))
```

Output:

```text
3
```

## Repeated values are allowed

```python
fruits = ["apple", "apple", "banana"]
print(fruits)
print(len(fruits))
```

Output:

```text
['apple', 'apple', 'banana']
3
```

- Both apple items stay in the list. Python does not remove repeated values for us.

## Keeping dictionaries inside a list

- A dictionary can describe one record.
- A list can keep several records together.

```python
files = []
files.append({"name": "customers.csv"})
files.append({"name": "orders.csv"})
print(files)
```

Output:

```text
[{'name': 'customers.csv'}, {'name': 'orders.csv'}]
```

- Here we have two separate dictionaries inside one list.
- Both stay because we added each one using append.
- For dictionary basics, see [[Python/Concepts/dictionaries|Dictionaries]].

## Common mistake with append

- We do not need to save the result of append back into the list variable.
- append already changes the list. Its return value is `None`, not the updated list.

### Wrong way

```python
fruits = ["apple"]
fruits = fruits.append("banana")
print(fruits)
```

Output:

```text
None
```

- The variable fruits now holds `None`. It no longer holds our list.

### Correct way

```python
fruits = ["apple"]
fruits.append("banana")
print(fruits)
```

Output:

```text
['apple', 'banana']
```

## Things to remember

- Change an existing item: use its position, like `fruits[1] = "orange"`.
- Add one new item: use `fruits.append("mango")`.
- Count the items: use `len(fruits)`.
- Trying to read a position that does not exist gives `IndexError`.
- We can use lists to keep file names, processing steps or several records.

## Questions for later

- Practise using [[revision/list-questions|List questions]]. Answers are kept out of
  that question file so we can try first.

## Reference

- [Python lists](https://docs.python.org/3/library/stdtypes.html#lists)
- [Python list methods](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)
- Prepared on request, 15 October 2026. These are reference notes; the current
  dictionary task, study timer and review dates are unchanged.
