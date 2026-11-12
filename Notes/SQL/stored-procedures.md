# SQL stored procedures

## Why we need them

A stored procedure keeps a named set of steps inside the database. We can call
it again with different inputs instead of copying the same SQL into every script.
For example, one procedure can check an order and change its status.

Creating a procedure saves its definition. Its body runs when we call it.
Procedures are useful for repeated database work; a single query is still enough
when the work only needs one simple statement.

PostgreSQL uses PL/pgSQL in the examples below. Oracle uses PL/SQL. These languages
add variables, conditions and error handling to SQL, but their syntax differs.
Run each example only in the database named above it.

## PostgreSQL: small input

Use a practice database and keep the examples in one connection. These names are
only for this note; they do not use the active project tables.

```sql
CREATE TEMP TABLE procedure_orders_demo (
    order_id integer PRIMARY KEY,
    status text NOT NULL
);

INSERT INTO procedure_orders_demo (order_id, status)
VALUES (101, 'pending'), (102, 'pending');
```

**Expected rows**

| order_id | status |
| ---: | --- |
| 101 | pending |
| 102 | pending |

The temporary table belongs to this connection and disappears when it ends.
The procedure created next is a stored object; remove it with the cleanup command.

## PostgreSQL: create and call

```sql
CREATE OR REPLACE PROCEDURE complete_order_demo(IN p_order_id integer)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE procedure_orders_demo
    SET status = 'completed'
    WHERE order_id = p_order_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Order % does not exist', p_order_id;
    END IF;
END;
$$;

CALL complete_order_demo(101);

SELECT order_id, status
FROM procedure_orders_demo
ORDER BY order_id;
```

**Expected output from SELECT**

| order_id | status |
| ---: | --- |
| 101 | completed |
| 102 | pending |

- `CREATE OR REPLACE` creates the procedure or replaces the same definition.
- `IN p_order_id integer` takes an integer input. The `p_` prefix helps us
  distinguish the parameter from the table's `order_id` column.
- `LANGUAGE plpgsql` chooses the language used for the body.
- `$$` surrounds the body text; it is not a transaction command.
- `BEGIN ... END` groups the steps inside the body.
- `CALL` runs the procedure. It does not automatically show the changed table.
- `FOUND` is true if the `UPDATE` affected a row. It refers to the most recent
  statement that sets it, so check it before another such statement changes it.

Try the following call separately:

```sql
CALL complete_order_demo(999);
```

**Expected error:** `Order 999 does not exist`. No matching row is changed.
If this error occurs inside an explicit transaction, use `ROLLBACK` before
continuing. The error is deliberate reference behaviour, not a learner mistake.

Avoid `WHERE order_id = order_id`: it does not compare the column with the input
and may update every row. Use clearly different parameter and column names.

## PostgreSQL: IN, OUT and INOUT

A parameter is a named value passed into or out of the procedure.

| Mode | Purpose |
| --- | --- |
| `IN` | Take an input; this is the default when the mode is omitted |
| `OUT` | Send a value back to the caller |
| `INOUT` | Take a value and send its changed value back |

This example has no table dependency:

```sql
CREATE OR REPLACE PROCEDURE add_fee_demo(
    IN p_fee numeric,
    INOUT p_total numeric
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_fee IS NULL OR p_total IS NULL OR p_fee < 0 THEN
        RAISE EXCEPTION 'Provide a total and a nonnegative fee';
    END IF;

    p_total := p_total + p_fee;
END;
$$;

CALL add_fee_demo(25, 200);
```

**Expected result row:** `p_total = 225`. `:=` assigns a new value to a variable.
An output parameter can return a result even though the procedure has no
`RETURNS` clause. `RETURN;` can exit a PL/pgSQL procedure early; use output
parameters to send values back rather than `RETURN 225;`.

An `OUT` parameter starts without an input value. In PostgreSQL 14 and later:

```sql
CREATE OR REPLACE PROCEDURE double_amount_demo(
    IN p_amount numeric,
    OUT p_result numeric
)
LANGUAGE plpgsql
AS $$
BEGIN
    p_result := p_amount * 2;
END;
$$;

CALL double_amount_demo(100, NULL);
```

**Expected result row:** `p_result = 200`. In a plain SQL `CALL`, supply the
`NULL` placeholder for this required output argument. Calling from a PL/pgSQL
block instead requires a variable to receive the output. Older PostgreSQL
versions may need `INOUT` instead of `OUT` for procedures.

## PostgreSQL: transactions

A transaction groups changes so they can be saved together with `COMMIT` or
undone with `ROLLBACK`. The order procedure leaves that choice to its caller.

After the successful call for order 101 above, run:

```sql
BEGIN;
CALL complete_order_demo(102);
ROLLBACK;

SELECT order_id, status
FROM procedure_orders_demo
ORDER BY order_id;
```

**Expected rows:** order 101 is `completed`; order 102 is still `pending`.
The update for order 102 was undone.

- PL/pgSQL `BEGIN ... END` groups code. SQL `BEGIN;` starts a transaction.
- A procedure does not need its own `COMMIT`. Keeping the caller in control
  lets several calls succeed or roll back together.
