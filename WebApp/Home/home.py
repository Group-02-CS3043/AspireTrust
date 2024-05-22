from flask import Blueprint,render_template,session,redirect,request,flash
from Settings.settings import *



home_app = Blueprint('auth', __name__,template_folder='./templates',static_folder='./static')

@home_app.route('/',methods = DEFUALT_SUBMISSION_METHODS,endpoint='home')
def home():
    if request.method == 'POST':
        flash("We will contact you as soon as possible ! Thank you for contacting us :)","Welcome")
        return render_template('home/home.html')
    if 'user' in session :
        return redirect('/dashboard')
    else:
        return render_template('home/home.html')
