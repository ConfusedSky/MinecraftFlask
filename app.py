import minecraftFlask
from flask_socketio import SocketIO
from minecraftFlask import socketio

app = minecraftFlask.create_app()
app.env = 'development'
socketio.run(app, debug=True)
