from flask import Blueprint,render_template
from Settings.settings import *


home_app = Blueprint('auth', __name__,template_folder='templates')

@home_app.route('/',methods = DEFAULT_METHODS,endpoint='home')
def home():
    return render_template('home.html')
