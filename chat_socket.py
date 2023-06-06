# Author: Colin Cummins
# Github Username: augustsunday
# Date: 6/6/2023
# Description:
# Citations:
# This Class is adapted from the 'MySocket' Class in 'Socket Programming HOWTO' by Gordon McMillan
# https://docs.python.org/3/howto/sockets.html
import socket


class ChatSocket:
    def __init__(self, sock: socket):
        self.sock = sock

    def send(self, msg):
        payload_length = len(msg)
        length_code = str(payload_length).zfill(4)
        msg = length_code + msg
        total_length = payload_length + 4

        total_sent = 0
        while total_sent < total_length:
            sent = self.sock.send(msg[total_sent:].encode('utf-8'))
            if sent == 0:
                raise RuntimeError("socket connection broken")
            total_sent = total_sent + sent

    def recv_length(self, msg_len: int):
        """
        Helper function that receives and returns a message of specified length from socket
        :return: Message [str]
        """

        chunks = []
        bytes_recd = 0
        while bytes_recd < msg_len:
            chunk = self.sock.recv(msg_len)
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks).decode("utf-8")

    def recv(self):
        """
        Receives and returns a message of arbitrary length from other side of connection
        :return: Message from other side of connection [str]
        """
        # Get the length code first
        payload_length = int(self.recv_length(4))

        # Special handling for length codes goes here

        # Get the payload
        return self.recv_length(payload_length)
