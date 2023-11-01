from flask import Blueprint,render_template,session,abort,request,redirect,flash,url_for
from Settings.settings import *
from Configurations.configurations import valid_session,valid_employee
from Database.connection import Connector
from Database.database_quaries import *
from .models import Account,get_account_details,set_new_operation
from datetime import datetime
from MySQLdb import MySQLError


bank_account_app = Blueprint('bank_account', __name__,template_folder='./templates',static_folder='static')

def get_user_id_from_account_number(account_number):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(GET_USER_ID_FROM_ACCOUNT_NUMBER,(account_number,))
            return connector.cursor.fetchone()
    except Exception as e:
        print("Error in get_user_id_from_account_number",e)
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

def get_branch_id(user_id):
    connector = Connector()
    try :
        with connector:
            connector.cursor.execute(GET_BRANCH_ID % user_id)
            return connector.cursor.fetchone()
    except Exception as e:
        print("Error in get_branch_id",e)
        return None


def get_branch_id_and_number_of_accounts_and_full_name(user_id,account_number):
    connector = Connector()
    try :
        with connector:
            connector.cursor.execute(GET_BRANCH_ID_AND_NUMBER_OF_ACCOUNTS_AND_FULL_NAME,(account_number,user_id,))
            return connector.cursor.fetchone()
    except Exception as e:
        error_code, error_message = e.args
        flash(error_message,"Error")
        

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




    

    









@bank_account_app.route('/transfer',methods = DEFUALT_SUBMISSION_METHODS,endpoint='transfer')
@valid_session
def transaction():
    if request.method == 'POST':
        print(request.form['from_account_number'],request.form['to_account_number'],request.form['amount'])
        user_id = get_user_id_from_account_number(request.form['to_account_number'])
        if user_id is None:
            flash("Given Account Number doesn't exists", 'Error')
            return redirect(url_for('bank_account.transfer'))
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


    



    


# @bank_account_app.route('/organization/current/exsisting',methods = DEFUALT_SUBMISSION_METHODS,endpoint='create_current_account_exsisting_org')  
# @valid_employee
# @valid_session
# def create_current_account_existing_organization():
#     if request.method == 'POST':
#         brach_id = get_branch_id(session['user_id'])
#         savings_account_id = get_savings_account_id(request.form['account_number'])
#         organization_name = request.form['organization_name']
#         organization_role = request.form['organization_role']
#         first_name_and_no_of_accounts = get_customer_first_name_and_no_accounts(str(request.form['account_number']))
#         if first_name_and_no_of_accounts is None:
#             flash("User Doesn't Exists", 'Error')
#             return redirect(url_for('bank_account.create_current_account_exsisting_org'))
#         ascii_values = [ord(char) for char in first_name_and_no_of_accounts['first_name']]
#         new_account_number = f"{str(brach_id['branch_id'])}-{str(sum(ascii_values)%1000)}-{str(first_name_and_no_of_accounts['number_of_accounts']+1)}"
#         if savings_account_id is None:
#             flash("Current Account doesn't Exists", 'Error')
#             return redirect(url_for('bank_account.create_current_account_organization_new'))
#         if creat_current_account_for_for_exsisting_user_organization(session['user_id'],new_account_number,request.form['account_number'],request.form['first_deposit'],organization_name,organization_role):
#             flash("Account Created Successfully","Account Creation")
#             context = {'account_number':new_account_number,'account_type':'SAVINGS','created_at':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'full_name':f'{first_name} {last_name}'}
#             return render_template('bankAccount/displayCreatedAccount.html',context=context)
#         else:
#             flash("Current Account Creation Failed", 'Error')
#             return redirect('/dashboard')
#     elif request.method == 'GET':
#         return render_template('bankAccount/existingCurrentOrganization.html')
    





    




 

def get_account_number(first_name,last_name,branch_id,number_of_accounts = 1):
        ascii_values = [ord(char) for char in (first_name+last_name)]
        return f'{branch_id:03}-{sum(ascii_values)%1000:03}-{number_of_accounts+1:03}'


######################################################## Individual Account Creation ########################################################
######################################################## New User Account Creation ########################################################
######################################################## Savings Account Creation ########################################################


