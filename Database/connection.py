import MySQLdb
from MySQLdb.cursors import DictCursor as Cursor
from MySQLdb.connections import Connection
from Configurations.configurations import get_database_configurations

class Connector:
    configurations:dict
    cursor : Cursor
    connection : Connection

    def __init__(self)->Cursor:
        try:
            self.configurations = get_database_configurations()
        
        except Exception as e:
            print("Exception has happened in initializing Connector ! Error : ",e)
            return None
        
    def connect(self):
        try:
            self.connection = MySQLdb.connect(*self.configurations.values(),cursorclass=Cursor)
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT VERSION()")
            print("Database version : ",self.cursor.fetchone()['VERSION()'])
        except Exception as e:
            print("Exception has happened in connect ! Error : ",e)
            return None


    