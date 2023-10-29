from flask import Flask,session,render_template,Blueprint,request
from Settings.settings import *
from Configurations.configurations import valid_session
from Database.connection import Connector
from Database.database_quaries import *


user_app = Blueprint('user', __name__,template_folder='./templates',static_folder='static')

def get_user__account_details(account_number):
    connector = Connector()
    with connector:
        connector.cursor.execute(GET_USER_ACCOUNT_DETAILS % account_number)
        return connector.cursor.fetchone()
    
@user_app.route('/account_details',methods = DEFUALT_SUBMISSION_METHODS,endpoint='user_account_details')
def user_account_details():
    if request.method == 'POST':
        account_number = request.form['account_number']
        context = get_user__account_details(account_number)
        print(context)
        return render_template('user_details.html',context = context)