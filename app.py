import minecraftFlask
from minecraftFlask import socketio

app = minecraftFlask.create_app()
app.env = 'development'

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000)
