from app import db
from sqlalchemy.types import Boolean, Date, DateTime, Float, Integer, Text, Time, Interval
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import UserMixin

class User(db.Model, Usermixin):
    id=db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        print("self.password is: ")
        print(self.password)
        print("input password is: ")
        print(password)
        return check_password_hash(self.password, password)

    def __repr__(self): #for debugging process
        return f'<user {self.id}: {self.name}>'


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
     def __repr__(self): #for debugging process
        return f'<Messages {self.id}:>'

class Conversations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
     def __repr__(self): #for debugging process
        return f'<Conversations {self.id}: >'

class Room (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.String(50), unique=True, nullable=False)
    users = db.Column(db.String)

@login.user_loader
def load_user(id):
    return User.query.get(int(id)) 