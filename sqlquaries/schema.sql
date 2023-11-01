u-- GROUP - 02 | Bank Transaction And Loan Processing System
-- Our database is named as aspiretrust


-- Note :
-- In here we didn't attach any triggers or procedures
-- Also for flexible design we can implement further tables
-- Like customers,saving_account_plans,fixed_deposit_plans,loan_types,user_permissions,etc
-- But for simplicity(reduce complexity) and reduce cost we have implemented lowest possible structure

-- Following contain queries creating database


drop database if exists aspiretrust;
create database aspiretrust;
use aspiretrust;


-- Creating user table
-- user table is storing common values for all the users
-- Since user table contain huge amount of data when joining it may be difficult
-- For a flexible design we can extend user credentials to a another table and reduce cost
-- In here to reduce complexity we have use only one table
CREATE TABLE IF NOT EXISTS user(
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    nic VARCHAR(12),
    user_type VARCHAR(10) NOT NULL CHECK(user.user_type IN ('CUSTOMER','EMPLOYEE')),
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    date_of_birth DATE NOT NULL,
    telephone VARCHAR(12) ,
    home_town VARCHAR(25) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS auth(
    user_id int PRIMARY KEY ,
    username VARCHAR(30) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);
-- Creating organization table
CREATE TABLE IF NOT EXISTS organization(
  organization_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(30) NOT NULL
);


-- Creating organization_member table
-- For flexibility we can add permissions and other needed details for this table
CREATE TABLE IF NOT exists organization_member(
	organization_member_id INT AUTO_INCREMENT PRIMARY KEY,
    organization_id INT NOT NULL,
    role VARCHAR(50) NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organization(organization_id),
    FOREIGN KEY (user_id) references user(user_id)
);


-- Creating branch table
-- Since manager role is having recursion relationship first we have to set the manager_id to NULL and then alter table to foreign key
CREATE TABLE IF NOT EXISTS branch (
  branch_id INT AUTO_INCREMENT PRIMARY KEY,
  city VARCHAR(20) NOT NULL,
  address VARCHAR(50) ,
  manager_id INT DEFAULT NULL
);

-- Creating employee table
CREATE TABLE IF NOT EXISTS employee (
  employee_id INT AUTO_INCREMENT PRIMARY KEY,
  position VARCHAR(25) NOT NULL CHECK (employee.position IN('MANAGER','TAILOR','ACADEMIC-STAFF')),
  branch_id INT NOT NULL,
  user_id INT NOT NULL,
  FOREIGN KEY (branch_id) REFERENCES branch(branch_id),
  FOREIGN KEY (user_id) REFERENCES user(user_id)
);

-- Creating account table
CREATE TABLE IF NOT EXISTS account (
	account_id INT AUTO_INCREMENT ,
    account_number VARCHAR(20) NOT NULL UNIQUE ,
    user_id INT NOT NULL,
    branch_id INT NOT NULL,
    account_type VARCHAR(20) NOT NULL CHECK (account.account_type IN ('SAVINGS','CURRENT')),
    balance DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (account_id,user_id,account_number),
	FOREIGN KEY (user_id) REFERENCES user(user_id),
	FOREIGN KEY (branch_id) REFERENCES branch(branch_id)
);

-- Creating savings_account table
CREATE TABLE IF NOT EXISTS savings_account (
  savings_account_id INT AUTO_INCREMENT,
  account_id INT NOT NULL,
  plan VARCHAR(10) NOT NULL CHECK (savings_account.plan IN ('CHILDREN','TEEN','ADULT','SENIOR')),
  primary key (savings_account_id,account_id),
  FOREIGN KEY (account_id) REFERENCES account(account_id)
);

-- Creating fixed_deposit table
CREATE TABLE IF NOT EXISTS fixed_deposit (
  fixed_deposit_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL ,
  amount DECIMAL(10,2) NOT NULL,
  duration INT NOT NULL CHECK (fixed_deposit.duration IN (6,12,36)),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  savings_account_id INT NOT NULL,
  FOREIGN KEY (savings_account_id) REFERENCES savings_account(savings_account_id),
  FOREIGN KEY (user_id) REFERENCES  user(user_id)
);


-- Creating operation table
CREATE TABLE IF NOT EXISTS operation (
  operation_id INT AUTO_INCREMENT PRIMARY KEY,
  account_id INT NOT NULL,
  operation_type VARCHAR(20) NOT NULL CHECK (operation.operation_type IN ('TRANSACTION','WITHDRAW','DEPOSIT')),
  amount DECIMAL(10,2) NOT NULL,
  remark VARCHAR(50) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (account_id) REFERENCES account(account_id)
);

-- Creating transaction table
CREATE TABLE IF NOT EXISTS transaction (
  transaction_id INT AUTO_INCREMENT PRIMARY KEY,
  operation_id INT NOT NULL,
  to_acc INT NOT NULL,
  FOREIGN KEY (operation_id) REFERENCES operation(operation_id),
  FOREIGN KEY (to_acc) REFERENCES account(account_id)
);

-- Creating loan table
CREATE TABLE IF NOT EXISTS loan(
    loan_id INT AUTO_INCREMENT ,
    user_id INT NOT NULL ,
    approved BOOLEAN DEFAULT false,
    amount DECIMAL(10,2),
    duration INT NOT NULL,
    branch_id INT ,
    interest_rate DECIMAL(10,2) ,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (loan_id,user_id)
);


-- Creating loan_request table
CREATE TABLE IF NOT EXISTS loan_request (
  loan_request_id INT AUTO_INCREMENT,
  user_id INT NOT NULL ,
  employee_id INT NOT NULL ,
  loan_id INT NOT NULL ,
  PRIMARY KEY (loan_request_id),
  FOREIGN KEY (user_id) REFERENCES user(user_id),
  FOREIGN KEY (employee_id) REFERENCES employee(employee_id),
  FOREIGN KEY (loan_id) REFERENCES loan(loan_id)
);

-- Creating online_loan table
CREATE TABLE IF NOT EXISTS online_loan(
    online_loan_id INT AUTO_INCREMENT PRIMARY KEY ,
    loan_id INT NOT NULL,
    fixed_deposit_id INT NOT NULL,
    FOREIGN KEY (loan_id) REFERENCES loan(loan_id),
    FOREIGN KEY (fixed_deposit_id) REFERENCES fixed_deposit(fixed_deposit_id)
);

-- Creating loan_installment table
CREATE TABLE loan_installment(
    loan_installment_id INT AUTO_INCREMENT PRIMARY KEY ,
    loan_id INT NOT NULL,
    due_date DATETIME ,
    paid BOOLEAN,
    paid_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    paid_count INT DEFAULT 0,
    due_count INT,
    FOREIGN KEY (loan_id) REFERENCES loan(loan_id)
);

-- Alter the branch table since now employee table is created
ALTER TABLE branch
ADD FOREIGN KEY (manager_id) REFERENCES employee (employee_id);