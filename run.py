from app import myapp_obj, socketio

socketio.run(myapp_obj, debug=True, host="192.168.0.195")
