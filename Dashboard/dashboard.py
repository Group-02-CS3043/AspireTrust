from flask import Blueprint,render_template,session,redirect,flash
from Settings.settings import *
from Configurations.configurations import valid_session
from Database.connection import Connector
from Database.database_quaries import *

dashboard_app = Blueprint('dashboard', __name__,template_folder='./templates',static_folder='static')

def get_account_details(user_id):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(GET_ACCOUNT_DETAILS,(user_id,))
            return connector.cursor.fetchall()
        
    except Exception as e:
        print("Error in get_account_details",e)
        return None

def get_first_name(user_id):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(GET_FIRSTNAME_FROM_USER_ID,(user_id,))
            return connector.cursor.fetchone()['first_name']
    except Exception as e:
        print("Error in get_first_name",e)
        return None


def get_positoin_of_employee(user_id):
    connector = Connector()
    with connector:
        connector.cursor.execute(GET_EMPLOYEE_ROLE % user_id)
        return connector.cursor.fetchone()['position']


def get_user_first_name(user_id):
    connector = Connector()
    with connector:
        connector.cursor.execute(GET_FIRSTNAME_FROM_USER_ID,(user_id,))
        return connector.cursor.fetchone()


@dashboard_app.route('/',methods = DEFAULT_METHODS,endpoint='dashboard')
@valid_session
def dashboard():
    if session['user_role'] == 'CUSTOMER':
        context = {}
        context['accounts'] = get_account_details(session['user_id'])
        print("context",context)
        context['first_name'] = get_first_name(session['user_id'])
        
        return render_template('dashboard/customer_dashboard.html',context = context)
    elif session['user_role'] == 'EMPLOYEE':
        position = get_positoin_of_employee(session['user_id'])
        session['position'] = position
        context = get_user_first_name(session['user_id'])
        print("context",context)
        if session['position'] == 'MANAGER':
            return render_template('dashboard/manager_dashbaord.html',context=context)
        else :
            return render_template('dashboard/employee_dashboard.html',context=context)

