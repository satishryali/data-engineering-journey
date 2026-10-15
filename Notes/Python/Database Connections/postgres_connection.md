# Postgres Connection

### Install the PostgreSQL Driver

```python
pip install psycopg2-binary
```

- psycopg2-binary : it comes pre-packaged with all required PostgreSQL C-libraries.

### Import psycopg2

- import psycopg2 for using it in the file.

### Define Connection Parameters

- To connect to any database, PostgreSQL needs 5 pieces of information
- host : hostname
- port : portnumber
- dbname : database_name
- user : username
- password : database_password

### Open the connection

- We have to call the psycopg2.connect()

```python
conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=db_password
)
```

- conn is active connection tunnel between python and your postgreSQL Server

### Create a cursor

- In postgreSQL, you don't run SQL Queries directly on the connection. So we have to create a cursor

```python
cur = conn.cursor()
```

- Cursor is like a mouse pointer/ command line inside the database. It is the tool that sends SQL commands to the server and retrives the results

### Execute a Query and Fetch Results

- For executing the query in the database we are having multiple functions
    - cur.fetchone()
    - cur.fetchall()

```python
# Run a simple test query to verify connection
cur.execute("SELECT version();")

# Fetch the result
db_version = cur.fetchone()
print(f"Connected to: {db_version[0]}")
```

### Close the connection

- cur.close()
- conn.close()

### Best Practice

- use with (Automatic cleanup) [[with(Context_Manager)]]