- PostgreSQL allows transaction control inside procedures only in allowed call
  contexts. A procedure called within an explicit transaction block cannot
  execute its own `COMMIT` or `ROLLBACK`.
- Top-level `CALL` and suitable nested calls can allow transaction control.
  An intervening function call, an exception-handler block, `SECURITY DEFINER`,
  or a procedure-level `SET` clause can restrict it further. Check the linked
  documentation before adding internal commits.
- In autocommit mode, a successful standalone call is committed by its surrounding
  transaction. That does not mean every procedure contains a commit statement.

## Procedure, function and cursor

| Item | Main purpose | PostgreSQL example |
| --- | --- | --- |
| Procedure | Run a named set of database steps | `CALL complete_order_demo(101);` |
| Function | Produce a value or rows usable in a query | `SELECT upper('pending');` |
| Cursor | Keep a position while reading query results | `FETCH NEXT FROM order_cursor;` |

A PostgreSQL function has a declared return type and cannot commit or roll back
the caller's transaction. Functions can also change data; they are not always
read-only. Procedures can send values through output parameters, but cannot be
used as expressions in `SELECT` like functions.

A cursor is not a procedure. A procedure may use one when row-by-row work is
needed. For updating all matching rows, prefer one `UPDATE` where possible.
See [SQL cursors](cursors.md) for separate cursor examples.

## Oracle: create and call

Run this as a script in SQL*Plus or SQLcl. `SET SERVEROUTPUT ON` enables printed
messages. `/` submits the preceding PL/SQL definition or block in these tools;
it is a client command, not part of the stored procedure body.

```sql
SET SERVEROUTPUT ON

CREATE OR REPLACE PROCEDURE add_fee_demo (
    p_fee IN NUMBER,
    p_total IN OUT NUMBER
)
AS
BEGIN
    IF p_fee IS NULL OR p_total IS NULL OR p_fee < 0 THEN
        RAISE_APPLICATION_ERROR(-20001, 'Provide a total and a nonnegative fee');
    END IF;

    p_total := p_total + p_fee;
END;
/

DECLARE
    v_total NUMBER := 200;
BEGIN
    add_fee_demo(25, v_total);
    DBMS_OUTPUT.PUT_LINE('Total: ' || v_total);
END;
/
```

**Expected printed output:** `Total: 225`.

- Oracle writes `p_fee IN NUMBER`; PostgreSQL writes `IN p_fee numeric`.
- Oracle uses `IN OUT` as two words. Supply a variable such as `v_total` so the
  caller can receive the changed value.
- The anonymous block calls the procedure directly by name. `DBMS_OUTPUT`
  prints a message; an output parameter passes a value back to calling code.
- `RAISE_APPLICATION_ERROR` raises an application error; `-20001` is within
  Oracle's application-error range of `-20000` to `-20999`.
- An ordinary Oracle procedure can commit or roll back, but that also affects
  the caller's current transaction. Choose who owns the transaction deliberately.
  Oracle DDL, including `CREATE PROCEDURE`, can implicitly commit; do not wrap
  procedure creation in a transaction expecting `ROLLBACK` to remove it.

## Change, remove and permissions

`CREATE OR REPLACE` can update a PostgreSQL procedure's body, but does not
rename it or change its input argument types in place. A different input
signature can create another procedure with the same name. Use explicit types
when removing the intended definition.

After practising, remove the PostgreSQL examples:

```sql
DROP PROCEDURE complete_order_demo(integer);
DROP PROCEDURE add_fee_demo(numeric, numeric);
DROP PROCEDURE double_amount_demo(numeric);
DROP TABLE procedure_orders_demo;
```

The last procedure's identity uses its input argument; its `OUT` argument does
not distinguish it from another definition. In Oracle, remove that example with:

```sql
DROP PROCEDURE add_fee_demo;
```

Creating procedures requires the relevant database/schema permissions. Calling
them requires `EXECUTE`; do not assume a caller has access just because creation
succeeded under a different account. PostgreSQL defaults to the caller's
privileges (`SECURITY INVOKER`); Oracle defaults to the owner's privileges
(`AUTHID DEFINER`). Grant access deliberately for shared databases.

## Sources and practice

- [PostgreSQL: CREATE PROCEDURE](https://www.postgresql.org/docs/current/sql-createprocedure.html)
- [PostgreSQL: CALL and output arguments](https://www.postgresql.org/docs/current/sql-call.html)
- [PostgreSQL: transaction management](https://www.postgresql.org/docs/current/plpgsql-transactions.html)
- [PostgreSQL: DROP PROCEDURE](https://www.postgresql.org/docs/current/sql-dropprocedure.html)
- [Oracle 19c: CREATE PROCEDURE](https://docs.oracle.com/en/database/oracle/oracle-database/19/lnpls/CREATE-PROCEDURE-statement.html)
- [Separate recall tasks](../revision/procedure-questions.md)

Prepared as a requested reference on 12 November 2026 IST. Examples show expected
output; they were not executed against a live PostgreSQL or Oracle database.
No learner attempt, assessment, review completion or study time is implied.
