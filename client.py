# Author: Colin Cummins
# Github Username: augustsunday
# Date: 6/6/2023
# Description:
# Citations -
# The code to establish and connect sockets was adapted from the 'Socket Programming HOWTO'
# by Gordon McMillan https://docs.python.org/3/howto/sockets.html

import socket
from chat_socket import *
from chat_handler import *

host = "localhost"
port = 59124

try:
    # create an INET, STREAMing socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # We will reuse this socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
    s.connect((host, port))
except socket.error:
    raise RuntimeError(f"Unable to connect to {host}:{port} ")

connection = ChatSocket(s)

# Pass our connection off to chat handler so it can mediate the conversation w/ server
# Client goes first per specifications

handler = ChatHandler(connection, True)
handler.mediate_chat()

