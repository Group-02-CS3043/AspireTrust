from flask import Blueprint,render_template,session,redirect,flash,request,url_for

from Settings.settings import *
from Configurations.configurations import valid_session,valid_manager
from Database.connection import Connector
from Database.database_quaries import *
from BankAccount.bank_account import get_branch_id

loan_app = Blueprint('loan', __name__,template_folder='./templates',static_folder='static')



def get_not_approved_loans(branch_id):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(GET_LOAN_DETAILS_NOT_APPROVED,(branch_id,))
            context = connector.cursor.fetchall()
            return context
    except Exception as e:
        error_code, error_message = e.args
        print(error_code, error_message)
        flash(error_message,"Error")
        return False


def apply_for_online_loan(user_id,fixed_deposit_id,amount,duration,interest_rate):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(APPLY_FOR_ONLINE_LOAN,(user_id,fixed_deposit_id,amount,duration,interest_rate,))
            connector.connection.commit()
            return True
    except Exception as e:
        error_code, error_message = e.args
        print(error_code, error_message)
        flash(error_message,"Error")
        return False
    
def get_user_details(user_id):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(GET_USER_DETAILS,(user_id,))
            return connector.cursor.fetchone()
    except Exception as e:
        print("Error in get_user_details",e)
        return False
    
def get_fd_accounts(user_id):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(GET_FD_ACCOUNTS,(user_id,))
            return connector.cursor.fetchall()
    except Exception as e:
        print("Error in get_fd_accounts",e)
        return False

def get_maximum_loan_amount(user_id):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(GET_MAXIMUM_LOAN_AMOUNT,(user_id,))
            return connector.cursor.fetchone()
    except Exception as e:
        print("Error in get_maximum_loan_amount",e)
        return False

@loan_app.route('/online_loan',methods = DEFUALT_SUBMISSION_METHODS,endpoint='online_loan')
@valid_session
def online_loan():
    if request.method == 'GET':
        context = get_user_details(session['user_id'])
        fd_accounts = get_fd_accounts(session['user_id'])
        if len(fd_accounts) == 0:
            flash("You don't have fixed deposits for this functionality","Error")
            return redirect('/dashboard')
        context['fd_accounts'] = fd_accounts
        context['maximum_loan_amount'] = int(get_maximum_loan_amount(session['user_id'])['maximum_loan_amount'])
        return render_template('loan/OnlineLoan.html',context=context)
    elif request.method == 'POST':
        print(request.form)
        amount = request.form['loan_amount']
        fixed_deposit_id = request.form['fixed_account_number']
        duration = request.form['duration']
        if apply_for_online_loan(session['user_id'],fixed_deposit_id,amount,duration,0.1):
            flash("Your loan has been accepted and loan amount has been transfered to your account","success")
            return redirect('/dashboard')
        else:
            return redirect('/loan/online_loan')
        
    
@loan_app.route('/loan_requests',methods = DEFUALT_SUBMISSION_METHODS,endpoint='loan_requests')
@valid_manager
def loan_requests():
    if request.method == 'GET':
        branch_id = get_branch_id(session['user_id'])
        print(branch_id)
        context = get_not_approved_loans(branch_id['branch_id'])
        return render_template('loan/loanRequest.html',context=context)

    
@loan_app.route('/approve',methods = DEFUALT_SUBMISSION_METHODS,endpoint='approve')
@valid_manager
def approve():
    if request.method == 'POST':
        loan_id = request.form['status']
        approve_loan(loan_id)
        return redirect(url_for('loan.loan_requests'))

@loan_app.route('/disapprove',methods = DEFUALT_SUBMISSION_METHODS,endpoint='disapprove')   
@valid_manager
def disapprove():
    if request.method == 'POST':
        loan_id = request.form['status']
        disapprove_loan(loan_id)
        return redirect(url_for('loan.loan_requests'))


def approve_loan(loan_id):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(APPROVE_LOAN,(loan_id,))
            connector.connection.commit()
            return True
    except Exception as e:
        error_code, error_message = e.args
        print(error_code, error_message)
        flash(error_message,"Error")
        return False
    

def disapprove_loan(loan_id):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(DISAPPROVE_LOAN,(loan_id,))
            connector.connection.commit()
            return True
    except Exception as e:
        error_code, error_message = e.args
        print(error_code, error_message)
        flash(error_message,"Error")
        return False
