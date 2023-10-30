from flask import Blueprint,render_template,session,redirect,flash,request
from Settings.settings import *
from Configurations.configurations import valid_session,valid_employee
from Database.connection import Connector
from Database.database_quaries import *


report_app = Blueprint('report', __name__,template_folder='./templates',static_folder='static')

def get_interbank_transactions(branch_id):
    connector = Connector()
    try:
        with connector:
            connector.cursor.execute(GET_ALL_TRANSACIONS,(branch_id,branch_id,))
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

@report_app.route('/interbank_transactions',methods = DEFAULT_METHODS,endpoint='interbank_transactions')
@valid_session
@valid_employee
def interbank_transactions():
    if request.method == 'GET':
        context = {}
        branch_id = get_branch_id(session['user_id'])['branch_id']
        context['transactions'] = get_interbank_transactions(branch_id)
        print("context",context)
        return render_template('reports/alltransactions.html',context = context)