def create_savings_account_for_new_user_individual(first_name,last_name,branch_id,nic,telephone,home_town,date_of_birth,first_deposit,account_number):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(CREATE_SAVINGS_ACCOUNT_FOR_NEW_INDIVIDUAL_USER,(first_name,last_name,branch_id,nic,telephone,home_town,date_of_birth,first_deposit,account_number,))
            context = connector.cursor.fetchone()
            flash("Account Created Successfully", 'Account')
            return render_template('bankAccount/displayCreatedAccount.html',context=context)
            
    except MySQLError as e:
        error_code, error_message = e.args
        flash(error_message,"Error")
        return redirect(url_for('bank_account.create_savings_account_for_new_individual_user'))
    
    except Exception as e:
        flash("Unkown Error occured","Error")
        return redirect(url_for('dashboard.dashboard'))
    

@bank_account_app.route('/individual/savings/new',methods = DEFUALT_SUBMISSION_METHODS,endpoint='create_savings_account_for_new_individual_user')
@valid_employee
def create_savings_account_for_new_individual_user():
    if request.method == 'POST':
        first_name, last_name, branch_id, nic, telephone, home_town, date_of_birth, first_deposit = (request.form[key] for key in ['first_name', 'last_name', 'branch_id', 'nic', 'telephone', 'home_town', 'date_of_birth', 'first_deposit'])
        account_number = get_account_number(first_name,last_name,branch_id)
        return create_savings_account_for_new_user_individual(first_name,last_name,branch_id,nic,telephone,home_town,date_of_birth,first_deposit,account_number)
    
    elif request.method == 'GET':
        context = get_branch_id(session['user_id'])
        return render_template('bankAccount/newSavingsIndividual.html',context=context)
    

######################################################## Current Account Creation ########################################################

def create_current_account_for_new_user_individual(first_name,last_name,branch_id,nic,telephone,home_town,date_of_birth,first_deposit,account_number):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(CREATE_CURRENT_ACCOUNT_FOR_NEW_INDIVIDUAL_USER,(first_name,last_name,branch_id,nic,telephone,home_town,date_of_birth,first_deposit,account_number,))
            context = connector.cursor.fetchone()
            flash("Account Created Successfully", 'Account')
            return render_template('bankAccount/displayCreatedAccount.html',context=context)
    except MySQLError as e:
        error_code, error_message = e.args
        flash(error_message,"Error")
        return redirect(url_for('bank_account.create_current_account_for_new_individual_user'))
    except Exception as e:
        flash("Unkown Error occured","Error")
        return redirect(url_for('dashboard.dashboard'))

@bank_account_app.route('/individual/current/new',methods = DEFUALT_SUBMISSION_METHODS,endpoint='create_current_account_for_new_individual_user')
@valid_employee
def create_current_account_for_new_individual_user():
    if request.method == 'POST':
        first_name, last_name, branch_id, nic, telephone, home_town, date_of_birth, first_deposit = (request.form[key] for key in ['first_name', 'last_name', 'branch_id', 'nic', 'telephone', 'home_town', 'date_of_birth', 'first_deposit'])
        account_number = get_account_number(first_name,last_name,branch_id)
        return create_current_account_for_new_user_individual(first_name,last_name,branch_id,nic,telephone,home_town,date_of_birth,first_deposit,account_number)

    elif request.method == 'GET':
        context = get_branch_id(session['user_id'])
        return render_template('bankAccount/newSavingsIndividual.html',context=context)
    

######################################################## Existing User Account Creation ################################################################################    
####################################################### Savings Account Creation ########################################################

def create_savings_account_for_exsisting_user_individual(user_id,account_number_of_new_account,account_number_of_old_account,amount):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(CREATE_SAVINGS_ACCOUNT_FOR_EXISTSING_INDIVIDUAL_USER,(user_id,account_number_of_new_account,account_number_of_old_account,amount,))
            context = connector.cursor.fetchone()
            flash("Account Created Successfully", 'Account')
            return render_template('bankAccount/displayCreatedAccount.html',context=context)
    except MySQLError as e:
        error_code, error_message = e.args
        flash(error_message,"Error")
        return redirect(url_for('bank_account.create_saving_account_for_existing_individual_user'))
    
    except Exception as e:
        flash("Unkown Error occured","Error")
        return redirect(url_for('dashboard.dashboard'))


