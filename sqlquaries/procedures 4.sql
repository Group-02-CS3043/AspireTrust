use aspiretrust;


-- reports for withdraw, deposit
DELIMITER $$
CREATE PROCEDURE withdraw(
    IN min_val decimal(10,2),
    IN max_val decimal(10,2),
    IN start_date DATE,
    IN end_date DATE,
    IN branch_id int
)
BEGIN
    SELECT created_at as date_time,
           account.account_number as account,
           amount,
           remark
    FROM operation 
    JOIN account account ON account.account_id = operation.account_id 
    WHERE (created_at BETWEEN start_date AND end_date)
	  AND operation_type='WITHDRAW'
      AND account.branch_id = branch_id 
      AND amount BETWEEN min_val AND max_val;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE deposit(
    IN min_val decimal(10,2),
    IN max_val decimal(10,2),
    IN start_date DATE,
    IN end_date DATE,
    IN branch_id int
)
BEGIN
    SELECT created_at as date_time,
           account.account_number as account,
           amount,
           remark
    FROM operation 
    JOIN account account ON account.account_id = operation.account_id 
    WHERE (created_at BETWEEN start_date AND end_date)
	  AND operation_type='DEPOSIT'
      AND account.branch_id = branch_id 
      AND amount BETWEEN min_val AND max_val;
END $$
DELIMITER ;

CREATE PROCEDURE InsertInitialLoanInstallment(IN loan_id_param INT)
BEGIN
    DECLARE next_payment_date_param DATETIME;

    -- Calculate next_payment_date as 1 month after the current date

    IF EXISTS(SELECT 1 FROM loan_installment WHERE loan_installment_id = loan_id_param) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Loan does not exists';
    end if;
    SET next_payment_date_param = DATE_ADD(NOW(), INTERVAL 1 MONTH);

    -- Insert the data into the loan_installment table
    INSERT INTO loan_installment (loan_id,next_payment_date, paid_count)
    VALUES (loan_id_param, next_payment_date_param, 0);
END;

CREATE PROCEDURE UpdateSubsequentLoanInstallment(IN loan_id_param INT)
BEGIN
    DECLARE previous_next_payment_date DATETIME;
    DECLARE last_payment_date_param DATETIME;
    DECLARE next_payment_date_param DATETIME;
    DECLARE paid_count_param INT;

    -- Get the previous next_payment_date and calculate the last_payment_date
  SELECT last_payment_date INTO  last_payment_date_param FROM loan_installment WHERE loan_id = loan_id_param;
  SELECT next_payment_date INTO next_payment_date_param FROM loan_installment WHERE  loan_id = loan_id_param;
  SELECT paid_count INTO paid_count_param FROM loan_installment WHERE loan_id = loan_id_param;



    SET next_payment_date_param = DATE_ADD(next_payment_date_param, INTERVAL 1 MONTH);
    SET last_payment_date_param = DATE_ADD(last_payment_date_param,INTERVAL 1 MONTH );

    SET paid_count_param = paid_count_param + 1;
    UPDATE loan_installment
        SET paid_count = paid_count_param,
        next_payment_date = next_payment_date_param,
        last_payment_date = last_payment_date_param
        WHERE loan_id = loan_id_param;

END;
call InsertInitialLoanInstallment(1);
UPDATE loan_installment SET last_payment_date = NOW() WHERE loan_installment_id = 1;

SELECT * FROM loan_installment;
call UpdateSubsequentLoanInstallment(1);
SELECT * FROM loan;