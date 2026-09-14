
CREATE DATABASE BankingAssignment;
GO

USE BankingAssignment;
GO


-- TABLE 1: Customers
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    status VARCHAR(10) NOT NULL
        CHECK (status IN ('Active', 'Inactive'))
);


-- TABLE 2: Branches
CREATE TABLE branches (
    branch_id INT PRIMARY KEY,
    branch_name VARCHAR(100) NOT NULL,
    branch_city VARCHAR(50) NOT NULL
);


-- TABLE 3: Accounts
CREATE TABLE accounts (
    account_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    branch_id INT NOT NULL,
    account_type VARCHAR(20) NOT NULL
        CHECK (account_type IN ('Savings', 'Current')),
    balance DECIMAL(15, 2) NOT NULL
        CHECK (balance >= 0),

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    FOREIGN KEY (branch_id)
        REFERENCES branches(branch_id)
);


-- TABLE 4: Transactions
CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY,
    account_id INT NOT NULL,
    amount DECIMAL(15, 2) NOT NULL
        CHECK (amount > 0),
    mode VARCHAR(20) NOT NULL
        CHECK (mode IN ('ATM', 'UPI', 'NEFT', 'Cash')),
    transaction_date DATE NOT NULL,

    FOREIGN KEY (account_id)
        REFERENCES accounts(account_id)
);


-- TABLE 5: Cards
CREATE TABLE cards (
    card_id INT PRIMARY KEY,
    account_id INT NOT NULL,
    card_type VARCHAR(20) NOT NULL
        CHECK (card_type IN ('Debit', 'Credit')),

    FOREIGN KEY (account_id)
        REFERENCES accounts(account_id)
);


/* =====================================================
   PART 2: INSERT SAMPLE DATA
   ===================================================== */


-- Insert 10 customers.
INSERT INTO customers
    (customer_id, customer_name, city, status)
VALUES
    (1,  'Amit Sharma',  'Delhi',   'Active'),
    (2,  'Priya Verma',  'Lucknow', 'Active'),
    (3,  'Rahul Singh',  'Mumbai',  'Inactive'),
    (4,  'Neha Gupta',   'Delhi',   'Active'),
    (5,  'Akash Yadav',  'Lucknow', 'Active'),
    (6,  'Pooja Mishra', 'Mumbai',  'Active'),
    (7,  'Rohit Kumar',  'Delhi',   'Inactive'),
    (8,  'Anita Patel',  'Lucknow', 'Active'),
    (9,  'Karan Mehta',  'Mumbai',  'Active'),
    (10, 'Simran Kaur',  'Delhi',   'Active');


-- Insert 3 branches.
INSERT INTO branches
    (branch_id, branch_name, branch_city)
VALUES
    (101, 'Delhi Central',  'Delhi'),
    (102, 'Lucknow Gomti',  'Lucknow'),
    (103, 'Mumbai Andheri', 'Mumbai');


-- Insert 15 accounts.
INSERT INTO accounts
    (account_id, customer_id, branch_id, account_type, balance)
VALUES
    (1001, 1, 101, 'Savings', 150000.00),
    (1002, 1, 101, 'Current',  50000.00),
    (1003, 2, 102, 'Savings', 120000.00),
    (1004, 3, 103, 'Savings',  40000.00),
    (1005, 4, 101, 'Savings', 250000.00),
    (1006, 5, 102, 'Current', 180000.00),
    (1007, 6, 103, 'Savings', 300000.00),
    (1008, 7, 101, 'Savings',  20000.00),
    (1009, 8, 102, 'Savings',  75000.00),
    (1010, 9, 103, 'Current', 200000.00),
    (1011, 2, 102, 'Current',  80000.00),
    (1012, 4, 101, 'Current',  50000.00),
    (1013, 6, 103, 'Current', 100000.00),
    (1014, 8, 102, 'Current',  25000.00),
    (1015, 1, 103, 'Savings',  60000.00);


-- Insert 24 transactions.
-- Balances are independent sample snapshots.
-- These inserts do not update account balances.
INSERT INTO transactions
    (transaction_id, account_id, amount, mode, transaction_date)
