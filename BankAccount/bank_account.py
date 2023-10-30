from flask import Blueprint,render_template,session,abort,request,redirect,flash,url_for
from Settings.settings import *
from Configurations.configurations import valid_session,valid_employee
from Database.connection import Connector
from Database.database_quaries import *
from .models import Account,get_account_details,set_new_operation


bank_account_app = Blueprint('bank_account', __name__,template_folder='./templates',static_folder='static')


def check_firstname_and_last_name_exsists(first_name,last_name):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(CHECK_FIRSTNAME_AND_LASTNAME_EXISTS,(first_name,last_name,))
            return connector.cursor.fetchone() is not None
    except Exception as e:
        print("Error in check_firstname_and_last_name_exsists",e)
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


def get_customer_first_name_and_no_accounts(account_number):
    connector = Connector()
    try :
        with connector:
            print("account_number",account_number)
            connector.cursor.execute(GET_CUSTOMER_FIRSTNAME_AND_NUMBER_OF_ACCOUNTS ,(account_number,))
            return connector.cursor.fetchone()
    except Exception as e:
        print("Error in get_customer_first_name",e)
        return None

def get_savings_account_id(account_number):
    connector = Connector()
    try :
        with connector:
            connector.cursor.execute(GET_SAVINGS_ACCOUNT_ID,(account_number,))
            return connector.cursor.fetchone()
    except Exception as e:
        print("Error in get_savings_account_id",e)
        return None

def create_savings_account_for_exsisting_user_individual(user_id,account_number_of_new_account,account_number_of_old_account,amount):
    connector = Connector()
    try:
        with connector:
            print(user_id,account_number_of_new_account,account_number_of_old_account,'SAVINGS',amount)
            connector.cursor.execute(CREATE_BANK_ACCOUNT_FOR_EXISTING_USERS,(user_id,account_number_of_new_account,account_number_of_old_account,"SAVINGS",amount,))
            connector.connection.commit()
            return True
    except Exception as e:
        print("Error in create_savings_account_for_exsisting_user",e)
        return False

def create_current_account_for_exsisting_user_individual(user_id,account_number_of_new_account,account_number_of_old_account,amount):
    connector = Connector()
    try:
        with connector:
            print(user_id,account_number_of_new_account,account_number_of_old_account,'CURRENT',amount)
            connector.cursor.execute(CREATE_BANK_ACCOUNT_FOR_EXISTING_USERS,(user_id,account_number_of_new_account,account_number_of_old_account,"CURRENT",amount,))
            connector.connection.commit()
            return True
    except Exception as e:
        print("Error in create_current_account_for_exsisting_user",e)
        return False

def creat_fixed_account_for_for_exsisting_user_individual(user_id,savings_account_id,amount,duration):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(CREATE_FIXED_DEPOSIT,(user_id,savings_account_id,amount,duration,))
            connector.connection.commit()
            return True
    except Exception as e:
        print("Error in create_fixed_account_for_for_exsisting_user",e)
        return False

def create_savings_account_for_new_user_individual(first_name,last_name,branch_id,nic,telephone,home_town,date_of_birth,first_deposit,account_number):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(CREATE_BANK_ACCOUNT_FOR_NEW_USERS,(first_name,last_name,branch_id,nic,telephone,home_town,date_of_birth,first_deposit,account_number,'SAVINGS'))
            connector.connection.commit()
            return True
    except Exception as e:
        print("Error in create_savings_account_for_exsisting_user",e)
        return False


def create_current_account_for_new_user_individual(first_name,last_name,branch_id,nic,telephone,home_town,date_of_birth,first_deposit,account_number):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(CREATE_BANK_ACCOUNT_FOR_NEW_USERS,(first_name,last_name,branch_id,nic,telephone,home_town,date_of_birth,first_deposit,account_number,'CURRENT'))
            connector.connection.commit()
            return True
    except Exception as e:
        print("Error in create_current_account_for_exsisting_user",e)
        return False


@bank_account_app.route('/transfer',methods = DEFUALT_SUBMISSION_METHODS,endpoint='transfer')
@valid_session
def transaction():
    if request.method == 'POST':
        print(request.form['from_account_number'],request.form['to_account_number'],request.form['amount'])
        status = set_new_operation(request.form['from_account_number'],request.form['to_account_number'],request.form['amount'],request.form['remarks'])
        if status:
            flash("Transaction Successfull", 'Transaction')
            return redirect('/dashboard')
        else:
            flash("Transaction Failed", 'error')
            return redirect('/dashboard')
    if request.method == 'GET':
        context = get_account_details(session['user_id'])
        return render_template('bankAccount/transaction.html',context=context)
    


@bank_account_app.route('/create-exsisting',methods = DEFAULT_METHODS,endpoint='create_exsisiting_account')
@valid_employee
@valid_session
def create_account_for_exsisting_users():
    return render_template('bankAccount/existingUserCreateMain.html')

@bank_account_app.route('/create-new',methods = DEFAULT_METHODS,endpoint='create_new_account')
@valid_employee
@valid_session
def create_account_for_new_users_individual():
    return render_template('bankAccount/newUserCreationMain.html')

