import bcrypt
from Database.connection import Connector

salt = bcrypt.gensalt()


class User:

    def __init__(self,username:str,password:str,connector:Connector) -> None:
        self.username = username
        self.password = password
        self.connector = connector

    def username_exists(self):
        try:
            self.connector.cursor.execute(f"SELECT username FROM Users WHERE username = '{self.username}'")
            return self.connector.cursor.fetchone() != None
        except Exception as e:
            print("Exception : ",e)
            return False

    def verify_user(self):
        try:
            self.connector.cursor.execute(f"SELECT password FROM Users WHERE username = '{self.username}'")
            password = self.connector.cursor.fetchone()[0]
            return (self.password == password)
        except Exception as e:
            print("Exception : ",e)
            return False
        
    def add_to_database(self):
        try:
            self.connector.cursor.execute(f"INSERT INTO Users(username,password) VALUES('{self.username}','{self.password}')")
            self.connector.connection.commit()
            return True
        except Exception as e:
            print("Exception : ",e)
            return False
    

