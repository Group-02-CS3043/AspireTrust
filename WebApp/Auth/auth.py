from flask import Blueprint,render_template,request,session,redirect,flash,abort,url_for
from Settings.settings import *
from .models import *
from Database.connection import Connector


auth_app:Blueprint = Blueprint('auth', __name__,template_folder='./templates',static_folder='static')
connector = Connector()


@auth_app.route('/login',methods = DEFUALT_SUBMISSION_METHODS,endpoint='login')
def login()->str:
    if 'user_id' in session :
        flash("You are already logged in", 'Login')
        return redirect('/dashboard')

    if request.method == 'GET':
        return render_template('auth/login.html')
    
    elif request.method == 'POST':
       if not is_user_exsists(request.form['username'],connector):
           flash("User doesn't exists", 'Error')
           return render_template('auth/login.html')
       else:
           user_id = authenticate_user(request.form,connector)
           if user_id:
               session['user_id'] = int(user_id)
               session['user_role'] = get_user_role(int(user_id),connector)
               flash("Login Successful", 'Success')
               return redirect('/dashboard')
           else:
                flash("Incorrect Credentials", 'Error')
                return render_template('auth/login.html')
    


@auth_app.route('/find',methods = DEFUALT_SUBMISSION_METHODS,endpoint='find')
def find_from_account_number():
    if 'user_id' in session :
        flash("You are already logged in", 'Login')
        return redirect('/dashboard')
    
    if request.method == 'POST':
        user_id = is_account_exsists(request.form['account_number'],connector)
        if user_id:
            if have_a_user_account(user_id,connector):
                flash("User already have an account", 'Error')
                return redirect('login')
            else:
                flash("User found ! Please create account for Web Portal", 'Success')
                return redirect('register')
        else:
            flash("Please contact your neaerest branch for more details ", 'No Account Found')
            return redirect('login')

    else:
        return render_template('auth/account.html')       
           
           
@auth_app.route('/register',methods = DEFUALT_SUBMISSION_METHODS,endpoint='register')
def sigup()->str:
    if 'user_id' in session :
        flash("You are already logged in", 'Login')
        return redirect('/dashboard')
    
    if request.method == 'POST':
        print(valid_account_number(request.form['account_number'],connector))
        if valid_account_number(request.form['account_number'],connector):
            flash('Account number is not correct', 'Error')
            return redirect(url_for('auth.register'))

        if is_user_exsists(request.form['username'],connector):
            flash('Username already exists', 'Error')
            return redirect(url_for('auth.register'))
        else:
            if request.form['confirm_password'] != request.form['password']:
                flash('Passwords are mismatch','Error')
                return redirect(url_for('auth.register'))
            user_id = create_user(request.form['username'],request.form['password'],request.form['account_number'],connector)
            session['user_id'] = int(user_id)
            session['user_role'] = get_user_role(int(user_id),connector)
            return redirect('/dashboard')

    if request.method == 'GET':
        return render_template('auth/register.html')


    #         user = User(request.form,connector)
    #         if user.verify_user():
    #             session['user'] = user.username
    #             session['user_role'] = user.user_role
    #             session['user_id'] = user.user_id
    #             return redirect('/dashboard')
    #         else:
    #             flash('Login Unsuccessful', 'error')
    #             return render_template('login.html')

    # else:
    #     return render_template('login.html')
    
# @auth_app.route('/account',methods = DEFUALT_SUBMISSION_METHODS)  
# def find_from_account_number():
#     if request.method == 'POST':
#         if find_user_acount_from_account_number(request.form['account-number'],connector):
            
#     else:
#         return render_template('find_account_using_account_number.html')

# @auth_app.route('/register',methods = DEFUALT_SUBMISSION_METHODS)
# def sigup()->str:
#     if 'user' in session :
#         return redirect('/dashboard')
    
#     if request.method == 'POST':
#         user = User(request.form,connector)
#         if user.username_exists():
#             flash('Username already exists', 'error')
#             return render_template('register.html')
#         elif user.add_to_database(): 
#             session['user'] = user.username
#             return redirect('/dashboard')
#         else:
#             flash('Registration Unsuccessful', 'error')
#             return render_template('register.html')
    
#     return render_template('register.html')

@auth_app.route('/logout',methods = DEFAULT_METHODS)
def logout():
    session.pop('user_id',None)
    flash('You have been logged out', 'Success')
    return redirect('/')

