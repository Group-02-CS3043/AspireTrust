from flask import Flask,session,render_template,Blueprint,request,redirect,flash,url_for
from Settings.settings import *
from Configurations.configurations import valid_session,valid_manager
from Database.connection import Connector
from Database.database_quaries import *
from Dashboard.dashboard import get_loan_details


user_app = Blueprint('user', __name__,template_folder='./templates',static_folder='static')

def get_emplyee_details(user_id):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(GET_EMPLOYEE_DETAILS,(user_id,))
            return connector.cursor.fetchone()
    except Exception as e:
        print("Error in get_emplyee_details",e)
        return None


def get_branch_id(user_id):
    connector = Connector()
    try :
        with connector:
            connector.cursor.execute(GET_BRANCH_ID % user_id)
            return connector.cursor.fetchone()
    except Exception as e:
        print("Error in get_branch_id",e)
        return None


def check_firstname_and_last_name_exsists(first_name,last_name):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(CHECK_FIRSTNAME_AND_LASTNAME_EXISTS,(first_name,last_name,))
            return connector.cursor.fetchone() is not None
    except Exception as e:
        print("Error in check_firstname_and_last_name_exsists",e)
        return None


def create_new_employee_account(manager_user_id,first_name,last_name,nic,date_of_birth,telephone,home_town,role):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(ADD_NEW_EMPLOYEE,(manager_user_id,first_name,last_name,nic,telephone,home_town,date_of_birth,role))
            connector.connection.commit()
            return True
    except Exception as e:
        print("Exception has happened in create_new_user ! Error : ",e)
        return False
 

def get_user__account_details(account_number):
    connector = Connector()
    with connector:
        connector.cursor.execute(GET_USER_ACCOUNT_DETAILS % account_number)
        return connector.cursor.fetchone()
    
def get_accounts_details(user_id):
    connector = Connector()
    with connector:
        connector.cursor.execute(GET_ACCOUNT_DETAILS,(user_id,))
        return connector.cursor.fetchall()

def get_user_informations(user_id):
    connector = Connector()
    with connector:
        connector.cursor.execute(GET_USER_INFORMATIONS,(user_id,))
        return connector.cursor.fetchone()
    
def get_user_id_from_account_number(account_number):
    connector = Connector()
    with connector:
        connector.cursor.execute(GET_USER_ID_FROM_ACCOUNT_NUMBER,(account_number,))
        return connector.cursor.fetchone()

def update_user_details(user_id,first_name,last_name,date_of_birth,telephone,home_town):
    connector = Connector()
    with connector:
        connector.cursor.execute(UPDATE_USER_DETAILS ,(user_id,first_name,last_name,date_of_birth,telephone,home_town))
        connector.connection.commit()

def get_fd_accounts(user_id):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(GET_FIXED_DEPOSIT_DETAILS,(user_id,))
            return connector.cursor.fetchall()
    except Exception as e:
        print("Error in get_fd_accounts",e)
        return False


@user_app.route('/account_details',methods = DEFUALT_SUBMISSION_METHODS,endpoint='user_account_details')
@valid_session
def user_account_details():
    if request.method == 'POST':
        account_number = request.form['account_number']
        user_id = get_user_id_from_account_number(account_number)
        if user_id == None:
            flash("Invalid Account Number","Error")
            return redirect('/dashboard')
        context = get_user__account_details(account_number)
        context['accounts'] = get_accounts_details(user_id['user_id'])
        context['fd_accounts'] = get_fd_accounts(user_id['user_id'])
        context['loans'] = get_loan_details(user_id['user_id'])
        print(context)
        return render_template('user_details.html',context = context)
    

@user_app.route('/details',methods = DEFUALT_SUBMISSION_METHODS,endpoint='user_informations')
@valid_session
def user_informations():
    if request.method == 'GET':
        context = get_user_informations(session['user_id'])
        employee_details = get_emplyee_details(session['user_id'])
        if employee_details != None:
            context['employee_details'] = employee_details
        print(context)
        return render_template('user/settings.html',context=context)
    if request.method == 'POST':
        print(request.form)
        update_user_details(session['user_id'],request.form['first_name'],request.form['last_name'],request.form['date_of_birth'],request.form['telephone'],request.form['home_town'])
        return redirect('/dashboard')
    

@user_app.route('/add-emplyee',methods = DEFUALT_SUBMISSION_METHODS,endpoint='add_employee')
@valid_manager
@valid_session
def add_employee():
    if request.method == 'GET':
        context = get_branch_id(session['user_id'])
        return render_template('createAccount/employeeAdding.html',context=context)
    elif request.method == 'POST':
        if check_firstname_and_last_name_exsists(request.form['first_name'],request.form['last_name']):
            flash("Employee Already Exists","Error")
            return redirect(url_for('user.add_employee'))
        elif create_new_employee_account(session['user_id'],request.form['first_name'],request.form['last_name'],request.form['nic'],request.form['date_of_birth'],request.form['telephone'],request.form['home_town'],request.form['role']):
            flash("Employee Account Created Successfully","Success")
            return redirect('/dashboard')
        else:
            flash("Something went wrong","Error")
            return redirect('/dashboard')