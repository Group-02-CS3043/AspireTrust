import bcrypt
from Database.connection import Connector
from Database.database_quaries import *


salt = bcrypt.gensalt()




# class User:
#     username:str
#     password:str
#     connector:Connector
#     data:dict

#     def __init__(self,data:dict,connector:Connector) -> None:
#         try:
#             self.data = data
#             self.username = data['username']
#             self.password = data['password']
#             self.connector = connector
#         except Exception as e:
#             print("Exception has happened in initializing User ! Error : ",e)
#             return None

#     def username_exists(self):
#         try:
#             with self.connector:
#                 self.connector.cursor.execute(SELECT_USERNAME, (self.username,))
#                 # print(self.connector.cursor.fetchone())
#                 return self.connector.cursor.fetchone() != None
#         except Exception as e:
#             print("Exception has happened in username exsit ! Error : ",e)
#             return False

#     def verify_user(self):
#         try:
#             with self.connector:
#                 self.connector.cursor.execute(GET_USER_DETAILS, (self.username,))
#                 self.user_id,password, self.user_role = self.connector.cursor.fetchone().values()
#                 if password == None:
#                     return False
#                 else:
#                     return password == self.password
#                 # return bcrypt.checkpw(self.password.encode('utf-8'), password.encode('utf-8'))
#         except Exception as e:
#             print("Exception has happened in verify_user ! Error : ",e)
#             return False



#     def add_to_database(self):
#         try:
#             username = self.data['username']
#             first_name = self.data['first-name']
#             last_name = self.data['last-name']
#             date_of_birth = self.data['birthday']
#             email = self.data['email']
#             telephone = self.data['telephone']
#             home_town = self.data['home-town']
#             password = bcrypt.hashpw(self.data['password'].encode('utf-8'), bcrypt.gensalt())
#             with self.connector:
#                 self.connector.cursor.execute(INSERT_USERS, (username, password, first_name, last_name, date_of_birth, telephone, home_town))
#                 self.connector.cursor.execute(CREATE_CUSTOMER_ACCOUNT, (self.connector.cursor.lastrowid,))
#                 self.connector.connection.commit()
#                 return True
#         except Exception as e:
#             print("Exception has happened in add_to_database ! Error : ",e)
#             return False
    

# def find_user_acount_from_account_number(account_number,connector):
#         try:
#             with connector:
#                 connector.cursor.execute(CHECK_FROM_ACCOUNT_NUMBER, (account_number,))
#                 if connector.cursor.fetchone() != None:
#                     return True
#                 else:
#                     redirect('auth.login')

#         except Exception as e:
#             print("Exception has happened in verify_user ! Error : ",e)
#             return False

def is_account_exsists(account_number:str,connector:Connector)->bool:
    try:
        with connector:
            connector.cursor.execute(CHECK_FROM_ACCOUNT_NUMBER, (account_number,))
            user_id = connector.cursor.fetchone()
            if user_id:
                return user_id['user_id']
            else:
                return False

    except Exception as e:
        print("Exception has happened in verify_user ! Error : ",e)
        return False

def have_a_user_account(user_id:int,connector:Connector)->bool:
    try:
        with connector:
            connector.cursor.execute(CHECK_WETHER_USER_IS_ALREADY_HAVE_A_REGISTERED_ACCOUNT,(user_id,))
            username = connector.cursor.fetchone()
            return username['username']
    except Exception as e:
        print("Eror happened when checking user has already registered : ",e)

def is_user_exsists(username:str,connector:Connector)->bool:
    try:
        with connector:
            connector.cursor.execute(VERIFY_USER_EXSISTS,(username,))
            return connector.cursor.fetchone() != None
    except Exception as e:
        print("Exception has happened in verify_user ! Error : ",e)
        return False

def authenticate_user(data:dict,connector:Connector)->int:
    try:
        with connector:
            username = data['username']
            password = data['password']
            connector.cursor.execute(AUTHENTICATE_USER, (data['username'],data['password'],))
            user_id = connector.cursor.fetchone()
            if user_id:
                return user_id['user_id']
            else:
                return None
            
    except Exception as e:
        print("Exception has happened in verify_user ! Error : ",e)
        return 0
    

def get_user_role(user_id:int,connector:Connector):
    try:
        with connector:
            connector.cursor.execute(GET_THE_USER_ROLE,(user_id,))
            return connector.cursor.fetchone()['user_type']
    except Exception as e:
        print("Exception has happened in get_user_role ! Error : ",e)
        return None
    
def create_user(username:str,password:str,account_number:str,connector:Connector):
    try:
        with connector:
            connector.cursor.execute(CREATE_USER_ACCOUNT_FROM_ACCOUNT_NUMBER,(username,password,account_number,))
            connector.connection.commit()
            connector.cursor.execute(CHECK_FROM_ACCOUNT_NUMBER,(account_number,))
            user_id = connector.cursor.fetchone()
            print(user_id)
            return user_id['user_id']
    except Exception as e:
        print("Error happened in creating User :",e)
        return None