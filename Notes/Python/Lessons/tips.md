# Tips to follow when creating dbt models,transformations or anything

- In dbt we are calling raw reference files as `seeds`.
- Use text, because it helps us to reduce errors while loading the data. because some files may contain dirty values (extra spaces, invalid dates, empty strings). Text datatype will prevents the database from crashing during the load.

# Interesting Topics

- if python file is executing directly as we can see that


- use [[with(Context_Manager)]] whenever you are opening and closing the connections.
- use [[Logging.md]] logging for the logging.
- use [[Hashicorp_vault.md]] for storing the secrets.

# Path :
- If you have to use the path, the use this command
- Path(__file__) to start working on the path, this command will give you the path of the current file you are working on, from there on you can move to any file you want.
