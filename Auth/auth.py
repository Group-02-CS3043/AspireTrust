from flask import Blueprint,render_template,request,session,redirect,flash
from Settings.settings import *
from .models import User
from Database.connection import Connector


auth_app:Blueprint = Blueprint('auth', __name__,template_folder='./templates',static_folder='static')
connector = Connector()


@auth_app.route('/login',methods = DEFUALT_SUBMISSION_METHODS)
def login()->str:
    if 'user' in session :
        return redirect('/')
    
    if request.method == 'POST':
        with connector:
            user = User(request.form,connector)
            if user.verify_user():
                session['user'] = user.username
                session['user_role'] = user.user_role
                session['user_id'] = user.user_id
                return redirect('/dashboard')
            else:
                flash('Login Unsuccessful', 'error')
                return render_template('login.html')

    else:
        return render_template('login.html')
    
    
@auth_app.route('/register',methods = DEFUALT_SUBMISSION_METHODS)
def sigup()->str:
    if 'user' in session :
        return redirect('/dashboard')
    
    if request.method == 'POST':
        user = User(request.form,connector)
        if user.username_exists():
            flash('Username already exists', 'error')
            return render_template('register.html')
        elif user.add_to_database(): 
            session['user'] = user.username
            return redirect('/dashboard')
        else:
            flash('Registration Unsuccessful', 'error')
            return render_template('register.html')
    
    return render_template('register.html')

@auth_app.route('/logout',methods = DEFAULT_METHODS)
def logout():
    session.pop('user',None)
    return redirect('/')

