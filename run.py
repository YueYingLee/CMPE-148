from app import myapp_obj, socketio

socketio.run(myapp_obj, debug=True, host="172.20.10.2")
