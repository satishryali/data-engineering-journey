"""Bounded challenges; Python is always manual until a contained runner is tested."""
PYTHON = [
    ('clean-records', 'py.records.cleaning', 'Clean records without changing input',
     'Write clean_orders(rows). Convert amount with int, copy valid dictionaries, keep invalid originals and reasons, and return two lists. Example: [{"id":1,"amount":" 7 "},{"id":2,"amount":"bad"},{"id":3,"amount":"0"}] gives valid amounts 7 and 0 plus one rejection. Test empty input and repeated calls. Catch ValueError per record; retain source rows.'),
    ('dictionary', 'py.dict.mutate', 'Update one dictionary safely',
     'Starting with {"id":11,"amount":"40"}, create a changed copy whose amount is integer 45. Original must retain string "40". Show both outputs and explain copying. Constraint: no mutation of the original.'),
    ('list-records', 'py.list.records', 'Collect selected records',
     'Given [{"id":1,"active":True},{"id":2,"active":False},{"id":3,"active":True}], return IDs of active records in input order. Expected [1,3]. Handle empty input; preserve input.'),
    ('csv-read', 'py.csv.read', 'Read a quoted CSV',
     'Use csv.reader on a scratch text stream containing id,name followed by 1,"Asha, Sales" and 2,Devi. Expected two data rows, with the comma inside one name. Handle the header and explain returned types.'),
    ('csv-write', 'py.csv.write', 'Write and read dictionaries',
     'Use DictWriter on a scratch StringIO with id,name headers and rows {"name":"Asha, Sales","id":1}, {"id":2,"name":"Devi"}. Read with DictReader. Expected string IDs "1","2" and intact comma in the first name. Explain fieldnames and newline handling.'),
    ('files', 'py.files.methods', 'Trace a file cursor',
     'Using a scratch StringIO containing "one\\ntwo\\n", read one line then the rest, seek to zero and readlines. Show expected outputs and explain the cursor. Close using a context manager.'),
    ('random', 'py.random.basics', 'Repeatable synthetic data',
     'Use random.Random(42) to make five records with unique sequential IDs and amounts between 10 and 20 inclusive. Verify bounds and reproducibility. Explain why random amounts need not be unique. Faker extension: describe where a locale affects generated names without claiming unique output.'),
]
SQL = [
    ('sql-count', 'sql.count.nulls', 'Count actual orders', 'Return customer_id, name, COUNT of actual orders, including customers with zero orders. Group by identity; output in customer_id order.', 'count'),
    ('sql-join', 'sql.join.preservation', 'Preserve every customer', 'Return customer_id and order_id for every customer, retaining unmatched rows. Sort by customer_id, order_id.', 'join'),
    ('sql-sum', 'sql.sum.nulls', 'Aggregate nullable amounts', 'Return customer_id, name and SUM of order amounts. Preserve unmatched customers; keep NULL sums as NULL. Group by identity; sort by customer_id.', 'sum'),
    ('sql-grain', 'sql.group.grain', 'Keep shared names separate', 'Return customer_id, name and actual order count. Different customer IDs with the same name must stay separate. Sort by customer_id.', 'count'),
]
