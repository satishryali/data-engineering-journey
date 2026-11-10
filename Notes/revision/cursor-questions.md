# Cursor recall questions

Try one task without opening the explanation. State which database you use and
whether you used notes or hints. These are pending prompts, not completed reviews.

1. A PostgreSQL cursor reads five ordered rows. Predict the rows returned by
   `FETCH FORWARD 2`, another `FETCH FORWARD 2`, then two `FETCH NEXT` calls.
   Write a small runnable example and compare the actual output.
2. A PostgreSQL script declares a normal cursor, commits, then tries to fetch.
   Explain the problem and rewrite the sequence so it can read two batches.
3. In Oracle PL/SQL, write a cursor FOR loop over three synthetic orders and
   explain who opens, fetches and closes the cursor. Compare it with a manual loop.
4. Explain whether calling `fetchmany(100)` on an unnamed psycopg2 cursor alone
   proves that the server sends only 100 rows to the client at a time.
