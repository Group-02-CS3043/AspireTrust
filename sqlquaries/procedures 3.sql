USE aspiretrust;

-- this procdeure generates a interbranch transaction report
DELIMITER $$
CREATE PROCEDURE inter_bank_report( IN min_val decimal(10,2) , IN max_val decimal(10,2),   IN start_date DATE, IN end_date DATE , IN from_branch_id int, IN to_branch_id int)
BEGIN
    SELECT created_at as date_time , from_account.account_number as  from_account  , to_account.account_number as to_account , amount, remark
    FROM operation
    JOIN transaction USING (operation_id)
    JOIN account from_account ON from_account.account_id = operation.account_id 
    JOIN account to_account ON to_account.account_id = transaction.to_acc
    WHERE (created_at BETWEEN start_date AND end_date )
    AND (from_account.branch_id = from_branch_id) AND (to_account.branch_id = to_branch_id) 
    AND (amount BETWEEN min_val AND max_val);
	
    
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE intra_bank_report( IN min_val decimal(10,2) , IN max_val decimal(10,2),   IN start_date DATE, IN end_date DATE , IN from_branch_id int, IN to_branch_id int)
BEGIN
    SELECT created_at as date_time , from_account.account_number as  from_account  , to_account.account_number as to_account , amount, remark
    FROM operation
    JOIN transaction USING (operation_id)
    JOIN account from_account ON from_account.account_id = operation.account_id 
    JOIN account to_account ON to_account.account_id = transaction.to_acc
    WHERE (created_at BETWEEN start_date AND end_date )
    AND (from_account.branch_id = from_branch_id) or (to_account.branch_id = to_branch_id) 
    AND (amount BETWEEN min_val AND max_val);
	
    
END $$
DELIMITER ;