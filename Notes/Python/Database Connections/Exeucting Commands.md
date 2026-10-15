# Execution of Commands in Postgres

- Open a cursor using the connection
```python
cur.execute("select * from customers")
```

- Note : execute command only runs the query through the establishment connection, it returs None.
-
