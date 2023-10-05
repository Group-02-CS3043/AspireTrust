import bcrypt
from Database.connection import Connector

salt = bcrypt.gensalt()




class User:

    def __init__(self,username:str,password:str,connector:Connector) -> None:
        self.username = username
        self.password = password
        self.connector = connector

    def verify_user(self):
        try:
            self.connector.cursor.execute(f"SELECT password FROM Users WHERE username = '{self.username}'")
            password = self.connector.cursor.fetchone()[0]
            return (self.password == password)
        except Exception as e:
            print("Exception : ",e)
            return False
    

