from flask import Blueprint,render_template,session,redirect
from Settings.settings import *
from Configurations.configurations import valid_session
from Database.connection import Connector
from Database.database_quaries import *

dashboard_app = Blueprint('dashboard', __name__,template_folder='./templates',static_folder='static')

def get_account_details(user_id):
    connector = Connector()
    with connector:
        connector.cursor.execute(GET_USER_ACCOUNTS % user_id)
        return connector.cursor.fetchall()


def get_positoin_of_employee(user_id):
    connector = Connector()
    with connector:
        connector.cursor.execute(GET_EMPLOYEE_ROLE % user_id)
        return connector.cursor.fetchone()['position']

@dashboard_app.route('/',methods = DEFAULT_METHODS,endpoint='dashboard')
@valid_session
def dashboard():
    if session['user_role'] == 'CUSTOMER':
        context = get_account_details(session['user_id'])
        return render_template('customer_dashboard.html',context = context)
    elif session['user_role'] == 'EMPLOYEE':
        position = get_positoin_of_employee(session['user_id'])
        session['position'] = position
        if session['position'] == 'MANAGER':
            return render_template('manager_dashbaord.html')
        else :
            return render_template('employee_dashboard.html')

