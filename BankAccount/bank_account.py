from flask import Blueprint,render_template,session,abort,request,redirect,flash
from Settings.settings import *
from Configurations.configurations import valid_session,valid_employee
from Database.connection import Connector
from Database.database_quaries import *
from .models import Account,get_account_details,set_new_operation


bank_account_app = Blueprint('bank_account', __name__,template_folder='./templates',static_folder='static')


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
    


@bank_account_app.route('/create-exsisting',methods = DEFUALT_SUBMISSION_METHODS,endpoint='create_exsisiting_account')
@valid_employee
@valid_session
def create_account_for_exsisting_users():
    return render_template('bankAccount/existingUserCreateMain.html')

@bank_account_app.route('/create-exsisting/savings',methods = DEFUALT_SUBMISSION_METHODS,endpoint='create_savings_account_existing')
@valid_employee
@valid_session 
def create_saving_account_existing():
    if request.method == 'POST':
        print(request.form['account_number'],request.form['first_deposit'])
        brach_id = get_branch_id(session['user_id'])
        first_name_and_no_of_accounts = get_customer_first_name_and_no_accounts(str(request.form['account_number']))
        print(first_name_and_no_of_accounts)
        ascii_values = [ord(char) for char in first_name_and_no_of_accounts['first_name']]
        new_account_number = f"{str(brach_id['branch_id'])}-{str(sum(ascii_values)%1000)}-{str(first_name_and_no_of_accounts['number_of_accounts']+1)}"
        create_savings_account_for_exsisting_user(session['user_id'],new_account_number,request.form['account_number'],request.form['first_deposit'])
        return redirect('/dashboard')

    elif request.method == 'GET':
        return render_template('bankAccount/existingSavingIndividual.html')


def create_savings_account_for_exsisting_user(user_id,account_number_of_new_account,account_number_of_old_account,amount):
    connector = Connector()
    with connector:
        print(user_id,account_number_of_new_account,account_number_of_old_account,'SAVINGS',amount)
        connector.cursor.execute(CREATE_BANK_ACCOUNT_FOR_EXISTING_USERS,(user_id,account_number_of_new_account,account_number_of_old_account,"SAVINGS",amount,))
        
        connector.connection.commit()
        return True