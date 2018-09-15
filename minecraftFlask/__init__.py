import os

from flask import Flask
from flask import render_template
from mcstatus import MinecraftServer
import subprocess
import sys
import cgi
import socket

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/')
    def generateMCScreen():
        f = subprocess.Popen(['tail', '-n', '100', '/home/masa/Documents/MinecraftServers/Vanilla1-12-2/logs/latest.log'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        server = MinecraftServer("72.194.118.95",25565)

        try:
            server.ping()
            query = server.query()
        except socket.error:
            header = "Minecraft server currently down"
            body = ""
            return render_template("template.jinja", header=header, body=body)
        
        header = "&nbspThe server has the following players online ({}, {}):".format(
            query.players.online, query.players.max) + " " + \
            ", ".join(query.players.names)
        body = ""

        while True:
            line = f.stdout.readline()
            if not line:
                break
            if "Server thread" not in line:
                continue
            line = line.split(" ")[0] + " " + ":".join(line.split(":")[3:])[1:]
            body += cgi.escape(line) + "</br>\n"

        return render_template("template.jinja", header=header, body=body)
    return app