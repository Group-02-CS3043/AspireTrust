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
    
    def __enter__(self):
        self.cursor = self.connect()
        return self.cursor
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()

    def connect(self):
        try:
            self.connection = MySQLdb.connect(*self.configurations.values(),cursorclass=Cursor,autocommit=True)
            self.cursor = self.connection.cursor()
            return self.cursor
        except Exception as e:
            print("Exception has happened in connect ! Error : ",e.message)
            return None


    