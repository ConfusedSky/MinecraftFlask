import minecraftFlask
from minecraftFlask import socketio

app = minecraftFlask.create_app()
app.env = 'development'
socketio.run(app, debug=True)
