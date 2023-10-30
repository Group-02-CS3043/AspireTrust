from flask import Flask,session,render_template,Blueprint,request,redirect
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
    

def get_user_informations(user_id):
    connector = Connector()
    with connector:
        connector.cursor.execute(GET_USER_INFORMATIONS % user_id)
        return connector.cursor.fetchone()
    

def update_user_details(user_id,first_name,last_name,date_of_birth,telephone,home_town):
    connector = Connector()
    with connector:
        connector.cursor.execute(UPDATE_USER_DETAILS ,(user_id,first_name,last_name,date_of_birth,telephone,home_town))
        connector.connection.commit()


@user_app.route('/account_details',methods = DEFUALT_SUBMISSION_METHODS,endpoint='user_account_details')
@valid_session
def user_account_details():
    if request.method == 'POST':
        account_number = request.form['account_number']
        context = get_user__account_details(account_number)
        print(context)
        return render_template('user_details.html',context = context)
    

@user_app.route('/details',methods = DEFUALT_SUBMISSION_METHODS,endpoint='user_informations')
@valid_session
def user_informations():
    if request.method == 'GET':
        context = get_user_informations(session['user_id'])
        return render_template('user/settings.html',context=context)
    if request.method == 'POST':
        print(request.form)
        update_user_details(session['user_id'],request.form['first_name'],request.form['last_name'],request.form['date_of_birth'],request.form['telephone'],request.form['home_town'])
        return redirect('/dashboard')