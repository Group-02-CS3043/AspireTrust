use aspiretrust;

-- procedures for creating new accounts for new users

CREATE PROCEDURE IF NOT EXISTS create_savings_account_for_new_individual_user(
    first_name_ VARCHAR(50),
    last_name_ VARCHAR(50),
    branch_id_ INT,
    nic_ VARCHAR(12),
    telephone_ VARCHAR(12),
    home_town_ VARCHAR(50),
    date_of_birth_ DATE,
    amount_ DECIMAL(10,2),
    account_number_ VARCHAR(20)
)
    BEGIN
        DECLARE _plan VARCHAR(20);
        DECLARE _age INT;
        DECLARE _user_id INT;
        DECLARE _error VARCHAR(50);

        IF EXISTS (SELECT 1 FROM user WHERE first_name = first_name_ AND last_name = last_name_) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'There is a user already registered !';
        END IF;

        IF NOT EXISTS (SELECT 1 FROM branch WHERE branch_id = branch_id_) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Branch id is not valid !';
        END IF;


        IF EXISTS(SELECT 1 FROM account WHERE account_number = account_number_) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account already exists !';
        end if;

        SET _age = TIMESTAMPDIFF(YEAR, date_of_birth_, NOW());
        SET _plan =
            CASE
                WHEN _age BETWEEN 0 AND 12 THEN 'CHILDREN'
                WHEN _age BETWEEN 13 AND 18 THEN 'TEEN'
                WHEN _age BETWEEN 19 AND 60 THEN 'ADULT'
                ELSE 'SENIOR'
            END;

        IF _plan = 'TEEN' AND amount_ < 500 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Teen account must deposit minimum 500' ;

        ELSEIF _plan = 'ADULT' AND  amount_ < 1000 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Adult account must deposit minimum 1000';
        ELSEIF _plan = 'SENIOR' AND amount_ < 1000 THEN
             SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Senior account must deposit minimum 1000';
        end if;

        INSERT INTO user(nic, user_type, first_name, last_name, date_of_birth, telephone, home_town)
            VALUES (nic_,'CUSTOMER',first_name_,last_name_,date_of_birth_,telephone_,home_town_);

        SET _user_id = LAST_INSERT_ID();
        INSERT INTO account(account_number, user_id, branch_id, account_type, balance)
            VALUES (account_number_,_user_id,branch_id_,'SAVINGS',amount_);

        INSERT INTO savings_account(account_id, plan) VALUES (LAST_INSERT_ID(),_plan);

        SELECT first_name,account_number,account_type,created_at FROM user JOIN account USING (user_id) WHERE account_number = account_number_;
    end;


CREATE PROCEDURE IF NOT EXISTS create_current_account_for_new_individual_user(
    first_name_ VARCHAR(50),
    last_name_ VARCHAR(50),
    branch_id_ INT,
    nic_ VARCHAR(12),
    telephone_ VARCHAR(12),
    home_town_ VARCHAR(50),
    date_of_birth_ DATE,
    amount_ DECIMAL(10,2),
    account_number_ VARCHAR(20)
)
    BEGIN
        DECLARE _user_id INT;

        IF EXISTS (SELECT 1 FROM user WHERE first_name = first_name_ AND last_name = last_name_) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'There is a user already registered !';
        END IF;

        IF NOT EXISTS (SELECT 1 FROM branch WHERE branch_id = branch_id_) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Branch id is not valid !';
        END IF;


        IF EXISTS(SELECT 1 FROM account WHERE account_number = account_number_) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account already exists !';
        end if;

        INSERT INTO user(nic, user_type, first_name, last_name, date_of_birth, telephone, home_town)
            VALUES (nic_,'CUSTOMER',first_name_,last_name_,date_of_birth_,telephone_,home_town_);

        SET _user_id = LAST_INSERT_ID();
        INSERT INTO account(account_number, user_id, branch_id, account_type, balance)
            VALUES (account_number_,_user_id,branch_id_,'CURRENT',amount_);

         SELECT first_name,account_number,account_type,created_at FROM user JOIN account USING (user_id) WHERE account_number = account_number_;
    end;


