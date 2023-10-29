from flask import Blueprint,render_template,session,abort,request,redirect,flash
from Settings.settings import *
from Configurations.configurations import valid_session
from Database.connection import Connector
from Database.database_quaries import *
from .models import Account,get_account_details,set_new_operation

bank_account_app = Blueprint('bank_account', __name__,template_folder='./templates',static_folder='static')


def get_branch(user_id):
    connector = Connector()
    with connector:
        connector.cursor.execute(GET_BRANCH % user_id)
        return connector.cursor.fetchone()['city']

@bank_account_app.route('/savings_account',methods = DEFUALT_SUBMISSION_METHODS,endpoint='create_savings_account')
@valid_session
def create_savigs_account():
    if request.method == 'POST':
        account = Account()
        account.validate_details(request.form)
        if account.create_new_user():
            return redirect('/dashboard')
        else:
            abort(500)
        

    else:
        if session['user_role'] == 'EMPLOYEE':
            context = {'account_type':'Savings Account'}
            context['branch'] = get_branch(session['user_id'])
            return render_template('AccCreationIndividual.html',context=context)
        else: abort(403)


@bank_account_app.route('/transfer',methods = DEFUALT_SUBMISSION_METHODS,endpoint='transfer')
def transaction():
    if request.method == 'POST':
        print(request.form['from_account_number'],request.form['to_account_number'],request.form['amount'])
        status = set_new_operation(request.form['from_account_number'],request.form['to_account_number'],request.form['amount'],'transfered to '+request.form['to_account_number'])
        if status:
            flash("Transaction Successfull", 'Transaction')
            return redirect('/dashboard')
        else:
            flash("Transaction Failed", 'error')
            return redirect('/dashboard')
    if request.method == 'GET':
        context = get_account_details(session['user_id'])
        return render_template('bankAccount/transaction.html',context=context)