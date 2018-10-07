#!/usr/bin/env python

from __future__ import print_function

import getpass
import sys
import re
import signal

from minecraft import authentication
from minecraft.exceptions import YggdrasilError
from minecraft.networking.connection import Connection
from minecraft.networking.packets import Packet, clientbound, serverbound
from minecraft.compat import input


def get_options():
    options = {}
        
    options["username"] = input("Enter your username: ")

    options["password"] = getpass.getpass("Enter your password: ")

    return options


auth_token = authentication.AuthenticationToken()
try:
    with open('minecraft.auth', 'r') as f:
        auth_token.client_token, auth_token.access_token = f.read().splitlines()

    # Library has issues need to do some hackey stuff to make sure it works.
    # I would use validate, but that would require some rewriting as well.
    auth_token.username = "refresh"
    auth_token.refresh()
except (IOError, YggdrasilError):
    # IF there is no authentication file authenticate using username and password
    try:
        options = get_options()
        auth_token.authenticate(options["username"], options["password"])
    except YggdrasilError as e:
        print(e)
        sys.exit()

with open('minecraft.auth', 'w') as fout:
    fout.write(auth_token.client_token + '\n')
    fout.write(auth_token.access_token)

print("Logged in as %s..." % auth_token.username)
connection = Connection(
    "localhost", 25565, auth_token=auth_token)

def handle_join_game(join_game_packet):
    print('Connected.')

connection.register_packet_listener(
    handle_join_game, clientbound.play.JoinGamePacket)

# def print_chat(chat_packet):
    # print("Message (%s): %s" % (
        # chat_packet.field_string('position'), chat_packet.json_data))

# connection.register_packet_listener(
    # print_chat, clientbound.play.ChatMessagePacket)

# global connected
# connected = True

# def disconnect(disconnect_packet):
    # print("You were disconnected: %s" % disconnect_packet.json_data)
    # global connected
    # connected = False

# connection.register_packet_listener(disconnect, 
        # clientbound.play.DisconnectPacket)
connection.connect()

def sendChat(message):
    packet = serverbound.play.ChatPacket()
    packet.message = message
    connection.write_packet(packet)
    

# while connected:
    # try:
        # text = input()
        # if text == "/respawn":
            # print("respawning...")
            # packet = serverbound.play.ClientStatusPacket()
            # packet.action_id = serverbound.play.ClientStatusPacket.RESPAWN
            # connection.write_packet(packet)
        # else:
            # packet = serverbound.play.ChatPacket()
            # packet.message = text
            # connection.write_packet(packet)
    # except KeyboardInterrupt:
        # print("Bye!")
        # sys.exit()