@bank_account_app.route('individual/savings/existing',methods = DEFUALT_SUBMISSION_METHODS,endpoint='create_saving_account_for_existing_individual_user')
@valid_employee
def create_saving_account_for_existing_individual_user():
    if request.method == 'POST':
        data = get_branch_id_and_number_of_accounts_and_full_name(session['user_id'],request.form['account_number'])
        if data is None:
            return redirect(url_for('bank_account.create_saving_account_for_existing_individual_user'))
    
        branch_id,number_of_accounts,full_name = (data[key] for key in ['branch_id','number_of_accounts','full_name'])
        new_account_number = get_account_number(full_name,"",branch_id,number_of_accounts=number_of_accounts)
        return create_savings_account_for_exsisting_user_individual(session['user_id'],new_account_number,request.form['account_number'],request.form['first_deposit'])

    elif request.method == 'GET':
        return render_template('bankAccount/existingSavingIndividual.html')
    

######################################################## Current Account Creation ########################################################


def create_current_account_for_exsisting_user_individual(user_id,account_number_of_new_account,account_number_of_old_account,amount):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(CREATE_CURRENT_ACCOUNT_FOR_EXISTSING_INDIVIDUAL_USER,(user_id,account_number_of_new_account,account_number_of_old_account,amount,))
            context = connector.cursor.fetchone()
            print("context",context)
            flash("Account Created Successfully", 'Account')
            return render_template('bankAccount/displayCreatedAccount.html',context=context)
    except Exception as e:
        error_code, error_message = e.args
        flash(error_message,"Error")
        return redirect(url_for('bank_account.create_current_account_for_existing_individual_user'))


@bank_account_app.route('individuals/current/exsisting',methods = DEFUALT_SUBMISSION_METHODS,endpoint='create_current_account_for_existing_individual_user')
@valid_employee
def create_current_account_for_existing_individual_user():
    if request.method == 'POST':
        data = get_branch_id_and_number_of_accounts_and_full_name(session['user_id'],request.form['account_number'])
        print(data)
        if data is None:
            return redirect(url_for('bank_account.create_current_account_for_existing_individual_user'))
            
        branch_id,number_of_accounts,full_name = (data[key] for key in ['branch_id','number_of_accounts','full_name'])
        new_account_number = get_account_number(full_name,"",branch_id,number_of_accounts=number_of_accounts)
        return create_current_account_for_exsisting_user_individual(session['user_id'],new_account_number,request.form['account_number'],request.form['first_deposit'])
    elif request.method == 'GET':
        return render_template('bankAccount/existingCurrentIndividual.html')
    
##################################################### Fixed Account Creation ########################################################


def creat_fixed_account_for_for_exsisting_user_individual(user_id,savings_account_number,amount,duration):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(CREATE_FIXED_ACCOUNT_FOR_EXISTSING_INDIVIDUAL_USER,(user_id,savings_account_number,amount,duration,))
            context = connector.cursor.fetchone()
            flash("Account Created Successfully", 'Account')
            return render_template('bankAccount/displayCreatedAccount.html',context=context)
    except MySQLError as e:
        error_code, error_message = e.args
        flash(error_message,"Error")
        return redirect(url_for('bank_account.create_fixed_account_for_existing_individual_user'))
    except Exception as e:
        flash("Unkown Error occured","Error")
        return redirect(url_for('dashboard.dashboard'))

@bank_account_app.route('/individuals/fixed/existing',methods = DEFUALT_SUBMISSION_METHODS,endpoint='create_fixed_account_for_existing_individual_user')  
@valid_employee
def create_fixed_account_for_existing_individual_user():
    if request.method == 'POST':
        savings_account_number,first_deposit,duration = (request.form[key] for key in ['account_number','first_deposit','duration'])
        return creat_fixed_account_for_for_exsisting_user_individual(session['user_id'],savings_account_number,first_deposit,duration)
    elif request.method == 'GET':
        return render_template('bankAccount/existingFixedIndividual.html')
    

########################################################## Organization Account Creation ##########################################################
########################################################## New User Account Creation ##########################################################
########################################################## Savings Account Creation ##########################################################

def create_savings_account_for_new_organization_user(first_name,last_name,branch_id,nic,telephone,home_town,date_of_birth,first_deposit,account_number,organization_name,organization_role):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(CREATE_SAVINGS_ACCOUNT_FOR_NEW_ORGANIZATION,(first_name,last_name,branch_id,nic,telephone,home_town,date_of_birth,first_deposit,account_number,organization_name,organization_role,))
            context = connector.cursor.fetchone()
            flash("Account Created Successfully", 'Account')
            return render_template('bankAccount/displayCreatedAccount.html',context=context)
    except MySQLError as e:
        error_code, error_message = e.args
        flash(error_message,"Error")
        return redirect(url_for('bank_account.create_savings_account_for_new_organization'))
    
    except Exception as e:
        flash("Unkown Error occured","Error")
        return redirect(url_for('dashboard.dashboard'))


