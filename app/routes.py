from flask import render_template, request,jsonify
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
from app.account import deleteAcc
from app.login import LoginForm
from app.resetpassword import ResetForm
from sqlalchemy import desc
from app.user_search import UserForm
from datetime import datetime
from app import myapp_obj, db
from . import socketio
from cryptography.fernet import Fernet
from flask_cors import CORS, cross_origin

def get_conversations():
    #get current user
    #from Conversations relation, get every conversation that contains this user (useranme) in participants
    #sort (?) these conversations. potentially by id, participants length, etc? or add a "last modified" field
    #which would be the timestamp of the last sent message and order by that (newest to oldest)
    #render this in HTML template
    user = current_user
    return Conversations.query.filter(Conversations.participants.contains(user.username)).all()

#This is the first page user will reach when they run the program
@myapp_obj.route("/")
def index():
    return render_template("index.html")



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
            flash("Registration failed")
    return render_template("register2.html", registerForm=registerForm)

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
                flash(f"Login failed.")
        else:
            flash(f"Login failed.")

    return render_template("login2.html", form=form)

@myapp_obj.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))



@myapp_obj.route("/delete_account", methods=["GET", "POST"])
@login_required
def delete_account():
    deleteForm=deleteAcc()
    if deleteForm.validate_on_submit() and request.method == "POST":
        user = current_user 
        if current_user.is_authenticated:       
            # Delete associated messages
            messages_to_delete = Messages.query.filter_by(sender_name=current_user.username).all()
            for message in messages_to_delete:
                db.session.delete(message)
            # Delete the user from the database
            db.session.delete(user)
            db.session.commit()
            # Log the user out after deleting the account
            flash("Sorry to see you leaving. :(\n")
            logout_user()
            
            flash("Your account has been deleted.")
            return redirect(url_for("register"))

    return render_template("delete_account.html", user=current_user, deleteForm=deleteForm)


@myapp_obj.route("/homepage", methods = ["GET", "POST"])
@login_required
def homepage():
    user = current_user
    user_conversations = get_conversations()
    form = UserForm()
    #after searching for a user, verify searched user exists and the current user is not trying to message themselves
    if form.validate_on_submit():
        valid_users = True
        username_list = [user.username]
        for conv_user in form.names.data.split(", "):
            searched_user = Users.query.filter_by(username=conv_user).first()
            if searched_user == None:
                flash(f"Cannot create conversation")
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
        

                
    return render_template("home.html",user = user, form = form, user_conversations = user_conversations)

@myapp_obj.route("/conversation/conversation_id=<conversation_id>", methods = ["GET", "POST"])
@login_required
def conversation(conversation_id):
     user = current_user
     user_conversations = get_conversations()
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
     #create new data structure (list of dictionaries (?))
     #each dictionary has: username, timestamp, decrypted message
     #sort the list by each dictionary timestamp (newest to oldest)
     #pass this to HTML for rendering 
     decrypted_messages = []
     for message in sorted_messages:
         encrypted_msg = message.encrypted_msg
         encryption_key = message.encryption_key
         cipher = Fernet(encryption_key)
         decrypted_message = cipher.decrypt(encrypted_msg)
         decrypted_message = decrypted_message.decode('utf-8') #actual message content, send to frontend
         msg_to_display = {
             "sender_name": message.sender_name, 
             "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S"), 
             "message": decrypted_message
         }
         decrypted_messages.append(msg_to_display)
     return render_template("conversation.html", decrypted_messages = decrypted_messages, conversation_id = conversation_id, participants = participants, user_conversations = user_conversations, user = user,connected_users=connected_users)


@socketio.on('join_room')
def handle_join(data):
    room = str(data['conversation_id'])
    join_room(room)
    print(f"{data['user']} joined conversation number {data['conversation_id']}")

"""
handles "message" event from the javascript socket io (client side)
payload = user message from the frontend
"""
@socketio.on('message')
def handle_message(payload):

    print(payload)
    #preparing encryption / key
    key = Fernet.generate_key() #generate a unique key for each message
    cipher = Fernet(key) #Fernet using a simplified version of AES 

    msg_content = payload["message"] #the actual message that the user sent
    user = payload["username"]
    encrypted_message = cipher.encrypt(msg_content.encode('utf-8')) #encode and encrypt sent message
    decrypted_message = cipher.decrypt(encrypted_message)
    decrypted_message = decrypted_message.decode('utf-8') #actual message content, send to frontend

    new_message = Messages()
    new_message.sender_name = user #sender name
    new_message.conversation_id = payload["conversation_id"] #convo_id
    new_message.timestamp = datetime.now() #timestamp
    new_message.encrypted_msg = encrypted_message
    new_message.encryption_key = key
    
   
    display_message = {
        'message': decrypted_message,
        'sender_name': new_message.sender_name,
        "timestamp": new_message.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    }
    room = str(payload["conversation_id"])
    send(display_message, to = room) 
    
    db.session.add(new_message)
    db.session.commit()
    print("MESSAGE SENT")


connected_users = {}

@socketio.on('connect')
def handle_connect():
    user_id = current_user.username
    connected_users[user_id] = 'online'
    print(f'User connected: {user_id}')
    update_connected_users()

@socketio.on('disconnect')
def handle_disconnect():
    user_id = current_user.username
    del connected_users[user_id]
    print(f'User disconnected: {user_id}')
    update_connected_users()


def update_connected_users():
    print('Updating connected users:', connected_users)
    connected_user_data = {user_id: status for user_id, status in connected_users.items()}
    socketio.emit('updateUsers', connected_user_data, room='/',namespace='/')
