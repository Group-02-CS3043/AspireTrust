import MySQLdb
from MySQLdb.cursors import DictCursor
from MySQLdb import Connection
import bcrypt


SQL_FOR_INSERT_USERS = "INSERT INTO user (username, password, first_name, last_name, date_of_birth, telephone, home_town) VALUES (%s, %s, %s, %s, %s, %s, %s)"
SQL_FOR_CREATE_TABALE_USERS =         """
        CREATE TABLE IF NOT EXISTS user (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(60) NOT NULL,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            date_of_birth DATE NOT NULL,
            telephone VARCHAR(12) NOT NULL UNIQUE,
            home_town VARCHAR(50) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""

SQL_FOR_GETTING_PASSWORD = "SELECT password FROM user WHERE username = %s"


salt = bcrypt.gensalt()

configurations = {
    'host': 'localhost',
    'port': 3306,
    'user':'flask',
    'password':'Flask@123'
}

def get_hashed_password(plain_text_password:str)->str:
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())

def get_connection()->Connection:
    return MySQLdb.connect(**configurations, cursorclass=DictCursor)

def create_database(connection:Connection):
    try:
        connection.cursor().excute('CREATE DATABASE IF NOT EXISTS aspiretrust')
        connection.close()
        print('Database created successfully')
    except:
        print('Error while creating database')

def update_configurations(configurations:dict):
    configurations['database'] = 'aspiretrust'
    return configurations


def create_user_table(connection:Connection,table_query:str=SQL_FOR_CREATE_TABALE_USERS):
    try:
        connection.cursor().execute(table_query)
        connection.close()
        print('users table created successfully')
    except:
        print('Error while creating users table')




def insert_data(connection:Connection,query:str, values:tuple=())->bool:
    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        connection.close()
        print('Data inserted successfully')
        return True
    except MySQLdb.IntegrityError:
        print('Duplicate entry')
        return False
    except:
        print('Error while inserting data')
        return False
   


    
def return_query(connection:Connection,query:str, values:tuple=())->dict:
    try:
        cursor  = connection.cursor()
        cursor.execute(query, values)
        result = cursor.fetchall()
        connection.close()
        return result 
    except:
        print('Error while returning data')
        return None




configurations = update_configurations(configurations)
connection = get_connection()
create_user = insert_data(connection, SQL_FOR_INSERT_USERS, ('yasantha', get_hashed_password('Yasantha@123'), 'Yasantha', 'Perera', '1995-10-10', '071-1234567', 'Kandy'))
user_login = return_query(connection,SQL_FOR_GETTING_PASSWORD, ('yasantha',))
print(bcrypt.checkpw('Yasantha@123'.encode('utf-8'), user_login[0]['password'].encode('utf-8')))