VALUES
    (1,  1001,  10000.00, 'ATM',  '20260801'),
    (2,  1001,   5000.00, 'UPI',  '20260802'),
    (3,  1002,  25000.00, 'NEFT', '20260803'),
    (4,  1003,  15000.00, 'UPI',  '20260804'),
    (5,  1003,   5000.00, 'ATM',  '20260805'),
    (6,  1004,   2000.00, 'ATM',  '20260806'),
    (7,  1005,  50000.00, 'NEFT', '20260807'),
    (8,  1005,  10000.00, 'UPI',  '20260808'),
    (9,  1006,  30000.00, 'Cash', '20260809'),
    (10, 1006,   5000.00, 'ATM',  '20260810'),
    (11, 1007, 100000.00, 'NEFT', '20260811'),
    (12, 1007,  20000.00, 'UPI',  '20260812'),
    (13, 1008,   1000.00, 'ATM',  '20260813'),
    (14, 1009,   7500.00, 'UPI',  '20260814'),
    (15, 1010,  40000.00, 'NEFT', '20260815'),
    (16, 1010,  10000.00, 'Cash', '20260816'),
    (17, 1011,  20000.00, 'NEFT', '20260817'),
    (18, 1012,   5000.00, 'ATM',  '20260818'),
    (19, 1013,  50000.00, 'Cash', '20260819'),
    (20, 1014,   2500.00, 'UPI',  '20260820'),
    (21, 1015,  12000.00, 'UPI',  '20260821'),
    (22, 1001,  10000.00, 'Cash', '20260822'),
    (23, 1007,  20000.00, 'ATM',  '20260823'),
    (24, 1009,   3000.00, 'ATM',  '20260824');


-- Insert 8 cards.
INSERT INTO cards
    (card_id, account_id, card_type)
VALUES
    (501, 1001, 'Debit'),
    (502, 1002, 'Credit'),
    (503, 1003, 'Debit'),
    (504, 1005, 'Debit'),
    (505, 1006, 'Debit'),
    (506, 1007, 'Debit'),
    (507, 1010, 'Credit'),
    (508, 1013, 'Credit');


-- Display all five tables.
SELECT * FROM customers;
SELECT * FROM branches;
SELECT * FROM accounts;
SELECT * FROM transactions;
SELECT * FROM cards;


/* =====================================================
   PART 3: ALL QUESTIONS WITH ANSWERS

   Interpretations:
   - Customer balance = total balance across their accounts.
   - Transaction volume = number of transactions.
   - Highest transaction customer = highest total amount.
   - Branch customer balance = total within that branch.
   - Q16 and Q24 have the same interpretation.
   ===================================================== */

USE BankingAssignment;
GO


-- Q1. Find all active customers.
-- Answer:
SELECT *
FROM customers
WHERE status = 'Active';


-- Q2. Find all savings accounts.
-- Answer:
SELECT *
FROM accounts
WHERE account_type = 'Savings';


-- Q3. Find accounts with balance > Rs. 1 lakh.
-- Answer:
SELECT *
FROM accounts
WHERE balance > 100000;


-- Q4. Find all ATM transactions.
-- Answer:
SELECT *
FROM transactions
WHERE mode = 'ATM';


-- Q5. Find customers from Delhi.
-- Answer:
SELECT *
FROM customers
WHERE city = 'Delhi';


-- Q6. Total balance by branch.
-- Answer:
SELECT
    b.branch_id,
    b.branch_name,
    COALESCE(SUM(a.balance), 0) AS total_balance
FROM branches AS b
LEFT JOIN accounts AS a
    ON b.branch_id = a.branch_id
GROUP BY b.branch_id, b.branch_name;


-- Q7. Average balance by account type.
-- Answer:
SELECT
    account_type,
    AVG(balance) AS average_balance
FROM accounts
GROUP BY account_type;


-- Q8. Number of accounts per customer.
-- Answer:
SELECT
    c.customer_id,
    c.customer_name,
    COUNT(a.account_id) AS account_count
FROM customers AS c
LEFT JOIN accounts AS a
    ON c.customer_id = a.customer_id
GROUP BY c.customer_id, c.customer_name;


-- Q9. Total transaction amount per customer.
-- Answer:
SELECT
    c.customer_id,
    c.customer_name,
    COALESCE(SUM(t.amount), 0) AS total_transaction_amount
FROM customers AS c
LEFT JOIN accounts AS a
    ON c.customer_id = a.customer_id
LEFT JOIN transactions AS t
    ON a.account_id = t.account_id
GROUP BY c.customer_id, c.customer_name;


-- Q10. Total transactions by mode.
-- Answer:
SELECT
    mode,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_transaction_amount
FROM transactions
GROUP BY mode;


-- Q11. Customer + Account details.
-- Answer:
SELECT
    c.customer_id,
    c.customer_name,
    c.city,
    c.status,
    a.account_id,
    a.account_type,
    a.balance
FROM customers AS c
INNER JOIN accounts AS a
    ON c.customer_id = a.customer_id;


-- Q12. Customer + Account + Branch.
-- Answer:
SELECT
    c.customer_id,
    c.customer_name,
    a.account_id,
    a.account_type,
    a.balance,
    b.branch_id,
    b.branch_name,
    b.branch_city
