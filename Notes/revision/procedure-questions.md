# Stored procedure recall questions

Try one task before opening the explanation. State the database/version and any
notes, hints or other help used. These unanswered prompts are not review results.

1. In PostgreSQL, create three synthetic orders in a practice table. Write a
   procedure that cancels only the order ID passed to it and raises an error for
   a missing order. Predict the rows, call it for one existing ID, then compare
   your actual query output. Explain the parameter name and WHERE condition.
2. Write a PostgreSQL procedure with a fee input and an INOUT total. Use different
   values from the reference, predict the returned total, and show actual output.
   Explain how this differs from printing a message.
3. Call a procedure that updates a row inside BEGIN/ROLLBACK. Show the row before
   and after. Explain why adding COMMIT inside that procedure would fail in this
   call context, and who should decide whether to save the changes.
4. In Oracle, write a procedure that changes an IN OUT amount and call it from
   an anonymous block. Show actual output and explain why the caller uses a variable.
5. Explain when you would choose a procedure, function or cursor for an order
   task. Include how you invoke each in PostgreSQL and whether each can be used
   as a value in a SELECT expression.
