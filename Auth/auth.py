from flask import Blueprint,render_template,request,session,redirect,flash
from Settings.settings import *
from .models import User
from Database.connection import Connector


auth_app:Blueprint = Blueprint('auth', __name__,template_folder='./templates',static_folder='static')
connector = Connector()
connector.connect()

@auth_app.route('/login',methods = DEFUALT_SUBMISSION_METHODS)
def login()->str:
    if 'user' in session :
        return redirect('/')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username,password,connector)
        if user.verify_user():
            session['user'] = username
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
        username = request.form['username']
        password = request.form['password']
        user = User(username,password,connector)
        if user.username_exists():
            flash('Username already exists', 'error')
            return render_template('register.html')
        elif user.add_to_database(): 
            session['user'] = username
            return redirect('/')
        else:
            flash('Registration Unsuccessful', 'error')
            return render_template('register.html')
    return render_template('register.html')

@auth_app.route('/logout',methods = DEFAULT_METHODS)
def logout():
    session.pop('user',None)
    return redirect('/')

