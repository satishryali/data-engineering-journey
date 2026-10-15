# using with (Automatic Cleanup)

- with statement is called a context manager
- It will something like
- "Open this resource, let me do my work, and no matter what happens (even if my code crashes with an error), clean it up and close it when I exit."
- Why we need it
- Whenever your program opens an external resource—like a file, a database connection, or a network socket—it consumes memory on your computer or database server. You must always close it when done.
- with (Syntax)

```python
with <FUNCTION_THAT_OPENS_SOMETHING> as <VARIABLE_NAME>:
    # Do your work here (indented)
    pass
```

- Ex :

```python
with psycopg2.connect(...) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM raw_customers;")
        rows = cur.fetchall()
```
