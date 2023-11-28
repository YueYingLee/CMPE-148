from app import myapp_obj, socketio

socketio.run(myapp_obj, debug=True, host="10.0.0.196")
