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

SELECT_USERNAME = 'SELECT username FROM user WHERE username = %s'
SELECT_PASSWORD = 'SELECT password FROM user WHERE username = %s'

INSERT_USERS = "INSERT INTO user (username, password,user_type, first_name, last_name, date_of_birth, telephone, home_town) VALUES (%s,%s, %s, %s, %s, %s, %s, %s)"
CREATE_CUSTOMER_ACCOUNT = "INSERT INTO customer (user_id) VALUES (%s)"
# GET_USER_ACCOUNTS = 'SELECT account_number,account_type,balance FROM account WHERE user_id = %d'
GET_EMPLOYEE_ROLE = 'SELECT position FROM employee WHERE user_id = %d'
GET_USER_ACCOUNT_DETAILS = "SELECT CONCAT(user.first_name, ' ', user.last_name) AS fullname,account_number,balance FROM account JOIN user USING (user_id) WHERE account_number = '%s'"
GET_BRANCH = "SELECT b.city FROM user JOIN employee USING(user_id) JOIN branch b USING (branch_id) WHERE user_id = %d "