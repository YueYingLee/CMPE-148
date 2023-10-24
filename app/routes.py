from flask import render_template
from flask import redirect, url_for
from flask import flash, get_flashed_messages
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_socketio import join_room, leave_room, send, SocketIO
from datetime import datetime
from app.models import Users, Conversations, Messages
from app.register import registerUser
from app.login import LoginForm
from sqlalchemy import desc
from app.user_search import UserForm
from datetime import datetime
from app import myapp_obj, db
from . import socketio

@myapp_obj.route("/")
def index():
    return render_template("login.html")

@myapp_obj.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        valid_user = Users.query.filter_by(username=form.name.data).first()
        if valid_user != None:
            if valid_user.check_password(form.password.data) == True:
                login_user(valid_user)
                return redirect(url_for("homepage"))
            else:
                flash(f"Invalid password. Try again.")
        else:
            flash(f"Invalid username. Try again or register an account.")

    return render_template("login.html", form=form)


@myapp_obj.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@myapp_obj.route("/register", methods=["GET", "POST"])
def register():
    registerForm = registerUser()
    if registerForm.validate_on_submit():
        same_Username = Users.query.filter_by(
            username=registerForm.username.data
        ).first()
        if same_Username == None:
            user = Users()
            user.username = registerForm.username.data
            user.set_password(registerForm.password.data)

            db.session.add(user)
            db.session.commit()
            return redirect("/login")
        else:
            flash("The username is not available. Please choose another username.")
    return render_template("register.html", registerForm=registerForm)

@myapp_obj.route("/homepage", methods = ["GET", "POST"])
@login_required
def homepage():
    user = current_user
    form = UserForm()
    #after searching for a user, verify searched user exists and the current user is not trying to message themselves
    if form.validate_on_submit():
        valid_users = True
        username_list = [user.username]
        for conv_user in form.names.data.split(", "):
            searched_user = Users.query.filter_by(username=conv_user).first()
            if searched_user == None:
                flash(f"User {conv_user} does not exist. Please try again")
                valid_users = False
            elif searched_user.username == user.username:
                flash('You cannot add yourself to a conversation')
                valid_users = False
            else:
                username_list.append(conv_user)

        if valid_users:
            if len(username_list) <= 10:
                username_list.sort()
                username_string = ",".join(username_list)
                print(username_string)
                current_conversation = Conversations.query.filter_by(participants=username_string).first()
                if current_conversation == None:
                    new_conversation = Conversations()
                    new_conversation.participants = username_string
                    db.session.add(new_conversation)
                    db.session.commit()
                    return redirect(f"/conversation/conversation_id={new_conversation.conv_id}")
                #ONCE VIEW CONVERSATIONS IS DONE, REMOVE THIS AND TELL USER "CONVERSATION ALREADY EXISTS"
                else:
                    return redirect(f"/conversation/conversation_id={current_conversation.conv_id}")
            else:
                flash("You can only have 10 users max in a conversation")
        

                
    return render_template("home.html",user = user, form = form)

@myapp_obj.route("/conversation/conversation_id=<conversation_id>", methods = ["GET", "POST"])
@login_required
def conversation(conversation_id):
     user = current_user
     print(conversation_id) #debugging
     #get the current conversation 
     current_conversation = Conversations.query.filter_by(conv_id = conversation_id).first()
     participants = current_conversation.participants
     #if a user tries to access a conversation they are not a participant in
     if user.username not in participants:
        flash('You do not have access to this conversation')
        return redirect("/homepage")
     

     #valid user participation, get all the messages sorted from oldest to newest
     all_messages = Messages.query.filter_by(conversation_id = current_conversation.conv_id).all()
     sorted_messages = sorted(all_messages, key=lambda message: message.timestamp)
     print(sorted_messages) #debugging
     return render_template("conversation.html", all_messages = all_messages, conversation_id = conversation_id, participants = participants)


"""
handles "message" event from the javascript socket io (client side)
payload = user message from the frontend
"""
@socketio.on('message')
def handle_message(payload):
    print("MESSAGE FROM FRONTEND") #debuggin purposes

    user = current_user
    #get each needed attribute for a message
    msg_content = payload["message"] #content
    new_message = Messages()
    new_message.sender_name = user.username #sender name
    new_message.conversation_id = payload["conversation_id"] #convo_id
    new_message.timestamp = datetime.now() #timestamp
    new_message.msg_content = msg_content 
    
    db.session.add(new_message)
    db.session.commit()
    print("MESSAGE SENT")
