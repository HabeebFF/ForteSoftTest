from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SECRET_KEY'] = "fe6b9674f46b32e7ec6f592fbd6cb76c"
db = SQLAlchemy(app) 
login_manager = LoginManager(app)
login_manager.login_view = 'login'


from hub import routes
from hub import model