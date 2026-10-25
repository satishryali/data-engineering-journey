# Decimal for prices and totals

Use `Decimal` for decimal prices such as `250.50`. It avoids the binary floating-point approximation introduced by `float` for values such as `0.1`.

## Import and create a Decimal

```python
from decimal import Decimal

price = Decimal("250.50")
quantity = 2
total = price * quantity
print(total)
```

Expected output:

```text
501.00
```

Pass the decimal value as a string. `Decimal("0.1")` starts from the decimal text. `Decimal(0.1)` starts from a float and carries its approximation into the Decimal.

The other import style is:

```python
import decimal

price = decimal.Decimal("250.50")
print(price)
```

Expected output:

```text
250.50
```

Use the call that matches your import: `Decimal(...)` or `decimal.Decimal(...)`.

## Convert the CSV price directly

CSV values arrive as strings, so convert the price directly to `Decimal` and the whole-number quantity to `int`.

```python
from decimal import Decimal

row = {"quantity": "3", "unit_price": "19.95"}
quantity = int(row["quantity"])
unit_price = Decimal(row["unit_price"])
amount = quantity * unit_price

total = Decimal("0.00")
total += amount
print(amount)
print(total)
```

Expected output:

```text
59.85
59.85
```

- `int("19.95")` cannot read a decimal price. Use `Decimal(row["unit_price"])` for that field.
- Keep whole-number order counts as integers. Amounts and counts are different things.
- `Decimal("0.00")` is a useful starting amount: it stays a Decimal even when no matching orders are found. Integer `0` can also be added to a Decimal, as in the learner's current code.
- Avoid `Decimal(float(row["unit_price"]))`; it converts to float first. Also avoid mixing Decimal amounts with float amounts in addition or multiplication; use Decimal values consistently.

## Round to two decimal places

`quantize(Decimal("0.01"))` sets the result to two decimal places. Choose the rounding rule required by the calculation.

```python
from decimal import Decimal, ROUND_HALF_UP

amount = Decimal("12.345")
rounded = amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
print(amount)
print(rounded)
print(round(amount, 2))
```

Expected output with Python's default Decimal rounding context:

```text
12.345
12.35
12.34
```

- `ROUND_HALF_UP` rounds to the nearest value; an exact halfway value rounds away from zero.
- The default Decimal rounding rule is `ROUND_HALF_EVEN`: a halfway value chooses the neighbour whose last kept digit is even. That is why `round(Decimal("12.345"), 2)` gives `12.34` under the default context.
- `round(decimal_amount, 2)` returns a Decimal and follows the current Decimal context's rounding rule. It does not automatically select half-up rounding.
- These calls return new values; they do not change `amount`.
- Decimal arithmetic still has a precision limit set by its context. Using Decimal does not mean every possible calculation is unlimited or needs no rounding policy.

## Learning evidence

Added 25 October 2026 after the learner asked for `decimal.Decimal` syntax. The supplied notebook snapshot imports `Decimal`, multiplies `int(quantity) * Decimal(unit_price)`, adds those amounts to totals, and calls `round(total, 2)` when writing summaries. Those are source-code observations; the attached output snapshot is empty. This note does not establish correct report outputs or independent understanding.

The current snapshot also returns a counts dictionary and collects returned results outside the function before a combined write. That supersedes the earlier global-list design in the older snapshot. Printing the returned dictionary outside the function is not shown; acceptance remains unverified.

The examples above are tutor examples. Recall practice is separate in [Notebook recall questions](../../revision/notebook-questions.md). Related: [CSV reading](csv-reading.md), [CSV writing](csv-writing.md), [Order-summary logic](../Logic/order-summary-after-loop.md).

Reference: [Python Decimal documentation](https://docs.python.org/3/library/decimal.html).
