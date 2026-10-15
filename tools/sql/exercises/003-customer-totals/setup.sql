-- New temporary sample tables; run once in a fresh/suitable connection.
CREATE TEMP TABLE revenue_customers (customer_id integer PRIMARY KEY, name text NOT NULL);
CREATE TEMP TABLE revenue_orders (order_id integer PRIMARY KEY, customer_id integer REFERENCES revenue_customers(customer_id), amount numeric(10,2) NOT NULL);
INSERT INTO revenue_customers VALUES (1, 'Asha'), (2, 'Ravi'), (3, 'Meera'), (4, 'Nila'), (5, 'Asha');
INSERT INTO revenue_orders VALUES (101, 1, 500), (102, 1, 200), (103, 2, 400), (104, 3, 150), (105, 1, 300);
