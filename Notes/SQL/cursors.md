# SQL cursors

## Why we need them

A normal SQL query works with a group of rows. A cursor lets us keep a position
in its result and read the next row or batch when needed. A batch is a small
group of rows, such as 100 orders at a time.

This can help when an application needs to read a large result in parts or when
a stored program needs different processing for each row. First check whether
one `SELECT`, `JOIN`, `UPDATE` or aggregate can do the job without a row loop.

Cursor syntax differs between databases. Use each example only in the database
named above it; PostgreSQL SQL commands and Oracle PL/SQL are not interchangeable.

## Small input

We will read these orders in order of ID:

| order_id | customer_name |
| ---: | --- |
| 101 | Asha |
| 102 | Ravi |
| 103 | Nila |

The examples define these rows inside the query. No permanent table is needed.

## PostgreSQL: fetch rows in parts

Run the complete block in one database session, such as one query-tool connection:

```sql
BEGIN;

DECLARE order_cursor NO SCROLL CURSOR FOR
    SELECT order_id, customer_name
    FROM (VALUES
        (101, 'Asha'),
        (102, 'Ravi'),
        (103, 'Nila')
    ) AS orders(order_id, customer_name)
    ORDER BY order_id;

FETCH NEXT FROM order_cursor;
FETCH FORWARD 2 FROM order_cursor;
FETCH NEXT FROM order_cursor;

CLOSE order_cursor;
COMMIT;
```

**Expected output from the fetches**

| Statement | Rows returned |
| --- | --- |
| First `FETCH NEXT` | 101 / Asha |
| `FETCH FORWARD 2` | 102 / Ravi; 103 / Nila |
| Last `FETCH NEXT` | Zero rows: the result has ended |

The query tool may show each result in a separate grid.

- `BEGIN` starts a transaction: a group of database work ended by `COMMIT` or `ROLLBACK`.
- `DECLARE ... CURSOR FOR` defines and opens the SQL cursor in PostgreSQL.
  There is no separate SQL `OPEN` command here.
- The position starts before the first row. `FETCH NEXT` reads and moves to the next row.
- A later fetch continues from the current position; it does not restart the query.
- `NO SCROLL` allows forward reading. `ORDER BY` gives this example a predictable order.
- `CLOSE` releases the cursor. It does not close the database connection.

## PostgreSQL: other fetch choices

Use these while the cursor is still open:

| Command | Meaning |
| --- | --- |
| `FETCH NEXT FROM order_cursor;` | Read one next row |
| `FETCH FORWARD 100 FROM order_cursor;` | Read up to 100 next rows |
| `FETCH ALL FROM order_cursor;` | Read all remaining rows |

`FETCH ALL` does not mean all rows from the beginning. Already fetched rows are
not returned again by forward reading. A batch can contain fewer rows than
requested. Fetching after the end returns an empty result, not a row of NULLs.

If you need to move backwards, declare a suitable query with `SCROLL` instead
of `NO SCROLL`. For example, `FETCH PRIOR FROM order_cursor;` reads the previous
row on a scrollable cursor. Do not assume every cursor supports backward movement.

## PostgreSQL: transaction and memory checks

- A normal cursor must be declared inside a transaction. It closes when that
  transaction ends, including at `COMMIT` or `ROLLBACK`.
- Keep `DECLARE` and the fetches in the same connection. A second query-tool
  connection cannot fetch the first connection's cursor.
- `WITH HOLD` can keep a cursor available after a successful commit, in the
  same session. PostgreSQL may store its rows in memory or temporary files.
  It is not a way to resume after disconnecting.
- Small fetches limit the rows delivered per call. They do not guarantee that
  the database uses little memory: sorting, joins and stored results can still
  require memory or temporary disk space.
- If a command fails inside the transaction, use `ROLLBACK` before starting again.

## Oracle: explicit cursor with a loop

PL/SQL is Oracle's language for blocks with variables, conditions and loops.
An explicit cursor is one we name and define ourselves.

