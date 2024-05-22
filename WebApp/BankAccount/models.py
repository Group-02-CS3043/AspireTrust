from Database.connection import Connector
from Database.database_quaries import *

class Account:
    connector:Connector
    def __init__(self) -> None:
        self.connector = Connector()
        self.connector.connect()
        
    def validate_details(self,form:dict):
        valid = True
        self.first_name = form['first_name']
        self.last_name = form['last_name']
        self.date_of_birth = form['birth_date']
        self.telephone = form['phone_number']
        self.email = form['email']
        self.home_town = form['home_town']
        self.username = self.first_name + self.last_name
        self.password = "sdasmkfkms"
        self.user_type = "CUSTOMER"


    def create_new_user(self):
        try:
            with self.connector:
                self.connector.cursor.execute(INSERT_USERS, (self.username, self.password,self.user_type, self.first_name, self.last_name, self.date_of_birth, self.telephone, self.home_town))
                self.connector.connection.commit()
                return True
        except Exception as e:
            print("Exception has happened in create_new_user ! Error : ",e)
            return False
        


def get_account_details(user_id):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(GET_USER_ACCOUNTS,(user_id,))
            details = connector.cursor.fetchall()
            return details
    except Exception as e:
        print("Exception has happened in get_account_details ! Error : ",e)
        return False
    

def set_new_operation(from_account_number,to_account_number,amount,remark):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(CREATE_TRANSACTION,(from_account_number,to_account_number,amount,remark))
            connector.connection.commit()
            return True
    except Exception as e:
        print("Exception has happened in set_new_operation ! Error : ",e)
        return False