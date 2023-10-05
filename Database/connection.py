import MySQLdb
from MySQLdb.cursors import Cursor
from Configurations.configurations import get_database_configurations

class Connector:
    configurations:dict
    cursor = None
    connection = None

    def __init__(self)->Cursor:
        try:
            self.configurations = get_database_configurations()
        
        except Exception as e:
            print("Exception : ",e)
            return None
        
    def connect(self):
        try:
            self.connection = MySQLdb.connect(*self.configurations.values())
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT VERSION()")
            print("Database version : ",self.cursor.fetchone()[0])
        except Exception as e:
            print("Exception : ",e)
            return None


    