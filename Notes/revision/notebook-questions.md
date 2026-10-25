# Notebook recall questions

- Decimal prices, added 25 October 2026: for quantity `"4"` and unit price `"12.35"`, predict and calculate the amount directly from CSV strings without a float conversion. Explain why `Decimal("0.1")` differs from `Decimal(0.1)`, and compare default rounding with half-up rounding for `Decimal("8.125")` to two decimal places. State any help used. Pending; not an answered review.

- Function results and a combined report, added 25 October 2026: explain why a fresh list inside each function call does not collect earlier calls, and why repeated `update()` calls do not keep separate rows. Build a small function that returns one counts dictionary, collect two calls without a global list inside that function, and write the combined results once. Explain what happens on rerun with `"w"` versus `"a"`. Pending; no scored review.

Try one task before opening its explanation. These prompts have not been answered or scored.

- Dictionaries: predict what a saved `keys()` view contains after adding a key. Build a doubled-value dictionary and explain whether the input changed. Compare `pop()`, `popitem()`, `clear()` and `del` with a small example.
- CSV: read an employee name containing a comma correctly. Write two synthetic employees to a new CSV, read them back and explain their Python types. Explain the role of `newline=""` and `fieldnames`.
- Files: predict two consecutive `read()` calls, then use `seek(0)` to reread. Explain `file.read` versus `file.read()` and what `print(help(...))` adds.
- Objects: reconstruct the small employee example and explain what `self`, `__init__` and `__str__` do.
- Random: choose two categories with and without repeated picks, repeat a seeded sequence, and shuffle a list. Explain the return values and whether the original list changes.
- Faker: generate three customer dictionaries and explain the locale and provider. Inspect the price method's argument before predicting its effect. Explain why a generated CSV does not prove records were loaded into PostgreSQL.

- CSV row collection, added 24 October 2026: read the completed-orders CSV into a list of dictionaries, then show its row count and first row. Predict the count if the file contained five data rows. Explain why repeated `order_id` keys in separate dictionaries are kept, while repeated `update()` calls on one dictionary replace earlier values. Not yet attempted or scored.

- Two context managers, added 24 October 2026: copy a small CSV to a different file using one `with` statement. Explain when both files close and why writing a file then reading that same file uses separate blocks in the notes. Not yet attempted or scored.

Explanations are linked from [Python notes](../Python/Index.md). These questions do not replace the pending RDS-001 task.

- Order summary logic, added 24 October 2026: use three orders: completed (quantity 2, price 40), completed (quantity 1, price 90), cancelled (quantity 3, price 20). Predict the two summary rows, then build and run the summary. Explain order count versus quantity and why summary writing belongs after the loop. State any notes or help used. Pending; no score or completed review.
