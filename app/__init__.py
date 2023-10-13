from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

#project base directory
basedir = os.path.abspath(os.path.dirname(__file__))

myapp_obj = Flask(__name__)
myapp_obj.config.from_mapping(
   SECRET_KEY = 'you-will-never-guess',
   SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
   )
myapp_obj.config['TESTING'] = False

myapp_obj.secret_key = "you-will-never-guess"

db = SQLAlchemy(myapp_obj)
login = LoginManager(myapp_obj)
login.login_view = 'login'

from app import routes, models