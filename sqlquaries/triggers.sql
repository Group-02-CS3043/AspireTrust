use aspiretrust;

-- this file is used to implements triggers
-- can be extended to add more triggers


-- this event checks the validity of an online loan
-- according the the banks requirements
-- if the requested loan amount is greater than 60% of the fixed deposit amount
-- or if the requested loan amount is greater than 500000 (upper bound)
-- then the trigger will throw an error
DROP TRIGGER online_loan_validity_check;
CREATE TRIGGER IF NOT EXISTS online_loan_validity_check BEFORE INSERT ON online_loan FOR EACH ROW
BEGIN
    DECLARE loan_amount INT;
    DECLARE fixed_deposit_size INT;
    SELECT amount INTO fixed_deposit_size FROM  fixed_deposit WHERE NEW.fixed_deposit_id = fixed_deposit.fixed_deposit_id;
    SELECT amount INTO loan_amount FROM loan WHERE loan.loan_id = NEW.loan_id;

    IF (loan_amount > fixed_deposit_size*0.6) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Loan amount must be greater than 60% of the Fixed Deposit';
    end if;
    IF (loan_amount>500000) THEN
         SIGNAL SQLSTATE '45000'
         SET MESSAGE_TEXT = 'Maximum Loan Amount is 5000000';
    end if;
end;

-- this event checks the validity of a transaction
-- according to bank requiremnts
-- savings account can not perform more than 5 transactions per month
-- when a transaction is made, the trigger will check if the account has made more than 5 transactions in the last 30 days
-- if it has then the trigger will throw an error
CREATE TRIGGER IF NOT EXISTS check_transaction_limit BEFORE INSERT ON operation FOR EACH ROW
BEGIN
    DECLARE transaction_count INT;
    SELECT count(*) INTO transaction_count FROM operation JOIN account USING (account_id) WHERE operation.operation_type = 'TRANSACTION'
                        AND operation.account_id= NEW.account_id
                        AND account.account_type='SAVINGS'
                        AND created_at>=DATE_SUB(NOW(),INTERVAL 30 DAY);

    IF transaction_count > 4 THEN
        SIGNAL SQLSTATE '45001'
        SET MESSAGE_TEXT = 'Transaction Limit Exceeded';
    end if;
end;

-- this event checks the validity of a operation
-- savinga account have a minimum balance requirement
-- other account cant have a negative balance
-- if the operation is a withdraw or transaction
-- then the trigger will check if the account has enough balance to perform the operation
-- if it does not then the trigger will throw an error
CREATE TRIGGER IF NOT EXISTS check_operation_validity
    -- THIS TRIGGER WORKS
BEFORE INSERT ON operation FOR EACH ROW
BEGIN
    DECLARE Message VARCHAR(250);
    DECLARE min_balance DECIMAL(10,2);
    DECLARE curr_balance DECIMAL(10,2);
    DECLARE _plan VARCHAR(10);
    DECLARE _account_type VARCHAR(10);
    SELECT balance INTO curr_balance FROM account WHERE account.account_id=NEW.account_id;
    SELECT account_type INTO _account_type FROM account WHERE account.account_id=NEW.account_id;
    SELECT plan INTO _plan FROM savings_account WHERE NEW.account_id = savings_account.savings_account_id;
    IF _plan='ADULT' OR 'SENIOR' THEN
        SET min_balance=1000;
    ELSEIF _plan='TEEN' THEN
        SET min_balance=500;
    ELSEIF _plan='CHILDREN' OR _account_type='CURRENT' THEN
        SET min_balance=0;
    END IF;
    SET Message = 'er';
    IF NEW.operation_type IN ('WITHDRAW', 'TRANSACTION') THEN
            IF curr_balance - NEW.amount < min_balance THEN
                SIGNAL SQLSTATE '45001'
                SET MESSAGE_TEXT = Message;
            END IF;
    END IF;
END;
DELIMITER //
