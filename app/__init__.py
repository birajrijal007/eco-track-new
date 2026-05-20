from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "ecotrack_secret_key"

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123hijorati2.0'
app.config['MYSQL_DB'] = 'ecotrack'

mysql = MySQL(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return None

from app.routes.home_route import home
from app.routes.auth_route import auth

app.register_blueprint(home)
app.register_blueprint(auth)