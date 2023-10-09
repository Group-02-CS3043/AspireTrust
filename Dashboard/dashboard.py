from flask import Blueprint,render_template,session,redirect
from Settings.settings import *
from Configurations.configurations import valid_session

dashboard_app = Blueprint('dashboard', __name__,template_folder='./templates',static_folder='./static')

user_accounts = [
    'savings',
    'current',
    'fixed_deposit'
]

@dashboard_app.route('/',methods = DEFAULT_METHODS,endpoint='dashboard')
@valid_session
def dashboard():
    context = {'user':session['user'],'accounts':user_accounts}
    return render_template('dashboard.html',context=context)