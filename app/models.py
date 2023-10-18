from app import db
from sqlalchemy.types import Boolean, Date, DateTime, Float, Integer, Text, Time, Interval, ARRAY
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import UserMixin
import datetime

"""
User relation 

user_id -> auto generated id for each user
name -> user entered name
password_hash -> user entered password stored as hash

"""
class User(db.Model, UserMixin):
    user_id=db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

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

"""
Conversation relations

conv_id -> auto generated id for conversation 
participants -> a string representation of a list of user_ids where each id is the user_id of someone
in the conversation. it's a string because SQLite does not support arrays. convert this string back to a 
list in the backend if you need to. 

"""
class Conversations(db.Model):
    conv_id = db.Column(db.Integer, primary_key=True)
    participants = db.Column(db.String)
    def __repr__(self): #for debugging process
        return f'<Conversations {self.id}: >'

"""
Messages relation 
msg_id -> Auto generated id for the message
sender_id -> links to User relation. the user_id of the User who sent the message
conversation_id -> links to Conversation relation. the conv_id of the current Conversation 
timestamp -> the date and time the message was sent
msg_content -> the actual content of the message. 1024 character limit

"""
class Messages(db.Model):
    msg_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey(User.user_id)) 
    conversation_id = db.Column(db.Integer, db.ForeignKey(Conversations.conv_id))
    timestamp = db.Column(db.DateTime, default=datetime.timezone.utc)
    msg_content = db.Column(db.String(1024))
    def __repr__(self): #for debugging process
        return f'<Messages {self.id}:>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id)) 