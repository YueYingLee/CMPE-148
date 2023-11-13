from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from flask_socketio import SocketIO
from flask_cors import CORS

#project base directory
basedir = os.path.abspath(os.path.dirname(__file__))

myapp_obj = Flask(__name__)
CORS(myapp_obj, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(myapp_obj, cors_allowed_origins="*")
myapp_obj.config.from_mapping(
   SECRET_KEY = 'you-will-never-guess',
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:ihcmpe148@cmpe1483c1s.cymhhes8mryj.us-east-2.rds.amazonaws.com/CMPE148_PROJECT'
   )
myapp_obj.config['TESTING'] = False

myapp_obj.secret_key = "you-will-never-guess"

db = SQLAlchemy(myapp_obj)
login = LoginManager(myapp_obj)
login.login_view = 'login'

from app import routes, models