FROM customers AS c
INNER JOIN accounts AS a
    ON c.customer_id = a.customer_id
INNER JOIN branches AS b
    ON a.branch_id = b.branch_id;


-- Q13. Customers having cards.
-- Answer:
SELECT c.*
FROM customers AS c
WHERE EXISTS (
    SELECT 1
    FROM accounts AS a
    INNER JOIN cards AS cd
        ON a.account_id = cd.account_id
    WHERE a.customer_id = c.customer_id
);


-- Q14. Customers without cards.
-- Answer:
SELECT c.*
FROM customers AS c
WHERE NOT EXISTS (
    SELECT 1
    FROM accounts AS a
    INNER JOIN cards AS cd
        ON a.account_id = cd.account_id
    WHERE a.customer_id = c.customer_id
);


-- Q15. Customers having multiple accounts.
-- Answer:
SELECT
    c.customer_id,
    c.customer_name,
    COUNT(a.account_id) AS account_count
FROM customers AS c
INNER JOIN accounts AS a
    ON c.customer_id = a.customer_id
GROUP BY c.customer_id, c.customer_name
HAVING COUNT(a.account_id) > 1;


-- Q16. Above-average balance customers.
-- Answer:
-- Customers without accounts count as zero balance.
;WITH customer_balances AS (
    SELECT
        c.customer_id,
        c.customer_name,
        COALESCE(SUM(a.balance), 0) AS total_balance
    FROM customers AS c
    LEFT JOIN accounts AS a
        ON c.customer_id = a.customer_id
    GROUP BY c.customer_id, c.customer_name
)
SELECT
    customer_id,
    customer_name,
    total_balance
FROM customer_balances
WHERE total_balance > (
    SELECT AVG(total_balance)
    FROM customer_balances
);


-- Q17. Second-highest balance.
-- Answer:
-- Finds the second-highest distinct ACCOUNT balance.
SELECT MAX(balance) AS second_highest_balance
FROM accounts
WHERE balance < (
    SELECT MAX(balance)
    FROM accounts
);


-- Q18. Customers above their branch average.
-- Answer:
-- Compare customer totals within each branch.
;WITH customer_branch_balances AS (
    SELECT
        customer_id,
        branch_id,
        SUM(balance) AS total_balance
    FROM accounts
    GROUP BY customer_id, branch_id
),
branch_comparison AS (
    SELECT
        customer_id,
        branch_id,
        total_balance,
        AVG(total_balance) OVER (
            PARTITION BY branch_id
        ) AS branch_average
    FROM customer_branch_balances
)
SELECT
    c.customer_id,
    c.customer_name,
    b.branch_name,
    bc.total_balance,
    bc.branch_average
FROM branch_comparison AS bc
INNER JOIN customers AS c
    ON bc.customer_id = c.customer_id
INNER JOIN branches AS b
    ON bc.branch_id = b.branch_id
WHERE bc.total_balance > bc.branch_average;


-- Q19. Highest transaction customer.
-- Answer:
-- Highest total transaction amount; includes ties.
;WITH customer_transactions AS (
    SELECT
        c.customer_id,
        c.customer_name,
        SUM(t.amount) AS total_transaction_amount
    FROM customers AS c
    INNER JOIN accounts AS a
        ON c.customer_id = a.customer_id
    INNER JOIN transactions AS t
        ON a.account_id = t.account_id
    GROUP BY c.customer_id, c.customer_name
)
SELECT
    customer_id,
    customer_name,
    total_transaction_amount
FROM customer_transactions
WHERE total_transaction_amount = (
    SELECT MAX(total_transaction_amount)
    FROM customer_transactions
);


-- Q20. Branch with highest total balance.
-- Answer:
-- Includes tied branches.
;WITH branch_balances AS (
    SELECT
        b.branch_id,
        b.branch_name,
        COALESCE(SUM(a.balance), 0) AS total_balance
    FROM branches AS b
    LEFT JOIN accounts AS a
        ON b.branch_id = a.branch_id
    GROUP BY b.branch_id, b.branch_name
)
SELECT
    branch_id,
    branch_name,
    total_balance
FROM branch_balances
WHERE total_balance = (
    SELECT MAX(total_balance)
    FROM branch_balances
);


-- Q21. Customer-wise total balance.
-- Answer:
SELECT
    c.customer_id,
    c.customer_name,
    COALESCE(SUM(a.balance), 0) AS total_balance
FROM customers AS c
LEFT JOIN accounts AS a
    ON c.customer_id = a.customer_id
GROUP BY c.customer_id, c.customer_name;


