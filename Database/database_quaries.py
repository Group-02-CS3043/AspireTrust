CHECK_FROM_ACCOUNT_NUMBER = "SELECT user_id from account WHERE account_number = %s"
VERIFY_USER_EXSISTS = "SELECT user_id from auth WHERE username = %s"
AUTHENTICATE_USER = "SELECT user_id from auth WHERE username = %s AND password = %s"
GET_THE_USER_ROLE = "SELECT user_type from user WHERE user_id = %s"
CREATE_USER_ACCOUNT_FROM_ACCOUNT_NUMBER = "CALL create_user_account_from_account_number(%s,%s,%s);"
CHECK_WETHER_USER_IS_ALREADY_HAVE_A_REGISTERED_ACCOUNT = "SELECT username FROM auth WHERE user_id = %s"
GET_FIRSTNAME_FROM_USER_ID = "SELECT first_name FROM user WHERE user_id = %s"
GET_USER_ACCOUNTS = 'SELECT account_number FROM account WHERE user_id = %s'
GET_ACCOUNT_ID = "SELECT account_id FROM account WHERE account_number = %s"
CREATE_TRANSACTION = "call transfer_money(%s,%s,%s,%s);"
GET_ACCOUNT_DETAILS = "call get_account_details(%s)"
GET_USER_DETAILS = "call get_user_details(%s)"
GET_MAXIMUM_LOAN_AMOUNT = 'call maximum_loan_amount(%s);'
GET_FD_ACCOUNTS = 'SELECT fixed_deposit_id FROM fixed_deposit WHERE user_id = %s'
GET_USER_INFORMATIONS = 'SELECT first_name,last_name,date_of_birth,telephone,home_town FROM user WHERE user_id = %s'
UPDATE_USER_DETAILS = 'call update_user_details(%s,%s,%s,%s,%s,%s)'
APPLY_FOR_ONLINE_LOAN = 'call apply_for_online_loan(%s,%s,%s,%s,%s)'
GET_BRANCH_ID = 'SELECT branch_id FROM employee WHERE user_id = %s'
CREATE_BANK_ACCOUNT_FOR_EXISTING_USERS = 'call create_bank_account_for_existing_user(%s,%s,%s,%s,%s)'
GET_CUSTOMER_FIRSTNAME_AND_NUMBER_OF_ACCOUNTS = 'call get_first_name_and_number_of_accounts(%s)'
CHECK_FIRSTNAME_AND_LASTNAME_EXISTS = 'SELECT first_name,last_name FROM user WHERE first_name = %s AND last_name = %s'
CREATE_BANK_ACCOUNT_FOR_NEW_USERS = 'call create_bank_account_for_new_user(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
GET_ALL_TRANSACIONS = 'call branch_wise_total_transactions(%s,%s);'
CREATE_FIXED_DEPOSIT = 'call create_fixed_deposit_for_existing_user(%s,%s,%s,%s)'
GET_SAVINGS_ACCOUNT_ID = 'SELECT savings_account_id FROM savings_account WHERE account_id = (SELECT account_id FROM account WHERE account_number = %s)'
CHECK_ACCOUNT_IS_VALID = 'SELECT account_id FROM account WHERE account_number = %s'
CREATE_BANK_ACCOUNT_FOR_ORGANIZATION = 'call create_bank_account_for_organization(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
CHECK_IF_ORGANIZATION_EXISTS = 'SELECT name FROM organization WHERE name = %s'
CREATE_BANK_ACCOUNT_FOR_EXSISTING_ORGANIZATION = 'call create_account_for_existing_organization(%s,%s,%s,%s,%s,%s,%s)'
CREATE_FIXED_DEPOSIT_FOR_ORGANIZATION = 'call create_fixed_deposit_for_existing_user_organization(%s,%s,%s,%s,%s,%s)'
GET_USER_ID_FROM_ACCOUNT_NUMBER = 'call get_user_id_from_account_number(%s)'
GET_FIXED_DEPOSIT_DETAILS = 'call get_fixed_accounts(%s)'
ADD_NEW_EMPLOYEE = 'call add_employee(%s,%s,%s,%s,%s,%s,%s,%s)'
GET_EMPLOYEE_DETAILS = 'SELECT employee_id,position,city FROM employee JOIN branch USING (branch_id) WHERE user_id = %s'
GET_REPORT_INTER_BRANCH = " call inter_bank_report(%s , %s , %s,%s,%s,%s); "
GET_REPORT_INTRA_BRANCH = "call intra_bank_report(%s,%s, %s,%s,%s,%s);"

SELECT_USERNAME = 'SELECT username FROM user WHERE username = %s'
SELECT_PASSWORD = 'SELECT password FROM user WHERE username = %s'

INSERT_USERS = "INSERT INTO user (username, password,user_type, first_name, last_name, date_of_birth, telephone, home_town) VALUES (%s,%s, %s, %s, %s, %s, %s, %s)"
CREATE_CUSTOMER_ACCOUNT = "INSERT INTO customer (user_id) VALUES (%s)"
# GET_USER_ACCOUNTS = 'SELECT account_number,account_type,balance FROM account WHERE user_id = %d'
GET_EMPLOYEE_ROLE = 'SELECT position FROM employee WHERE user_id = %d'
GET_USER_ACCOUNT_DETAILS = "SELECT user.first_name,user.last_name, user.home_town FROM account JOIN user USING (user_id) WHERE account_number = '%s'"


GET_BRANCH_ID_AND_NUMBER_OF_ACCOUNTS_AND_FULL_NAME = 'call get_branch_id_and_number_of_accounts_and_full_name(%s,%s)'

########################################### Quaries for account creation ###########################################

CREATE_SAVINGS_ACCOUNT_FOR_NEW_INDIVIDUAL_USER = 'call create_savings_account_for_new_individual_user(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
CREATE_CURRENT_ACCOUNT_FOR_NEW_INDIVIDUAL_USER = 'call create_current_account_for_new_individual_user(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
CREATE_SAVINGS_ACCOUNT_FOR_NEW_ORGANIZATION = 'call create_savings_account_for_new_organization_user(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
CREATE_CURRENT_ACCOUNT_FOR_NEW_ORGANIZATION = 'call create_current_account_for_new_organization_user(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
CREATE_SAVINGS_ACCOUNT_FOR_EXISTSING_INDIVIDUAL_USER = 'call create_savings_account_for_existing_individual_user(%s,%s,%s,%s)'
CREATE_CURRENT_ACCOUNT_FOR_EXISTSING_INDIVIDUAL_USER = 'call create_current_account_for_existing_individual_user(%s,%s,%s,%s)'
CREATE_FIXED_ACCOUNT_FOR_EXISTSING_INDIVIDUAL_USER = 'call create_fixed_account_for_existing_account_individual_user(%s,%s,%s,%s)'
CREATE_SAVINGS_ACCOUNT_FOR_EXISTSING_ORAGANIZATION_USER = 'call create_savings_account_for_existing_organization_user(%s,%s,%s,%s,%s)'