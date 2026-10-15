-- create table customers (
--     customer_id int,
--     name varchar(20)
-- );
-- create table orders (
--     order_id int,
--     customer_id int
-- );
-- insert into customers values(1, 'Asha'), (2, 'Ravi'), (3, 'Meera');
-- insert into orders values (101, 1), (102, 1), (103, 2);
-- insert into orders values(104,3);
alter table orders
add COLUMN amount int;

insert into
    orders
values
    (105, 1);

select
    *
from
    orders;

insert into
    orders (amount)
select
    val
from
    (
        values
            (500),
            (200),
            (300)
        where
            not exists (
                select
                    1
                from
                    orders
                where
                    customer_id = 1
            )
    );

INSERT INTO
    orders (amount)
SELECT
    val
FROM
    (
        VALUES
            (500),
            (200),
            (300)
    ) AS t (val)
WHERE
    NOT EXISTS (
        SELECT
            1
        FROM
            orders
        WHERE
            customer_id = 1
    );

insert into
    customers
values
    (5, 'Asha');

select
    c.name,
    count(o.order_id)
from
    customers c
    left join orders o on c.customer_id = o.customer_id
group by
    c.name;

select
    c.name,
    count(o.order_id)
from
    customers c
    left join orders o on c.customer_id = o.customer_id
group by
    c.customer_id,
    c.name;

select
    c.name,
    sum(o.order_id)
from
    customers c
    left join orders o on c.customer_id = o.customer_id
group by
    c.customer_id,
    c.name;

-- insert into customers values(4,'Nila');
-- select * from orders;
-- select * from customers;
-- delete from customers where customer_id = 4;