# Generate practice data with Faker

Faker creates made-up names, addresses and other values. Use it for practice records when we do not need real customer details.

## Create a generator

Install packages in the Python environment used by the notebook, if needed. This is a shell command, not Python:

```powershell
python -m pip install Faker faker-commerce
```

```python
from faker import Faker

fake = Faker("en_IN")
print(fake.name())
print(fake.email())
print(fake.phone_number())
print(fake.address())
print(fake.date_of_birth())
```

Expected behaviour: each call returns a made-up value of the requested kind. Exact values vary. The notebook saved names such as `Bhavya Yogi` and `Samuel Pal` from separate calls.

- `Faker` is the class we import; `fake` is the generator object we create.
- `en_IN` is a locale: English settings for India. It affects supported data formats; it does not guarantee every provider produces India-specific data.
- `fake.name()` calls a method, just like the methods in [Objects and printing](objects-and-printing.md).
- Generated values can repeat. Separate method calls do not automatically describe one consistent real person.

## Build customer dictionaries

```python
from faker import Faker

fake = Faker("en_IN")
for i in range(3):
    customer = {
        "customer_id": i + 1,
        "customer_name": fake.name(),
        "email": fake.email(),
        "city": fake.city(),
    }
    print(customer)
```

Expected behaviour: print three dictionaries, with customer IDs `1`, `2`, `3` and varied generated fields. `range(3)` gives `0`, `1`, `2`; adding one makes the IDs start at 1. This loop prints records; it does not save them to a database.

Your notebook uses the same idea for five customers, and its saved output contains five dictionaries.

## Add the commerce provider

A provider adds a group of data-generation methods.

```python
from faker import Faker
from faker_commerce import Provider

fake = Faker("en_IN")
fake.add_provider(Provider)
print(fake.ecommerce_name())
print(fake.ecommerce_category())
print(fake.ecommerce_price())
print(fake.date_time())
```

Expected behaviour: print a product name, category, generated price value and date/time. Values vary. The notebook saved `Handmade Frozen Towels` from `ecommerce_name()`.

- The installation package is `faker-commerce`; the import name is `faker_commerce`.
- `add_provider(Provider)` makes these commerce methods available on this generator.
- The notebook's `faker-ecommerce` installation attempt failed with “No matching distribution found”. That saved failure does not mean Faker itself failed to install.
- Cell 12 currently contains incomplete text, `fake.commerce.`, but retains a previous output. That output cannot verify the code currently shown in that cell.

## Check a method argument before using it

The product-writing cell uses:

```python
fake.ecommerce_price(random.randint(5000, 50000))
```

This is the learner's existing expression, not a corrected example to copy. It also needs `import random` and the generator/provider setup above.

The installed provider's signature is `ecommerce_price(as_int: bool = True)`. Its first argument selects integer versus decimal-style output; it does not set a price limit. Passing a positive random integer takes the true branch, so this call does not restrict the result to 5,000-50,000. The saved CSV includes `20292072` as one price. No INR meaning is automatically attached to the generated number.

This finding explains the current expression. The notebook has been preserved for the learner to investigate and change.

## What the product loop has done

The final cell combines Faker, [random](random.md) and [CSV writing](csv-writing.md):

- Writes a header with product ID, name, category, selling price and created-at fields.
- Runs `range(1000)` and uses `i + 1` for IDs.
- Calls the provider for values and writes each row with `writerow()`.
- Uses a relative filename, so the destination depends on the notebook's working folder.

The file [product_data.csv](../../../projects/rrdap/Test/product_data.csv) was inspected on 17 October 2026: **1,000 nonempty data records**, plus the header and **1,001 empty rows** from extra line endings. Its bytes contain `\r\r\n`. The writing cell omits `newline=""`; see the existing [newline explanation](csv-writing.md#why-newline-matters).

The file is CSV-generation evidence. PostgreSQL loading and SQL verification are still pending; this is not completion of RDS-001.

## Sources

Practice: [datafaker.ipynb](../../../projects/rrdap/Test/datafaker.ipynb), cells 0-23 (zero-based). Saved output and the CSV were inspected; assistance is unknown. Small standalone examples above were checked separately, without rerunning the product-writing cell or changing the learner's files.

References: [Faker documentation](https://faker.readthedocs.io/en/master/), [commerce provider](https://github.com/nicobritos/python-faker-commerce), [price method source](https://github.com/nicobritos/python-faker-commerce/blob/main/faker_commerce/__init__.py).
