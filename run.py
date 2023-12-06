from app import myapp_obj, socketio

socketio.run(myapp_obj, debug=True, host="10.250.62.200")
