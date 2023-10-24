import bcrypt
from Database.connection import Connector
from Database.database_quaries import *

INSERT_USERS = "INSERT INTO user (username, password, first_name, last_name, date_of_birth, telephone, home_town) VALUES (%s, %s, %s, %s, %s, %s, %s)"
salt = bcrypt.gensalt()


class User:
    username:str
    password:str
    connector:Connector
    data:dict

    def __init__(self,data:dict,connector:Connector) -> None:
        try:
            self.data = data
            self.username = data['username']
            self.password = data['password']
            self.connector = connector
        except Exception as e:
            print("Exception has happened in initializing User ! Error : ",e)
            return None

    def username_exists(self):
        try:
            with self.connector:
                self.connector.cursor.execute(SELECT_USERNAME, (self.username,))
                # print(self.connector.cursor.fetchone())
                return self.connector.cursor.fetchone() != None
        except Exception as e:
            print("Exception has happened in username exsit ! Error : ",e)
            return False

    def verify_user(self):
        try:
            with self.connector:
                self.connector.cursor.execute(GET_USER_DETAILS, (self.username,))
                self.user_id,password, self.user_role = self.connector.cursor.fetchone().values()
                if password == None:
                    return False
                else:
                    return password == self.password
                # return bcrypt.checkpw(self.password.encode('utf-8'), password.encode('utf-8'))
        except Exception as e:
            print("Exception has happened in verify_user ! Error : ",e)
            return False
        
    def add_to_database(self):
        try:
            username = self.data['username']
            first_name = self.data['first-name']
            last_name = self.data['last-name']
            date_of_birth = self.data['birthday']
            email = self.data['email']
            telephone = self.data['telephone']
            home_town = self.data['home-town']
            password = bcrypt.hashpw(self.data['password'].encode('utf-8'), bcrypt.gensalt())
            with self.connector:
                self.connector.cursor.execute(INSERT_USERS, (username, password, first_name, last_name, date_of_birth, telephone, home_town))
                self.connector.cursor.execute(CREATE_CUSTOMER_ACCOUNT, (self.connector.cursor.lastrowid,))
                self.connector.connection.commit()
                return True
        except Exception as e:
            print("Exception has happened in add_to_database ! Error : ",e)
            return False
    
