from flask import (
    Blueprint, g, render_template, request, url_for, jsonify
)
import subprocess
import sys
import cgi
import socket
import os
from mcstatus import MinecraftServer
from threading import Lock
from . import socketio

bp = Blueprint('index', __name__)
thread = None
thread_lock = Lock()

def background_thread():
    f = subprocess.Popen(['tail', '-F', '-n', '0', '/home/masa/Documents/MinecraftServers/Vanilla1-12-2/logs/latest.log'], stdout=subprocess.PIPE)
    while True:
        line = f.stdout.readline()
        if not line:
            break
        # Do things with the line
        if "joined" in line:
            print("Emitting header update")
            socketio.sleep(.5)
            socketio.emit("update header")
        if "left" in line:
            print("Emitting header update")
            socketio.sleep(2)
            socketio.emit("update header")
        print(line)

@socketio.on('connect')
def connect():
    global thread
    with thread_lock:
        if thread is None or not thread.isAlive():
            thread = socketio.start_background_task(target=background_thread)

@bp.route("/status")
def status():
    server = MinecraftServer("localhost", 25565)
    try:
        query = server.query()
        qtup =  {
                    "players":
                    {
                        "online": query.players.online,
                        "max": query.players.max,
                        "names": query.players.names
                    },
                    "serverUp": True
                }
    except socket.error:
        qtup = { "serverUp": False }
    return jsonify(qtup)

@bp.route('/')
def index():
    f = subprocess.Popen(['tail', '-n', '100', '/home/masa/Documents/MinecraftServers/Vanilla1-12-2/logs/latest.log'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    messages = []
    while True:
        line = f.stdout.readline()
        if not line:
            break
        if "Server thread" not in line:
            continue
        line = line.split(" ")[0] + " " + ":".join(line.split(":")[3:])[1:]
        messages.append(cgi.escape(line))

    return render_template("template.jinja", messages=messages)