CREATE PROCEDURE IF NOT EXISTS create_savings_account_for_new_organization_user(
    first_name_ VARCHAR(50),
    last_name_ VARCHAR(50),
    branch_id_ INT,
    nic_ VARCHAR(12),
    telephone_ VARCHAR(12),
    home_town_ VARCHAR(50),
    date_of_birth_ DATE,
    amount_ DECIMAL(10,2),
    account_number_ VARCHAR(20),
    organization_name_ VARCHAR(30),
    organization_role_ VARCHAR(20)
)
    BEGIN
        DECLARE _plan VARCHAR(20);
        DECLARE _age INT;
        DECLARE _user_id INT;
        DECLARE _organization_id INT;
        DECLARE _account_id INT;

        IF EXISTS (SELECT 1 FROM user WHERE first_name = first_name_ AND last_name = last_name_) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'There is a user already registered !';
        END IF;

        IF NOT EXISTS (SELECT 1 FROM branch WHERE branch_id = branch_id_) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Branch id is not valid !';
        END IF;


        IF EXISTS(SELECT 1 FROM organization WHERE organization.name = organization_name_) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Organization already exists !';
        end if;

        IF EXISTS(SELECT 1 FROM account WHERE account_number = account_number_) THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account already exists !';
        end if;

        SET _age = TIMESTAMPDIFF(YEAR, date_of_birth_, NOW());
        SET _plan =
            CASE
                WHEN _age BETWEEN 0 AND 12 THEN 'CHILDREN'
                WHEN _age BETWEEN 13 AND 18 THEN 'TEEN'
                WHEN _age BETWEEN 19 AND 60 THEN 'ADULT'
                ELSE 'SENIOR'
            END;

        IF _plan = 'TEEN' AND amount_ < 500 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Teen account must deposit minimum 500' ;

        ELSEIF _plan = 'ADULT' AND  amount_ < 1000 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Adult account must deposit minimum 1000';
        ELSEIF _plan = 'SENIOR' AND amount_ < 1000 THEN
             SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Senior account must deposit minimum 1000';
        end if;

        INSERT INTO organization(name) VALUES (organization_name_);
        SET _organization_id = LAST_INSERT_ID();

        INSERT INTO user(nic, user_type, first_name, last_name, date_of_birth, telephone, home_town)
            VALUES (nic_,'CUSTOMER',first_name_,last_name_,date_of_birth_,telephone_,home_town_);
        SET _user_id = LAST_INSERT_ID();

        INSERT INTO organization_member( organization_id, role, user_id) VALUES (_organization_id,organization_role_,_user_id);

        INSERT INTO account(account_number, user_id, branch_id, account_type, balance)
            VALUES (account_number_,_user_id,branch_id_,'SAVINGS',amount_);

        INSERT INTO savings_account(account_id, plan) VALUES (LAST_INSERT_ID(),_plan);

         SELECT first_name,account_number,account_type,created_at,organization_name_,organization_role_ FROM user JOIN account USING (user_id) WHERE account_number = account_number_;
    end;

CREATE PROCEDURE IF NOT EXISTS create_current_account_for_new_organization_user(
    first_name_ VARCHAR(50),
    last_name_ VARCHAR(50),
    branch_id_ INT,
    nic_ VARCHAR(12),
    telephone_ VARCHAR(12),
    home_town_ VARCHAR(50),
    date_of_birth_ DATE,
    amount_ DECIMAL(10,2),
    account_number_ VARCHAR(20),
    organization_name_ VARCHAR(30),
    organization_role_ VARCHAR(20)
)
    BEGIN
        DECLARE _user_id INT;
        DECLARE _organization_id INT;

        IF EXISTS (SELECT 1 FROM user WHERE first_name = first_name_ AND last_name = last_name_) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'There is a user already registered !';
        END IF;

        IF NOT EXISTS (SELECT 1 FROM branch WHERE branch_id = branch_id_) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Branch id is not valid !';
        END IF;


        IF EXISTS(SELECT 1 FROM organization WHERE organization.name = organization_name_) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Organization already exists !';
        end if;

        IF EXISTS(SELECT 1 FROM account WHERE account_number = account_number_) THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account already exists !';
        end if;


        INSERT INTO organization(name) VALUES (organization_name_);
        SET _organization_id = LAST_INSERT_ID();

        INSERT INTO user(nic, user_type, first_name, last_name, date_of_birth, telephone, home_town)
            VALUES (nic_,'CUSTOMER',first_name_,last_name_,date_of_birth_,telephone_,home_town_);
        SET _user_id = LAST_INSERT_ID();

        INSERT INTO organization_member( organization_id, role, user_id) VALUES (_organization_id,organization_role_,_user_id);

        INSERT INTO account(account_number, user_id, branch_id, account_type, balance)
            VALUES (account_number_,_user_id,branch_id_,'CURRENT',amount_);

        SELECT first_name,account_number,organization_name_,organization_role_,created_at FROM user JOIN account WHERE user.user_id = _user_id;
    end;
