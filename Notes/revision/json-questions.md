# JSON recall questions

Try one bounded task at a time without opening the explanation first. State any notes or help used. These prompts are not completed assessments.

1. Explain how a Python dictionary differs from JSON text and a JSON file. Does JSON have to live on disk?
2. For JSON containing an object, an array and a string, predict the default Python type produced by `loads()`.
3. Reconstruct an example of each: `load`, `loads`, `dump`, `dumps`. Explain the input and result.
4. Read a customer with three nested orders. Print their IDs and calculate the total. Run the cell twice and explain how you prevent an accumulated old total.
5. Compare reading the same file with `file.read()` and `json.load(file)`. Print their types.
6. Compare output with and without `indent`, `sort_keys` and `ensure_ascii=False`. Does escaped Unicode lose the original characters?
7. Predict what `allow_nan=False` does when writing `float("nan")`. Test in memory using `dumps()`.
8. Read a decimal number with `parse_float=Decimal`; compare its type with default parsing. Explain why default `dumps()` cannot directly write the resulting Decimal.
9. Catch invalid JSON containing a trailing comma and print the error's line number. Explain why this does not check business values.
10. With a changed small CSV, convert IDs and amounts, save one JSON array, read it back and calculate the count from the loaded data. Preserve the original input.

Explanation and completed example: [JSON](../Python/Concepts/json.md).
