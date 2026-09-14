
CREATE DATABASE employee_assignment;
go
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(100) NOT NULL,
    emp_age INT NOT NULL,
    emp_department VARCHAR(50) NOT NULL,
    emp_salary DECIMAL(10, 2) NULL,
    emp_city VARCHAR(50) NOT NULL
);

-- TASK 1: Insert 10 employees.
INSERT INTO employees
    (emp_id, emp_name, emp_age, emp_department, emp_salary, emp_city)
VALUES
    (1, 'Amit',   28, 'IT',      70000.00, 'Lucknow'),
    (2, 'Anita',  26, 'IT',      65000.00, 'Lucknow'),
    (3, 'Rahul',  24, 'IT',      45000.00, 'Delhi'),
    (4, 'Priya',  30, 'IT',      80000.00, 'Lucknow'),
    (5, 'Akash',  27, 'IT',      60000.00, 'Mumbai'),
    (6, 'Neha',   29, 'IT',      75000.00, 'Delhi'),
    (7, 'Pooja',  32, 'HR',      55000.00, 'Lucknow'),
    (8, 'Rohit',  23, 'HR',          NULL, 'Delhi'),
    (9, 'Karan',  35, 'Finance', 50000.00, 'Mumbai'),
    (10,'Vikas',  22, 'Finance', 35000.00, 'Pune');

-- TASK 2: Display all employees (10 rows at this point).
SELECT * FROM employees;

-- TASK 3: Update the salary of one employee.
UPDATE employees SET emp_salary = 72000.00 WHERE emp_id = 1;

-- TASK 4: Change one employee's city.
UPDATE employees SET emp_city = 'Lucknow' WHERE emp_id = 5;

-- TASK 5: Delete one employee (9 rows remain).
DELETE FROM employees WHERE emp_id = 10;

-- SECTION A: Filtering

-- A1. Employees earning more than 50,000.
SELECT * FROM employees WHERE emp_salary > 50000;

-- A2. Employees from IT.
SELECT * FROM employees WHERE emp_department = 'IT';

-- A3. Employees from Lucknow.
SELECT * FROM employees WHERE emp_city = 'Lucknow';

-- A4. Employees earning between 40,000 and 60,000.
SELECT * FROM employees WHERE emp_salary BETWEEN 40000 AND 60000;

-- A5. Employees whose name starts with A.
SELECT * FROM employees WHERE emp_name LIKE 'A%';

-- A6. Employees whose name ends with a.
SELECT * FROM employees WHERE emp_name LIKE '%a';

-- A7. Employees belonging to IT or HR.
SELECT * FROM employees WHERE emp_department IN ('IT', 'HR');

-- A8. Employees older than 25 and earning more than 50,000.
SELECT * FROM employees WHERE emp_age > 25 AND emp_salary > 50000;

-- A9. Employees whose salary is NULL.
SELECT * FROM employees WHERE emp_salary IS NULL;

-- A10. Employees whose salary is not NULL.
SELECT * FROM employees WHERE emp_salary IS NOT NULL;

-- SECTION B: Sorting and grouping

-- B1. Sort employees by salary (ascending).
SELECT * FROM employees ORDER BY emp_salary ASC;

-- B2. Sort employees from highest salary to lowest.
SELECT * FROM employees ORDER BY emp_salary DESC;

-- B3. Count employees in every department.
SELECT emp_department, COUNT(*) AS employee_count
FROM employees GROUP BY emp_department;

-- B4. Average salary per department.
SELECT emp_department, AVG(emp_salary) AS average_salary
FROM employees GROUP BY emp_department;

-- B5. Maximum salary per department.
SELECT emp_department, MAX(emp_salary) AS maximum_salary
FROM employees GROUP BY emp_department;

-- B6. Departments having more than 5 employees.
SELECT emp_department, COUNT(*) AS employee_count
FROM employees GROUP BY emp_department HAVING COUNT(*) > 5;

-- B7. Departments whose average salary is greater than 60,000.
SELECT emp_department, AVG(emp_salary) AS average_salary
FROM employees GROUP BY emp_department HAVING AVG(emp_salary) > 60000;

-- B8. Sort departments by average salary (ascending).
SELECT emp_department, AVG(emp_salary) AS average_salary
FROM employees GROUP BY emp_department ORDER BY average_salary ASC;

-- B9. Number of employees in every city.
SELECT emp_city, COUNT(*) AS employee_count
FROM employees GROUP BY emp_city;

-- B10. Cities having more than 3 employees.
SELECT emp_city, COUNT(*) AS employee_count
FROM employees GROUP BY emp_city HAVING COUNT(*) > 3;

-- SECTION C: Aggregate functions

-- C1. Total employees.
SELECT COUNT(*) AS total_employees FROM employees;

-- C2. Total salary.
SELECT SUM(emp_salary) AS total_salary FROM employees;

-- C3. Average salary.
SELECT AVG(emp_salary) AS average_salary FROM employees;

-- C4. Maximum salary.
SELECT MAX(emp_salary) AS maximum_salary FROM employees;

-- C5. Minimum salary.
SELECT MIN(emp_salary) AS minimum_salary FROM employees;

-- C6. Average salary of IT employees.
SELECT AVG(emp_salary) AS it_average_salary
FROM employees WHERE emp_department = 'IT';

-- C7. Highest salary in HR.
SELECT MAX(emp_salary) AS hr_highest_salary
FROM employees WHERE emp_department = 'HR';

-- C8. Total salary paid to Finance employees.
SELECT SUM(emp_salary) AS finance_total_salary
FROM employees WHERE emp_department = 'Finance';

-- C9. Number of employees in Delhi.
SELECT COUNT(*) AS delhi_employee_count
FROM employees WHERE emp_city = 'Delhi';

-- C10. Average salary of employees earning more than 50,000.
SELECT AVG(emp_salary) AS average_salary_above_50000
FROM employees WHERE emp_salary > 50000;

-- C11. Department-wise total salary.
SELECT emp_department, SUM(emp_salary) AS total_salary
FROM employees GROUP BY emp_department;

-- C12. Department-wise average salary.
SELECT emp_department, AVG(emp_salary) AS average_salary
FROM employees GROUP BY emp_department;

-- C13. Department with the highest average salary (includes ties).
SELECT emp_department, AVG(emp_salary) AS average_salary
FROM employees
GROUP BY emp_department
HAVING AVG(emp_salary) = (
    SELECT MAX(department_average)
    FROM (
        SELECT AVG(emp_salary) AS department_average
        FROM employees GROUP BY emp_department
    ) AS department_averages
);

-- C14. Department with the highest total salary (includes ties).
SELECT emp_department, SUM(emp_salary) AS total_salary
FROM employees
GROUP BY emp_department
HAVING SUM(emp_salary) = (
    SELECT MAX(department_total)
    FROM (
        SELECT SUM(emp_salary) AS department_total
        FROM employees GROUP BY emp_department
    ) AS department_totals
);

-- C15. City-wise employee count.
SELECT emp_city, COUNT(*) AS employee_count
FROM employees GROUP BY emp_city;

