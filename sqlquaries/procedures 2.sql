use aspiretrust;

CREATE PROCEDURE IF NOT EXISTS get_user_id_from_account_number(
    account_number VARCHAR(20)
)
BEGIN
    SELECT user_id FROM account a WHERE a.account_number = account_number;
end;


CREATE PROCEDURE IF NOT EXISTS create_user_account_from_account_number(
    username VARCHAR(20),
    password VARCHAR(50),
    account_number VARCHAR(20)
    )
BEGIN
        DECLARE _user_id INT;
        SELECT user_id INTO _user_id FROM account a WHERE a.account_number = account_number;
        INSERT INTO auth(user_id, username, password) VALUES (_user_id,username,password);
end;


CREATE PROCEDURE IF NOT EXISTS transfer_money(
    from_acccount_number VARCHAR(20),
    to_account_number VARCHAR(20),
    amount INT,
    remarks VARCHAR(50)
)
BEGIN
    DECLARE from_account_id INT;
    DECLARE to_account_id INT;
    SELECT account_id INTO  from_account_id FROM account WHERE account_number = from_acccount_number;
    SELECT account_id INTO  to_account_id FROM  account WHERE  account_number = to_account_number;
    INSERT INTO operation(account_id, operation_type, amount, remark) VALUES (from_account_id,'TRANSACTION',amount,remarks);
    INSERT INTO transaction(operation_id, to_acc) VALUES (LAST_INSERT_ID(),to_account_id);
    UPDATE account SET account.balance = account.balance - amount WHERE account_number = from_acccount_number;
    UPDATE account SET account.balance = account.balance + amount WHERE account_number = to_account_number;
end;

CREATE PROCEDURE IF NOT EXISTS get_account_details(
    user_id INT
)
BEGIN
    SELECT account_number,balance,account_type FROM account WHERE account.user_id = user_id;
end;


CREATE PROCEDURE IF NOT EXISTS get_user_details(
    user_id INT
)
BEGIN
    SELECT first_name,last_name,telephone,nic,home_town FROM user;
end;

CREATE PROCEDURE IF NOT EXISTS maximum_loan_amount(
    user_id INT
)
BEGIN
    SELECT amount*0.6 as maximum_loan_amount FROM fixed_deposit WHERE fixed_deposit.user_id = user_id;
end;

CREATE PROCEDURE IF NOT EXISTS update_user_details(
    user_id INT,
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    date_of_birth DATE,
    telephone VARCHAR(12),
    home_town VARCHAR(20)
)
BEGIN
    UPDATE user
        SET user.first_name = first_name,
        user.last_name = last_name,
        user.date_of_birth = date_of_birth,
        user.telephone  = telephone,
        user.home_town = home_town
    WHERE user.user_id = user_id;
end;


CREATE PROCEDURE IF NOT EXISTS apply_for_online_loan(
    user_id INT,
    fixed_deposit_id INT,
    amount DECIMAL(10,2),
    duration INT,
    interest_rate DECIMAL(3,2)
)
BEGIN
    DECLARE _branch_id INT;
    DECLARE _account_id_ INT;
    DECLARE _savings_account_id INT;
    DECLARE _loan_id INT;
    SELECT savings_account_id INTO _savings_account_id FROM fixed_deposit WHERE fixed_deposit.fixed_deposit_id = fixed_deposit_id;
    SELECT account_id INTO _account_id_ FROM savings_account WHERE savings_account.savings_account_id = _savings_account_id;
    SELECT branch_id INTO _branch_id FROM account WHERE account_id = _account_id_;
    INSERT INTO loan(user_id, approved, amount, duration, branch_id, interest_rate) VALUES (user_id,0,amount,duration,_branch_id,interest_rate);
    SET _loan_id = LAST_INSERT_ID();
    INSERT INTO online_loan(loan_id, fixed_deposit_id) VALUES (LAST_INSERT_ID(),fixed_deposit_id);
    UPDATE loan
        SET approved = 1
        WHERE loan_id = _loan_id;
    UPDATE account
        SET account.balance = account.balance + amount
        WHERE account_id = _account_id_;
end;


CREATE PROCEDURE IF NOT EXISTS create_bank_account_for_existing_user(
    user_id_ INT,
    new_account_number_ VARCHAR(20),
    old_account_number_ VARCHAR(20),
    account_type_ VARCHAR(20),
    amount DECIMAL(10,2)
)
    BEGIN
            DECLARE _branch_id INT;
            DECLARE user_id_of_customer INT;
            SELECT branch_id INTO _branch_id FROM employee WHERE employee.user_id = user_id_;
            SELECT user_id INTO user_id_of_customer FROM account WHERE account.account_number = old_account_number_;
            INSERT INTO account(account_number, user_id, branch_id, account_type, balance)
                VALUES (new_account_number_,user_id_of_customer,_branch_id,account_type_,amount);
    end;


CREATE PROCEDURE get_first_name_and_number_of_accounts(
    account_number_ VARCHAR(20)
)
BEGIN
    DECLARE _user_id INT;
    SELECT user_id INTO _user_id FROM account WHERE account_number = account_number_;
    SELECT first_name,COUNT(account_id) as number_of_accounts FROM account JOIN user USING(user_id) where user_id =_user_id GROUP BY user_id;
end;