Run this as a script in SQL*Plus or SQLcl. `SET SERVEROUTPUT ON` enables the
printed messages; `/` runs the PL/SQL block in these tools.

```sql
SET SERVEROUTPUT ON

DECLARE
    CURSOR order_cursor IS
        SELECT 101 AS order_id, 'Asha' AS customer_name FROM dual
        UNION ALL
        SELECT 102, 'Ravi' FROM dual
        UNION ALL
        SELECT 103, 'Nila' FROM dual
        ORDER BY order_id;
    order_row order_cursor%ROWTYPE;
BEGIN
    OPEN order_cursor;
    LOOP
        FETCH order_cursor INTO order_row;
        EXIT WHEN order_cursor%NOTFOUND;
        DBMS_OUTPUT.PUT_LINE(order_row.order_id || ' / ' || order_row.customer_name);
    END LOOP;
    CLOSE order_cursor;
END;
/
```

**Expected printed output**

```text
101 / Asha
102 / Ravi
103 / Nila
```

`dual` lets this Oracle example select literal values without a real orders table.
`%ROWTYPE` makes a record with the cursor's columns. `OPEN` prepares the result;
`FETCH ... INTO` reads the next row into that record. Check `%NOTFOUND` directly
after fetching, before processing. Otherwise the loop may process values even
though that fetch did not return a row. `||` joins text for display.

## Oracle: shorter cursor FOR loop

This alternative manages opening, fetching and closing for us:

```sql
SET SERVEROUTPUT ON

DECLARE
    CURSOR order_cursor IS
        SELECT 101 AS order_id, 'Asha' AS customer_name FROM dual
        UNION ALL
        SELECT 102, 'Ravi' FROM dual
        UNION ALL
        SELECT 103, 'Nila' FROM dual
        ORDER BY order_id;
BEGIN
    FOR order_row IN order_cursor LOOP
        DBMS_OUTPUT.PUT_LINE(order_row.order_id || ' / ' || order_row.customer_name);
    END LOOP;
END;
/
```

**Expected output:** the same three printed lines as the manual loop.

Do not manually open this cursor before entering its `FOR` loop. The loop creates
its own row record, fetches each row, and closes the cursor on completion or an
exception. The row record is available inside the loop only.

## SQL cursor versus Python cursor

With psycopg2, `conn.cursor()` creates a Python object used to execute commands
and fetch results. It is not automatically a PostgreSQL server-side cursor.
An unnamed psycopg2 cursor normally transfers the query result to the client;
calling `fetchmany()` alone does not turn it into server-side streaming.
Named cursors, such as `conn.cursor(name='order_reader')`, provide server-side
cursor behaviour. See the existing [connection notes](../Python/Database%20Connections/postgres_connection.md)
for the Python API.

## Remember

- A cursor keeps a position in a query result; it is not a new permanent table.
- Fetching reads rows. It does not update them or commit changes.
- Prefer a single SQL operation when it expresses the whole task clearly.
- Use explicit ordering when the processing order matters.
- Close cursors when finished. Avoid holding transactions open during long breaks.

## References and practice

Prepared reference only. Examples were checked against documentation, not executed
against a live database. No learner attempt or independent assessment is recorded.
Try the separate [cursor recall questions](../revision/cursor-questions.md).

- [PostgreSQL DECLARE](https://www.postgresql.org/docs/current/sql-declare.html)
- [PostgreSQL FETCH](https://www.postgresql.org/docs/current/sql-fetch.html)
- [PostgreSQL CLOSE](https://www.postgresql.org/docs/current/sql-close.html)
- [Oracle explicit cursor](https://docs.oracle.com/en/database/oracle/oracle-database/19/lnpls/explicit-cursor-declaration-and-definition.html)
- [Oracle cursor FOR loop](https://docs.oracle.com/en/database/oracle/oracle-database/19/lnpls/cursor-FOR-LOOP-statement.html)
- [Psycopg2 server-side cursors](https://www.psycopg.org/docs/usage.html#server-side-cursors)
