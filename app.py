from flask import Flask,session,render_template
from Auth.auth import auth_app 
from Home.home import home_app
from Dashboard.dashboard import dashboard_app

from Configurations.configurations import get_configurations,get_secret_key
from Configurations.Error_handler import handle_error

app = Flask(__name__)

app.secret_key = get_secret_key()
app.config.update(get_configurations())




app.register_blueprint(auth_app, url_prefix='/auth',name='auth')
app.register_blueprint(home_app,url_prefix='/',name='home')
app.register_blueprint(dashboard_app,url_prefix='/dashboard',name='dashboard')
app = handle_error(app)




if __name__ == '__main__':
    app.run()