
SELECT_USERNAME = 'SELECT username FROM user WHERE username = %s'
SELECT_PASSWORD = 'SELECT password FROM user WHERE username = %s'
GET_USER_DETAILS = 'SELECT user_id,password,user_type FROM user WHERE username = %s'
INSERT_USERS = "INSERT INTO user (username, password,user_type, first_name, last_name, date_of_birth, telephone, home_town) VALUES (%s,%s, %s, %s, %s, %s, %s, %s)"
CREATE_CUSTOMER_ACCOUNT = "INSERT INTO customer (user_id) VALUES (%s)"
GET_USER_ACCOUNTS = 'SELECT account_number,account_type,balance FROM account WHERE user_id = %d'
GET_EMPLOYEE_ROLE = 'SELECT position FROM employee WHERE user_id = %d'
GET_USER_ACCOUNT_DETAILS = "SELECT CONCAT(user.first_name, ' ', user.last_name) AS fullname,account_number,balance FROM account JOIN user USING (user_id) WHERE account_number = '%s'"
GET_BRANCH = "SELECT b.city FROM user JOIN employee USING(user_id) JOIN branch b USING (branch_id) WHERE user_id = %d "