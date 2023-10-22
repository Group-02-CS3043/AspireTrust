SELECT_USERNAME = 'SELECT username FROM user WHERE username = %s'
SELECT_PASSWORD = 'SELECT password FROM user WHERE username = %s'
INSERT_USERS = "INSERT INTO user (username, password, first_name, last_name, date_of_birth, telephone, home_town) VALUES (%s, %s, %s, %s, %s, %s, %s)"
CREATE_CUSTOMER_ACCOUNT = "INSERT INTO customer (user_id) VALUES (%s)"