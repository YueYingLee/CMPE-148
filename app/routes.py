from flask import render_template
from flask import redirect, request, session, url_for
from flask import flash, get_flashed_messages
from app import myapp_obj, db, socketio
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_socketio import join_room, leave_room, emit
from datetime import datetime
from app.send_emails import sendEmails
from app.register import registerUser 
from app.models import User, Emails, Todo, Profile, ChatRoom, Note
from app.login import LoginForm
from app.notes import NoteForm
from app.todo import TodoForm
from app.profile import BioForm, PasswordForm, DeleteForm
from app.chat import CreateRoomForm, JoinRoomForm
from sqlalchemy import desc


@myapp_obj.route("/")
def index():
    return render_template('index.html' )


@myapp_obj.route("/homepage")
@login_required
def homepage():
    user = current_user
    user_fullname = user.fullname
    return render_template('homepage.html', user_fullname = user_fullname)


@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        valid_user = User.query.filter_by(name = form.name.data).first()
        if valid_user != None:
          if valid_user.check_password(form.password.data)== True:
             login_user(valid_user)
             return redirect(url_for('homepage'))
          else :
             flash(f'Invalid password. Try again.')
        else: 
             flash(f'Invalid username. Try again or register an account.')  

    return render_template('login.html', form=form)


@myapp_obj.route("/logout", methods = ['GET', 'POST'])
@login_required
def logout():
       logout_user()
       return redirect(url_for('login'))