@bank_account_app.route('/create-exsisting/savings',methods = DEFUALT_SUBMISSION_METHODS,endpoint='create_savings_account_existing')
@valid_employee
@valid_session 
def create_saving_account_existing_individual():
    if request.method == 'POST':
        brach_id = get_branch_id(session['user_id'])
        first_name_and_no_of_accounts = get_customer_first_name_and_no_accounts(str(request.form['account_number']))
        if first_name_and_no_of_accounts is None:
            flash("User Doesn't Exists", 'Error')
            return redirect(url_for('bank_account.create_savings_account_existing'))
        ascii_values = [ord(char) for char in first_name_and_no_of_accounts['first_name']]
        new_account_number = f"{str(brach_id['branch_id'])}-{str(sum(ascii_values)%1000)}-{str(first_name_and_no_of_accounts['number_of_accounts']+1)}"
        if create_savings_account_for_exsisting_user_individual(session['user_id'],new_account_number,request.form['account_number'],request.form['first_deposit']):
            flash("Account Created Successfully", 'Account')
            return redirect('/dashboard')
        else:
            flash("Account Creation Failed", 'Error')
            return redirect('/dashboard')

    elif request.method == 'GET':
        return render_template('bankAccount/existingSavingIndividual.html')
    
@bank_account_app.route('/create-exsisting/current',methods = DEFUALT_SUBMISSION_METHODS,endpoint='create_current_account_existing')
@valid_employee
@valid_session
def create_current_account_existing_individual():
    if request.method == 'POST':
        brach_id = get_branch_id(session['user_id'])
        first_name_and_no_of_accounts = get_customer_first_name_and_no_accounts(str(request.form['account_number']))
        if first_name_and_no_of_accounts is None:
            flash("User Doesn't Exists", 'Error')
            return redirect(url_for('bank_account.create_current_account_existing'))
        ascii_values = [ord(char) for char in first_name_and_no_of_accounts['first_name']]
        new_account_number = f"{str(brach_id['branch_id'])}-{str(sum(ascii_values)%1000)}-{str(first_name_and_no_of_accounts['number_of_accounts']+1)}"
        if create_current_account_for_exsisting_user_individual(session['user_id'],new_account_number,request.form['account_number'],request.form['first_deposit']):
            flash("Account Created Successfully", 'Account')
            return redirect('/dashboard')
        else:
            flash("Account Creation Failed", 'Error')
            return redirect('/dashboard')

    elif request.method == 'GET':
        return render_template('bankAccount/existingCurrentIndividual.html')

@bank_account_app.route('/create-exsisting/fixed',methods = DEFUALT_SUBMISSION_METHODS,endpoint='create_fixed_account_exsisting')  
@valid_employee
@valid_session
def create_fixed_account_existing_individual():
    if request.method == 'POST':
        savings_account_id = get_savings_account_id(request.form['account_number'])
        if savings_account_id is None:
            flash("Savings Account doesn't Exists", 'Error')
            return redirect(url_for('bank_account.create_fixed_account_exsisting'))
        if creat_fixed_account_for_for_exsisting_user_individual(session['user_id'],savings_account_id['savings_account_id'],request.form['first_deposit'],request.form['duration']):
            flash("Fixed Deposit Created Successfully", 'Account')
            return redirect('/dashboard')
        else:
            flash("Fixed Deposit Creation Failed", 'Error')
            return redirect('/dashboard')
    elif request.method == 'GET':
        return render_template('bankAccount/existingFixedIndividual.html')

@bank_account_app.route('/create-new/savings',methods = DEFUALT_SUBMISSION_METHODS,endpoint='create_savings_account_new')
@valid_employee
@valid_session
def create_savings_account_new_individual():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        branch_id = request.form['branch_id']
        nic = request.form['nic']
        telephone = request.form['telephone']
        home_town = request.form['home_town']
        date_of_birth = request.form['date_of_birth']
        first_deposit = request.form['first_deposit']
        ascii_values = [ord(char) for char in (first_name+last_name)]
        new_account_number = f"{str(branch_id)}-{str(sum(ascii_values)%1000)}-{str(1)}"

        if check_firstname_and_last_name_exsists(first_name,last_name):
            flash("User Already Exists", 'Error')
            return redirect(url_for('bank_account.create_savings_account_new'))
        if create_savings_account_for_new_user_individual(first_name,last_name,branch_id,nic,telephone,home_town,date_of_birth,first_deposit,new_account_number):
            flash("Account Created Successfully","Account Creation")
            return redirect('/dashboard')
        else:
            flash("Error Occured ", "Error")
            return redirect('/dashboard')

    elif request.method == 'GET':
        context = get_branch_id(session['user_id'])
        print("context",context)
        return render_template('bankAccount/newSavingsIndividual.html',context=context)


@bank_account_app.route('/create-new/current',methods = DEFUALT_SUBMISSION_METHODS,endpoint='create_current_account_new')
@valid_employee
@valid_session
def create_current_account_new_individual():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        branch_id = request.form['branch_id']
        nic = request.form['nic']
        telephone = request.form['telephone']
        home_town = request.form['home_town']
        date_of_birth = request.form['date_of_birth']
        first_deposit = request.form['first_deposit']
        ascii_values = [ord(char) for char in (first_name+last_name)]
        new_account_number = f"{str(branch_id)}-{str(sum(ascii_values)%1000)}-{str(1)}"

        if check_firstname_and_last_name_exsists(first_name,last_name):
            flash("User Already Exists", 'Error')
            return redirect(url_for('bank_account.create_current_account_new'))
        if create_current_account_for_new_user_individual(first_name,last_name,branch_id,nic,telephone,home_town,date_of_birth,first_deposit,new_account_number):
            flash("Account Created Successfully","Account Creation")
            return redirect('/dashboard')
        else:
            flash("Error Occured ", "Error")
            return redirect('/dashboard')

    elif request.method == 'GET':
        context = get_branch_id(session['user_id'])
        print("context",context)
        return render_template('bankAccount/newSavingsIndividual.html',context=context)