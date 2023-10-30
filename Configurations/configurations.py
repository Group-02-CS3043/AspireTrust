from dotenv import load_dotenv
import os
from flask import request, redirect, session
from functools import wraps
from flask import session,redirect



global_configurations = {
    'PERMANENT_SESSION_LIFETIME':60
}

database_configurations = {
    'host':'localhost',
    'user':'flask',
    'password':'',
    'database':'aspiretrust',
}


load_dotenv()


def get_configurations()->dict:
    return global_configurations

def get_secret_key()->str:
    return os.environ.get("SECRET_KEY")

def get_database_configurations()->dict:
    database_configurations['password'] = os.environ.get("MYSQL_PASSWORD")
    return database_configurations



def valid_session(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session :
            print('user not in session')
            return redirect('/auth/login')
        return view_func(*args, **kwargs)
    return wrapped_view