-- Q22. Customer-wise transaction volume.
-- Answer:
-- Volume is interpreted as transaction count.
SELECT
    c.customer_id,
    c.customer_name,
    COUNT(t.transaction_id) AS transaction_volume
FROM customers AS c
LEFT JOIN accounts AS a
    ON c.customer_id = a.customer_id
LEFT JOIN transactions AS t
    ON a.account_id = t.account_id
GROUP BY c.customer_id, c.customer_name;


-- Q23. Branch-wise average balance.
-- Answer:
-- Average account balance within each branch.
SELECT
    b.branch_id,
    b.branch_name,
    AVG(a.balance) AS average_balance
FROM branches AS b
LEFT JOIN accounts AS a
    ON b.branch_id = a.branch_id
GROUP BY b.branch_id, b.branch_name;


-- Q24. Above-average customers.
-- Answer:
-- Uses total customer balance, as in Question 16.
;WITH customer_balances AS (
    SELECT
        c.customer_id,
        c.customer_name,
        COALESCE(SUM(a.balance), 0) AS total_balance
    FROM customers AS c
    LEFT JOIN accounts AS a
        ON c.customer_id = a.customer_id
    GROUP BY c.customer_id, c.customer_name
)
SELECT
    customer_id,
    customer_name,
    total_balance
FROM customer_balances
WHERE total_balance > (
    SELECT AVG(total_balance)
    FROM customer_balances
);


-- Q25. Top customers per branch.
-- Answer:
-- Highest customer total in each branch; includes ties.
;WITH customer_branch_balances AS (
    SELECT
        customer_id,
        branch_id,
        SUM(balance) AS total_balance
    FROM accounts
    GROUP BY customer_id, branch_id
),
ranked_customers AS (
    SELECT
        customer_id,
        branch_id,
        total_balance,
        DENSE_RANK() OVER (
            PARTITION BY branch_id
            ORDER BY total_balance DESC
        ) AS balance_rank
    FROM customer_branch_balances
)
SELECT
    c.customer_id,
    c.customer_name,
    b.branch_name,
    r.total_balance,
    r.balance_rank
FROM ranked_customers AS r
INNER JOIN customers AS c
    ON r.customer_id = c.customer_id
INNER JOIN branches AS b
    ON r.branch_id = b.branch_id
WHERE r.balance_rank = 1
ORDER BY b.branch_id, c.customer_id;


-- Q26. Rank customers by balance.
-- Answer:
-- Equal balances receive the same rank without rank gaps.
;WITH customer_balances AS (
    SELECT
        c.customer_id,
        c.customer_name,
        COALESCE(SUM(a.balance), 0) AS total_balance
    FROM customers AS c
    LEFT JOIN accounts AS a
        ON c.customer_id = a.customer_id
    GROUP BY c.customer_id, c.customer_name
)
SELECT
    customer_id,
    customer_name,
    total_balance,
    DENSE_RANK() OVER (
        ORDER BY total_balance DESC
    ) AS balance_rank
FROM customer_balances
ORDER BY balance_rank, customer_id;


-- Q27. Top 3 customers per branch.
-- Answer:
-- Returns the top three balance ranks.
-- Ties can result in more than three customers per branch.
;WITH customer_branch_balances AS (
    SELECT
        customer_id,
        branch_id,
        SUM(balance) AS total_balance
    FROM accounts
    GROUP BY customer_id, branch_id
),
ranked_customers AS (
    SELECT
        customer_id,
        branch_id,
        total_balance,
        DENSE_RANK() OVER (
            PARTITION BY branch_id
            ORDER BY total_balance DESC
        ) AS balance_rank
    FROM customer_branch_balances
)
SELECT
    c.customer_id,
    c.customer_name,
    b.branch_name,
    r.total_balance,
    r.balance_rank
FROM ranked_customers AS r
INNER JOIN customers AS c
    ON r.customer_id = c.customer_id
INNER JOIN branches AS b
    ON r.branch_id = b.branch_id
WHERE r.balance_rank <= 3
ORDER BY b.branch_id, r.balance_rank, c.customer_id;


-- Q28. Rank transactions per customer.
-- Answer:
-- Highest transaction amount receives rank 1.
-- Equal amounts receive the same rank.
SELECT
    c.customer_id,
    c.customer_name,
    t.transaction_id,
    t.account_id,
    t.amount,
    t.mode,
    t.transaction_date,
    DENSE_RANK() OVER (
        PARTITION BY c.customer_id
        ORDER BY t.amount DESC
    ) AS transaction_rank
FROM customers AS c
INNER JOIN accounts AS a
    ON c.customer_id = a.customer_id
INNER JOIN transactions AS t
    ON a.account_id = t.account_id
ORDER BY c.customer_id, transaction_rank, t.transaction_id;