CREATE PROCEDURE IF NOT EXISTS create_bank_account_for_new_user(
    first_name_ VARCHAR(50),
    last_name_ VARCHAR(50),
    branch_id_ INT,
    nic_ VARCHAR(12),
    telephone_ VARCHAR(12),
    home_town_ VARCHAR(50),
    date_of_birth_ DATE,
    amount_ DECIMAL(10,2),
    account_number_ VARCHAR(20),
    account_type_ VARCHAR(20)
)
    BEGIN
        DECLARE _branch_id INT;
        SELECT branch_id INTO  _branch_id FROM branch WHERE branch_id = branch_id_;
        IF _branch_id IS NULL THEN
            SIGNAL SQLSTATE '01011' SET MESSAGE_TEXT = 'Branch id is not valid';
        end if;
        INSERT INTO user(nic, user_type, first_name, last_name, date_of_birth, telephone, home_town)
            VALUES (nic_,'CUSTOMER',first_name_,last_name_,date_of_birth_,telephone_,home_town_);
        INSERT INTO account(account_number, user_id, branch_id, account_type, balance)
            VALUES (account_number_,LAST_INSERT_ID(),branch_id_,account_type_,amount_);
    end;



CREATE PROCEDURE branch_wise_total_transactions(
    from_branch_id_ INT,
    to_branch_id_ INT
)
    BEGIN
        SELECT operation.created_at as date_time, a.account_number as from_account ,b.account_number as to_account,amount,remark FROM operation JOIN transaction USING(operation_id) JOIN account a USING (account_id) JOIN account b ON transaction.to_acc = b.account_id where a.branch_id = from_branch_id_ OR  b.branch_id=to_branch_id_;
    end;


CREATE PROCEDURE create_fixed_deposit_for_existing_user(
    user_id_ INT,
    savings_account_id_ INT,
    amount_ DECIMAL(10,2),
    duration_ INT
)
    BEGIN
        DECLARE _branch_id INT;
        DECLARE user_id_of_customer INT;
        SELECT branch_id INTO _branch_id FROM employee WHERE employee.user_id = user_id_;
        SELECT user_id INTO user_id_of_customer FROM savings_account JOIN account USING (account_id )WHERE savings_account_id = savings_account_id_;
        INSERT INTO fixed_deposit(user_id, amount, duration, savings_account_id) VALUES (user_id_of_customer,amount_,duration_,savings_account_id_);
    end;

CREATE PROCEDURE create_fixed_deposit_for_existing_user_organization(
    user_id_ INT,
    savings_account_id_ INT,
    amount_ DECIMAL(10,2),
    duration_ INT,
    organization_name VARCHAR(20),
    organization_role VARCHAR(20)
)
    BEGIN
        DECLARE _organization_id INT;
        DECLARE _customer_id INT;

        SELECT organization_id INTO _organization_id FROM organization WHERE organization.name = organization_name;
        SELECT user_id INTO _customer_id FROM savings_account JOIN account USING (account_id )WHERE savings_account_id = savings_account_id_;
        IF _organization_id IS NULL THEN
            INSERT INTO organization(name) VALUES (organization_name);
            SET _organization_id = LAST_INSERT_ID();
            INSERT INTO organization_member( organization_id, role, user_id) VALUES (_organization_id,organization_role,_customer_id);
        end if;
        INSERT INTO fixed_deposit( user_id, amount, duration, savings_account_id) VALUES (user_id_,amount_,duration_,savings_account_id_);
    end;


CREATE PROCEDURE create_account_for_existing_organization(
    employee_user_id_ INT,
    old_account_number_ VARCHAR(20),
    new_account_number_ VARCHAR(20),
    amount_ DECIMAL(10,2),
    organization_name_ VARCHAR(20),
    organization_role_ VARCHAR(20),
    account_type_ VARCHAR(20)
)
    BEGIN
        DECLARE _branch_id INT;
        DECLARE organization_id_ INT;
        DECLARE customer_user_id INT;
        SELECT user_id INTO customer_user_id FROM  account WHERE account_number = old_account_number_;
        SELECT branch_id INTO _branch_id FROM employee WHERE employee.user_id = employee_user_id_;
        SELECT organization_id INTO organization_id_ FROM organization WHERE organization.name = organization_name_;
        IF organization_id_ IS NULL THEN
            INSERT INTO organization(name) VALUES (organization_name_);
            SET organization_id_ = LAST_INSERT_ID();
        end if;
        INSERT INTO organization_member(organization_id, role, user_id)  VALUES (organization_id_,organization_role_,customer_user_id);
        INSERT INTO account(account_number, user_id, branch_id, account_type, balance) VALUES (new_account_number_,customer_user_id,_branch_id,account_type_,amount_);
    end;

CREATE PROCEDURE get_fixed_accounts(
user_id_ INT
)
    BEGIN
        SELECT fixed_deposit_id,amount,duration FROM fixed_deposit WHERE user_id = user_id_;
    end;

CREATE PROCEDURE add_employee(
    manager_user_id INT,
    first_name_ VARCHAR(20),
    last_name_ VARCHAR(20),
    nic_ VARCHAR(12),
    telephone_ VARCHAR(12),
    home_town_ VARCHAR(20),
    date_of_birth_ DATE,
    role_ VARCHAR(20)
)
    BEGIN
        DECLARE _branch_id INT;
        SELECT branch_id INTO _branch_id FROM employee WHERE user_id = manager_user_id;
        INSERT INTO user(nic, user_type, first_name, last_name, date_of_birth, telephone, home_town ) VALUES (nic_,'EMPLOYEE',first_name_,last_name_,date_of_birth_,telephone_,home_town_);
        INSERT INTO employee( position, branch_id, user_id) VALUES (role_,_branch_id,LAST_INSERT_ID());
    end;
