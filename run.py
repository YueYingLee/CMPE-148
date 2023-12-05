from app import myapp_obj, socketio

socketio.run(myapp_obj, debug=True, host="127.0.0.1")
