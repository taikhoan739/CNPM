from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import secrets
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/saledb" % quote('Admin@123')
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/saledb" % quote('Marcus0@')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 3
app.config['SECRET_KEY'] = secrets.token_hex(16)
login = LoginManager(app)
db = SQLAlchemy(app)