@bank_account_app.route('/organization/savings/new',methods = DEFUALT_SUBMISSION_METHODS,endpoint='create_savings_account_for_new_organization')
@valid_employee
def create_savings_account_for_new_organization():
    if request.method == 'POST':
        first_name, last_name, branch_id, nic, telephone, home_town, date_of_birth, first_deposit, organization_name, organization_role = (request.form[key] for key in ['first_name', 'last_name', 'branch_id', 'nic', 'telephone', 'home_town', 'date_of_birth', 'first_deposit', 'organization_name', 'organization_role'])
        account_number = get_account_number(first_name,last_name,branch_id,number_of_accounts=1)
        print(account_number)
        return create_savings_account_for_new_organization_user(first_name,last_name,branch_id,nic,telephone,home_town,date_of_birth,first_deposit,account_number,organization_name,organization_role)

    elif request.method == 'GET':
        context = get_branch_id(session['user_id'])
        print("context",context)
        return render_template('bankAccount/newSavingsOrganization.html',context=context)
    

########################################################## Current Account Creation ##########################################################
def create_current_account_for_new_organization_user(first_name,last_name,branch_id,nic,telephone,home_town,date_of_birth,first_deposit,account_number,organization_name,organization_role):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(CREATE_CURRENT_ACCOUNT_FOR_NEW_ORGANIZATION,(first_name,last_name,branch_id,nic,telephone,home_town,date_of_birth,first_deposit,account_number,organization_name,organization_role,))
            context = connector.cursor.fetchone()
            flash("Account Created Successfully", 'Account')
            return render_template('bankAccount/displayCreatedAccount.html',context=context)
    except MySQLError as e:
        error_code, error_message = e.args
        flash(error_message,"Error")
        return redirect(url_for('bank_account.create_current_account_for_new_organization'))
    
    except Exception as e:
        flash("Unkown Error occured","Error")
        return redirect(url_for('dashboard.dashboard'))


   
@bank_account_app.route('/organization/current/new',methods = DEFUALT_SUBMISSION_METHODS,endpoint='create_current_account_for_new_organization')
@valid_employee
def create_current_account_for_new_organization():
    if request.method == 'POST':
        first_name, last_name, branch_id, nic, telephone, home_town, date_of_birth, first_deposit, organization_name, organization_role = (request.form[key] for key in ['first_name', 'last_name', 'branch_id', 'nic', 'telephone', 'home_town', 'date_of_birth', 'first_deposit', 'organization_name', 'organization_role'])
        account_number = get_account_number(first_name,last_name,branch_id)
        return create_current_account_for_new_organization_user(first_name,last_name,branch_id,nic,telephone,home_town,date_of_birth,first_deposit,account_number,organization_name,organization_role)
 
    elif request.method == 'GET':
        context = get_branch_id(session['user_id'])
        print("context",context)
        return render_template('bankAccount/newCurrentOrganization.html',context=context)
    
########################################################## Existing User Account Creation ##########################################################
########################################################## Savings Account Creation ##########################################################


def create_savings_account_for_exsisting_organization_user(user_id,account_number_of_new_account,account_number_of_old_account,amount,organization_name,organization_role):
    connector = Connector()
    try:
        with connector:
            print(user_id,account_number_of_new_account,account_number_of_old_account,amount,organization_name)
            connector.cursor.execute(CREATE_SAVINGS_ACCOUNT_FOR_EXISTSING_ORAGANIZATION_USER,(user_id,account_number_of_old_account,account_number_of_new_account,amount,organization_name,organization_role,))
            context = connector.cursor.fetchone()
            flash("Account Created Successfully", 'Account')
            return render_template('bankAccount/displayCreatedAccount.html',context=context)
    except MySQLError as e:
          error_code, error_message = e.args
          flash(error_message,"Error")
          return redirect(url_for('bank_account.create_savings_account_for_existing_user_organization'))
    except Exception as e:
        flash("Unkown Error occured","Error")
        return redirect(url_for('dashboard.dashboard'))

