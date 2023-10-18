from flask import render_template
from flask import redirect, request, session, url_for
from flask import flash, get_flashed_messages
from app import myapp_obj, db
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_socketio import join_room, leave_room, send, SocketIO
from datetime import datetime
from app.models import User

from sqlalchemy import desc


@myapp_obj.route("/")
def index():
    return render_template('index.html' )


@myapp_obj.route("/homepage")
@login_required
def homepage():
    user = current_user
    user_fullname = user.username
    return render_template('homepage.html', user_fullname = user_fullname)


@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        valid_user = User.query.filter_by(username = form.name.data).first()
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

@myapp_obj.route("/register", methods =['GET', 'POST'])
def register():
        registerForm  = registerUser()
        if registerForm.validate_on_submit():
          same_Username = User.query.filter_by(username = registerForm.username.data).first()
          if same_Username == None:
            user = User(username= registerForm.username.data)
            user.set_password(registerForm.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect('/login')
          else :
             flash('The username is not available. Please choose another username.')
        return render_template('register.html', registerForm=registerForm)
