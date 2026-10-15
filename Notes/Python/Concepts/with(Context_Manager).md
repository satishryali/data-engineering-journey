# using with (Automatic Cleanup)

Source-note correction, 15 October 2026: for **psycopg2**, a connection context commits
on success and rolls back on exception; it does not close the connection. A cursor
context closes its cursor. Explicitly close the connection when finished (for example
with try/finally or an appropriate closing wrapper). The sketch below needs real
connection arguments and a database; it is not a self-contained runnable program.
This corrects source material, not an observed learner misconception; no assessment
of this concept happened during setup.
Reference: https://www.psycopg.org/docs/usage.html#with-statement

- with statement is called a context manager
- It will something like
- A context manager runs its defined exit behaviour even when the body raises an exception. The resource-specific manager decides whether this closes a resource, commits/rolls back a transaction, or performs another action.
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
