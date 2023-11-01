from flask import Blueprint,render_template,session,redirect,flash,request
from Settings.settings import *
from Configurations.configurations import valid_session,valid_employee
from Database.connection import Connector
from Database.database_quaries import *
from datetime import datetime


report_app = Blueprint('report', __name__,template_folder='./templates',static_folder='static')

def get_interbank_transactions(min_val , max_val,start_date ,end_date , from_branch_id , to_branch_id):

    connector = Connector()
    try:
        with connector:

            connector.cursor.execute(GET_REPORT_INTER_BRANCH,(min_val,max_val,start_date ,end_date,from_branch_id,to_branch_id,))
            # connector.cursor.execute(GET_ALL_TRANSACIONS,(branch_id,branch_id,))
            return connector.cursor.fetchall()
    except Exception as e:
        print("Error in get_interbank_transactions",e)
        return None

def get_intrabank_transactions (min_val , max_val,start_date ,end_date , from_branch_id , to_branch_id):

    connector = Connector()
    try:
        with connector:

            connector.cursor.execute(GET_REPORT_INTRA_BRANCH,(min_val,max_val,start_date ,end_date,from_branch_id,to_branch_id,))
            # connector.cursor.execute(GET_ALL_TRANSACIONS,(branch_id,branch_id,))
            return connector.cursor.fetchall()
    except Exception as e:
        print("Error in get_interbank_transactions",e)
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

@report_app.route('/interbank_transactions',methods = DEFUALT_SUBMISSION_METHODS,endpoint='interbank_transactions')
@valid_session
@valid_employee
def interbank_transactions():
    if request.method == 'GET':
        context = {}
        branch_id = get_branch_id(session['user_id'])['branch_id']
        start_date = '2019-01-01'
        end_date = datetime.now().strftime("%Y-%m-%d")
        min_value = 0
        
        max_value = 10000
        context['transactions'] = get_interbank_transactions(min_value , max_value , start_date,end_date,branch_id,branch_id)
        context['start_date'] = start_date
        context['end_date'] = end_date
        context['min_value'] = min_value
        context['max_value'] =max_value


        print("context",context)
        return render_template('reports/alltransactions.html',context = context)
    elif request.method == 'POST':
        print(request.form)
        context = {}
        branch_id = get_branch_id(session['user_id'])['branch_id']
        start_date = request.form['starting_date']
        end_date =request.form['end_date']
        min_value = request.form['min_value']
        max_value = request.form['max_value']
        context['transactions'] = get_interbank_transactions(min_value , max_value , start_date,end_date,branch_id,branch_id)
        context['start_date'] = start_date
        context['end_date'] = end_date
        context['min_value'] = min_value
        context['max_value'] =max_value
        return render_template('reports/alltransactions.html',context = context)
    


@report_app.route('/intrabank_transactions',methods = DEFUALT_SUBMISSION_METHODS,endpoint='intrabank_transactions')
@valid_session
@valid_employee
def intrabank_transactions():
    if request.method == 'GET':
        context = {}
        branch_id = get_branch_id(session['user_id'])['branch_id']
        start_date = '2019-01-01'
        end_date = datetime.now().strftime("%Y-%m-%d")
        min_value = 0
        
        max_value = 10000
        context['transactions'] = get_intrabank_transactions(min_value , max_value , start_date,end_date,branch_id,branch_id)
        context['start_date'] = start_date
        context['end_date'] = end_date
        context['min_value'] = min_value
        context['max_value'] =max_value


        print("context",context)
        return render_template('reports/alltransactions.html',context = context)
    elif request.method == 'POST':
        print(request.form)
        context = {}
        branch_id = get_branch_id(session['user_id'])['branch_id']
        start_date = request.form['starting_date']
        end_date =request.form['end_date']
        min_value = request.form['min_value']
        max_value = request.form['max_value']
        context['transactions'] = get_intrabank_transactions(min_value , max_value , start_date,end_date,branch_id,branch_id)
        context['start_date'] = start_date
        context['end_date'] = end_date
        context['min_value'] = min_value
        context['max_value'] =max_value
        return render_template('reports/alltransactions.html',context = context)