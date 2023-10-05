from dotenv import load_dotenv
import os

global_configurations = {
    'PERMANENT_SESSION_LIFETIME':60
}

database_configurations = {
    'host':'localhost',
    'user':'flask',
    'password':'',
    'database':'flask',
}


load_dotenv()


def get_configurations()->dict:
    return global_configurations

def get_secret_key()->str:
    return os.environ.get("SECRET_KEY")

def get_database_configurations()->dict:
    database_configurations['password'] = os.environ.get("MYSQL_PASSWORD")
    return database_configurations