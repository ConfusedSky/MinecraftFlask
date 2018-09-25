from flask import (
    Blueprint, g, render_template, request, url_for, jsonify
)
import subprocess
import sys
import cgi
import socket
import os
from mcstatus import MinecraftServer
from . import socketio

bp = Blueprint('index', __name__)

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
    server = MinecraftServer("localhost", 25565)

    query = None
    messages = []

    try:
        query = server.query()

        serverUp = True

        while True:
            line = f.stdout.readline()
            if not line:
                break
            if "Server thread" not in line:
                continue
            line = line.split(" ")[0] + " " + ":".join(line.split(":")[3:])[1:]
            messages.append(cgi.escape(line))
    except socket.error:
        serverUp = False

    return render_template("template.jinja", serverUp=serverUp, query=query, messages=messages)
