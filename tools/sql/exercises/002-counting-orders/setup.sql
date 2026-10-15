-- Use once in a fresh PostgreSQL connection, not over existing temporary tables.
CREATE TEMP TABLE customers (customer_id integer PRIMARY KEY, name text NOT NULL);
CREATE TEMP TABLE orders (order_id integer PRIMARY KEY, customer_id integer REFERENCES customers(customer_id));
INSERT INTO customers VALUES (1, 'Asha'), (2, 'Ravi'), (3, 'Meera'), (4, 'Nila');
INSERT INTO orders VALUES (101, 1), (102, 1), (103, 2), (104, 3);
