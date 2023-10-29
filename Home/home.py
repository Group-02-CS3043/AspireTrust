from flask import Blueprint,render_template,session,redirect
from Settings.settings import *



home_app = Blueprint('auth', __name__,template_folder='./templates',static_folder='./static')

@home_app.route('/',methods = DEFAULT_METHODS,endpoint='home')
def home():
    if 'user' in session :
        return redirect('/dashboard')
    else:
        return render_template('home/home.html')