@bank_account_app.route('/organization/savings/exsisting',methods = DEFUALT_SUBMISSION_METHODS,endpoint='create_savings_account_for_existing_user_organization')  
@valid_employee
def create_savings_account_for_existing_user_organization():
    if request.method == 'POST':
        data = get_branch_id_and_number_of_accounts_and_full_name(session['user_id'],request.form['account_number'])
        if data is None:
            return redirect(url_for('bank_account.create_savings_account_for_existing_user_organization'))
        branch_id,number_of_accounts,full_name = (data[key] for key in ['branch_id','number_of_accounts','full_name'])
        new_account_number = get_account_number(full_name,"",branch_id,number_of_accounts=number_of_accounts)
        return create_savings_account_for_exsisting_organization_user(session['user_id'],new_account_number,request.form['account_number'],request.form['first_deposit'],request.form['organization_name'],request.form['organization_role'])
    
    elif request.method == 'GET':
        return render_template('bankAccount/existingSavingOrganization.html')
    

########################################################## Current Account Creation ##########################################################

def create_current_account_for_exsisting_organization_user(user_id,account_number_of_new_account,account_number_of_old_account,amount,organization_name,organization_role):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(CREATE_CURRENT_ACCOUNT_FOR_EXISTSING_ORAGANIZATION_USER,(user_id,account_number_of_old_account,account_number_of_new_account,amount,organization_name,organization_role,))
            context = connector.cursor.fetchone()
            flash("Account Created Successfully", 'Account')
            return render_template('bankAccount/displayCreatedAccount.html',context=context)
    except MySQLError as e:
          error_code, error_message = e.args
          flash(error_message,"Error")
          return redirect(url_for('bank_account.create_current_account_for_existing_user_organization'))
    except Exception as e:
        flash("Unkown Error occured","Error")
        return redirect(url_for('dashboard.dashboard'))

@bank_account_app.route('/organization/current/exsisting',methods = DEFUALT_SUBMISSION_METHODS,endpoint='create_current_account_for_existing_user_organization')  
@valid_employee
def create_current_account_for_existing_user_organization():
    if request.method == 'POST':
        data = get_branch_id_and_number_of_accounts_and_full_name(session['user_id'],request.form['account_number'])
        if data is None:
            return redirect(url_for('bank_account.create_current_account_for_existing_user_organization'))
        branch_id,number_of_accounts,full_name = (data[key] for key in ['branch_id','number_of_accounts','full_name'])
        new_account_number = get_account_number(full_name,"",branch_id,number_of_accounts=number_of_accounts)
        return create_current_account_for_exsisting_organization_user(session['user_id'],new_account_number,request.form['account_number'],request.form['first_deposit'],request.form['organization_name'],request.form['organization_role'])
    elif request.method == 'GET':
        return render_template('bankAccount/existingCurrentOrganization.html')
    

########################################################## Fixed Account Creation ##########################################################


def creat_fixed_account_for_for_exsisting_user_organization(user_id,savings_account_number,amount,duration,user_organization_name,user_organization_role):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(CREATE_FIXED_ACCOUNT_FOR_EXISTING_ORGANIZATION_USER,(user_id,savings_account_number,amount,duration,user_organization_name,user_organization_role,))
            context = connector.cursor.fetchone()
            flash("Account Created Successfully", 'Account')
            return render_template('bankAccount/displayCreatedAccount.html',context=context)
    except MySQLError as e:
        error_code, error_message = e.args
        flash(error_message,"Error")
        return redirect(url_for('bank_account.create_fixed_account_for_existing_user_organization'))
    except Exception as e:
        flash("Unkown Error occured","Error")
        return redirect(url_for('dashboard.dashboard'))
    
@bank_account_app.route('/organization/fixed/exsisting',methods = DEFUALT_SUBMISSION_METHODS,endpoint='create_fixed_account_for_existing_user_organization')  
@valid_employee
def create_fixed_account_for_existing_user_organization():
    if request.method == 'POST':
        savings_account_number,first_deposit,duration,organization_name,organization_role = (request.form[key] for key in ['account_number','first_deposit','duration','organization_name','organization_role'])
        print(session['user_id'],savings_account_number,first_deposit,duration,organization_name,organization_role)
        return creat_fixed_account_for_for_exsisting_user_organization(session['user_id'],savings_account_number,first_deposit,duration,organization_name,  organization_role)
    elif request.method == 'GET':
        return render_template('bankAccount/existingFixedOrganization.html')