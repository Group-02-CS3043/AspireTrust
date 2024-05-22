-- -------------------------------------------------------------------
-- Following contain queries inserting data
-- ------------------------------------------------------------------------



-- Adding dummy data to user table
INSERT INTO user (user_type, first_name, last_name, date_of_birth, telephone, home_town) VALUES
('CUSTOMER', 'John', 'Doe', '1990-01-01', '1234567890', 'New York'),
( 'CUSTOMER', 'Jane', 'Smith', '1995-05-05', '0987654321', 'Los Angeles'),
('CUSTOMER', 'Bob', 'Johnson', '1985-12-31', '1112223333', 'Chicago'),
('EMPLOYEE', 'meyale', 'carl', '1980-07-15', '5555555555', 'Sydney'),
('EMPLOYEE', 'chris', 'owens', '1980-07-15', '09238782372', 'Tokiyo'),
('EMPLOYEE', 'charles', 'bebage', '1980-07-15', '21889121', 'Down South'),
('EMPLOYEE', 'anna', 'mary', '1980-07-15', '2313131', 'Monaragala'),
('CUSTOMER', 'elon', 'musk', '1982-09-20', '6666666666', 'Rathnapura');

-- Adding dummy data to organization table
INSERT INTO organization (name) VALUES
('X cooperation'),
('facebook pvt ltd'),
('MFTE');

-- Adding dummy data to organization_member table
-- we can access user_id from following query
-- SELECT user_id FROM user WHERE username = 'elon_musk';
INSERT INTO organization_member (organization_id, role, user_id) VALUES
(1, 'Employee', 1),
(1, 'CEO', 8),
(2, 'Employee', 2);

-- Adding dummy data to branch table
-- Since employee table have recursive relationship First we have add null value to manager_id and after employee table created we can update last database quaries
INSERT INTO branch (city, address,manager_id) VALUES
('New York', '123 Main St.',NULL),
('Los Angeles', '456 Elm St.',NULL),
('Chicago', '789 Oak St.',NULL);

-- Adding dummy data to table employee
-- we can access user_id and branch_id from following queries
-- SELECT user_id FROM user WHERE username = 'elon_musk';
-- SELECT branch_id FROM branch WHERE city = 'New York';
INSERT INTO employee (position, branch_id, user_id) VALUES
('MANAGER', 1, 7),
('TAILOR', 1, 4),
('TAILOR', 2, 5);

-- We have to update above nulled manager id
-- We can get branch_id,employee_id from following quaries
-- SELECT branch_id FROM employee WHERE position = 'Manager' LIMIT 1;
-- SELECT employee_id FROM employee WHERE position = 'Manager' LIMIT 1;
UPDATE branch
SET manager_id = 1
WHERE branch_id = 1;



-- Adding dummy data for account table
-- we can access user_id and branch_id from following queries
-- SELECT user_id FROM user WHERE username = 'elon_musk';
-- SELECT branch_id FROM branch WHERE city = 'New York';
INSERT INTO account (account_number, user_id, branch_id, account_type, balance) VALUES
('123-4567-890', 1, 1, 'SAVINGS', 5000.00),
('234-5678-901', 2, 2, 'CURRENT', 10000.00),
('345-6789-012', 3, 3, 'SAVINGS', 7500.00),
('456-7890-123', 4, 1, 'CURRENT', 2000.00),
('567-8901-234', 5, 2, 'SAVINGS', 3000.00),
('567-8901-235', 6, 2, 'SAVINGS', 3000.00);

-- Adding data to savings_account table
-- we can get account id from following query
-- SELECT account_id FROM account JOIN user USING (user_id) WHERE username = 'john_doe';
INSERT INTO savings_account (account_id, plan) VALUES
(1, 'Children'),
(3, 'Teen'),
(5, 'Adult'),
(6, 'Senior');


-- Adding Fixed Deposits
-- we can get the saving_account_id from following query
-- SELECT savings_account_id from savings_account JOIN account USING(account_id) JOIN user USING (user_id) WHERE  username = 'john_doe';
INSERT INTO fixed_deposit(user_id, amount, duration , savings_account_id)
VALUES (1,10000,6,1),
       (2,20000,12,2),
       (3,100000,36 ,3);


-- Adding data to loan table
-- We can get the user_id and branch_id from following queries
-- SELECT user_id FROM user WHERE username = 'elon_musk';
-- SELECT branch_id FROM branch WHERE city = 'New York';
INSERT INTO loan(user_id, amount, duration, branch_id, interest_rate)
VALUES
    (1,10000,12,1,14),
    (2,10000,6,2,13),
    (8,40000,18,3,15);


-- Adding data to loan_request table
-- we can get the employee_id from following query
-- SELECT employee_id FROM employee JOIN user USING (user_id) where username = 'chris_owens';
INSERT INTO loan_request(user_id, employee_id, loan_id)
VALUES (1,3,1);


-- Adding data to the operation table
-- We can get the operation_type based on the type of transaction, e.g., 'deposit', 'withdraw', 'transaction'
-- Assuming operation_id is auto-incremented and created_at should have the current timestamp
INSERT INTO operation(account_id, operation_type, amount, remark, created_at)
VALUES (1,'DEPOSIT',1000,'gift',CURRENT_TIMESTAMP),
       (2,'WITHDRAW',1000,'books',CURRENT_TIMESTAMP),
       (3,'TRANSACTION',2000,'bill payment',CURRENT_TIMESTAMP);



-- Adding data to the transaction table
-- We can get the operation_id and to_acc (destination account) based on the corresponding operation
-- Assuming operation_id in the transaction table is a foreign key referencing the operation table, and to_acc references the account table
INSERT INTO transaction(operation_id, to_acc)
VALUES (3,2),
       (1,2);