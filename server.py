# Author: Colin Cummins
# Github Username: augustsunday
# Date: 6/6/2023
# Description: Server program for chat

# Citations -
# The code to establish and connect sockets was adapted from the 'Socket Programming HOWTO'
# by Gordon McMillan https://docs.python.org/3/howto/sockets.html


import socket

from chat_handler import ChatHandler
from chat_socket import *


hostname = "localhost"
port = 59124

# Establish Server Socket and listen for a connection
try:
    # create an INET, STREAMing socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # We will reuse this socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
    # bind the socket to a public host, and a well-known port
    sock.bind((hostname, port))
    # become a server socket with 1 connection available
    sock.listen(1)
    print(f"Server socket opened at {hostname}:{port}")
except socket.error:
    raise RuntimeError(f"Unable to create server socket at {hostname}:{port} ", __name__)

print("Listening for client connection...")

try:
    clientsocket, address = sock.accept()
    print(f"Client connected from {address}")
except socket.error:
    raise RuntimeError("Unable to accept connection from client!")

connection = ChatSocket(clientsocket)

# Pass our connection off to chat handler so it can mediate the conversation w/ server
# Client goes first by default

handler = ChatHandler(connection, False)
handler.mediate_chat()