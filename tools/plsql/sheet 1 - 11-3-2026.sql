-- CREATE TABLE employees_practice (
--     employee_id   NUMBER PRIMARY KEY,
--     employee_name VARCHAR2(50),
--     department    VARCHAR2(30),
--     salary        NUMBER
-- );

-- INSERT ALL
--     INTO employees_practice VALUES (101, 'Ravi',  'IT',      45000)
--     INTO employees_practice VALUES (102, 'Priya', 'Finance', 55000)
--     INTO employees_practice VALUES (103, 'Arun',  'IT',      60000)
--     INTO employees_practice VALUES (104, 'Neha',  NULL,      50000)
--     INTO employees_practice VALUES (105, 'Kiran', 'HR',      48000)
-- SELECT 1 FROM dual;

-- COMMIT;

select * from employees_practice where department <> 'IT' or department is null;


select 
count(case when salary >= 60000 then 1 else 0 end ) as high_salary_count,
count(case when salary < 60000 or salary is null then 1 end) as other_salary_count
from EMPLOYEES_PRACTICE;


select sum(case when SALARY >= 60000 then 1 end) as high_salary_count from EMPLOYEES_PRACTICE;

select sum(case when department = 'IT' then salary end) as it_total_salary from EMPLOYEES_PRACTICE;

select department, 
sum(case when department )