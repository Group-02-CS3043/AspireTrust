USE aspiretrust;

-- this file is used to implements events
-- can be extended to add more events

-- this event is created to calculate savings interest
-- and add it the the savings account balance
-- It runs every month
CREATE EVENT IF NOT EXISTS calculate_savings_interest
ON SCHEDULE EVERY 1 MONTH
DO
BEGIN
    UPDATE account JOIN savings_account USING (account_id)
    SET
        account.balance = CASE
            WHEN savings_account.plan='CHILDREN' THEN
                account.balance * 1.12
            WHEN savings_account.plan='TEEN' THEN
                account.balance* 1.11
            WHEN savings_account.plan='ADULT' THEN
                account.balance * 1.10
            WHEN savings_account.plan='SENIOR' THEN
                account.balance * 1.13
            ELSE account.balance -- No change if duration is not 6, 12, or 36
        END
    WHERE savings_account.plan IN ('CHILDREN','TEEN','ADULT','SENIOR');
END;


-- this event is created ot calculate fixed deposit interest amount
-- and add it the amount of the fixed deposit
-- It runs every month
CREATE EVENT IF NOT EXISTS calculate_fd_installment
ON SCHEDULE EVERY 1 MONTH
DO
BEGIN
    UPDATE fixed_deposit
    SET
        fixed_deposit.amount = CASE
            WHEN fixed_deposit.duration = 6 THEN fixed_deposit.amount * 1.13
            WHEN fixed_deposit.duration = 12 THEN fixed_deposit.amount * 1.14
            WHEN fixed_deposit.duration = 36 THEN fixed_deposit.amount * 1.15
            ELSE amount  -- No change if duration is not 6, 12, or 36
        END
    WHERE duration IN (6, 12, 36);
END;

-- this event is created to check if any fixed deposit has expired
-- and if it has expired then it will add the amount to the savings account
-- and set the amount of the fixed deposit to 0
-- then every fixed deposit with amount 0 will be deleted
-- It runs every day
CREATE EVENT IF NOT EXISTS check_expired_fixed_deposits
ON SCHEDULE EVERY 1 DAY
DO
BEGIN
    UPDATE account JOIN savings_account using (account_id) JOIN fixed_deposit USING (savings_account_id)
        SET account.balance=account.balance+fixed_deposit.amount,
            fixed_deposit.amount = 0
        WHERE fixed_deposit_id IN
                (SELECT fixed_deposit_id FROM fixed_deposit WHERE
                    DATE_ADD(created_at, INTERVAL duration MONTH) < NOW());
    UPDATE fixed_deposit
    JOIN (
        SELECT fixed_deposit_id
        FROM fixed_deposit
        WHERE DATE_ADD(created_at, INTERVAL duration MONTH) < NOW()
    ) AS subquery
    SET fixed_deposit.amount = 0
    WHERE fixed_deposit.fixed_deposit_id = subquery.fixed_deposit_id;

    DELETE FROM fixed_deposit WHERE fixed_deposit.amount = 0;
END;


-- this event is created to check if any loan has expired
-- and if it has expired then it will set the amount of the loan to 0
-- then every loan with amount 0 will be deleted
-- It runs every day
CREATE EVENT IF NOT EXISTS check_expired_loan
ON SCHEDULE EVERY 1 DAY
DO
BEGIN
    UPDATE loan
    JOIN (
        SELECT loan_id
        FROM loan
        WHERE DATE_ADD(created_at, INTERVAL duration MONTH) < NOW()
    ) AS subquery
    SET loan.amount = 0
    WHERE loan.loan_id = subquery.loan_id;
    DELETE FROM online_loan WHERE online_loan.loan_id IN (SELECT loan_id FROM loan
        WHERE DATE_ADD(created_at, INTERVAL duration MONTH) < NOW());
    DELETE FROM loan_installment WHERE loan_installment.loan_id IN (SELECT loan_id FROM loan
        WHERE DATE_ADD(created_at, INTERVAL duration MONTH) < NOW());
    DELETE FROM loan WHERE loan.amount = 0;
END;
