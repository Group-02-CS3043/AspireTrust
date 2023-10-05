from flask import Flask,session
from Auth.auth import auth_app 
from Home.home import home_app
from Configurations.configurations import get_configurations,get_secret_key,get_database_configurations
from Database.connection import Connector

app = Flask(__name__)

app.secret_key = get_secret_key()
app.config.update(get_configurations())



app.register_blueprint(auth_app, url_prefix='/auth',name='auth')
app.register_blueprint(home_app,url_prefix='/',name='home')
if __name__ == '__main__':
    app.run(debug=True)