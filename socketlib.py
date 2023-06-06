"""
Socket Libraries for Chat Client

Adapted from "Socket Programming HOWTO" by Gordon McMillan - https://docs.python.org/3.4/howto/sockets.html
"""

import socket


class ChatSocket:
    def __init__(self, hostname: str = "localhost", port: int = 49152):
        # create an INET, STREAMing socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # We will reuse this socket
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

class ServerSocket(ChatSocket):
    def __init__(self, hostname: str = "localhost", port: int = 49152):
        """
        Create server socket
        :param hostname: Hostname of socket
        :param port: Socket port
        """
        try:
            super().__init__(hostname, port)
            # bind the socket to a public host, and a well-known port
            self.sock.bind((hostname, port))
            # become a server socket with 1 connection available
            self.sock.listen(1)
            print(f"Server socket opened at {hostname}:{port}")

        except socket.error:
            raise RuntimeError(f"Unable to create server socket at {hostname}:{port} ", __name__)

    def accept(self):
        return self.sock.accept()


class ClientSocket(ChatSocket):
    def __init__(self, hostname: str = "localhost", port: int = 49152):
        """
        Create client socket
        :param hostname: Hostname of socket
        :param port: Socket port
        """
        try:
            super().__init__(hostname, port)
        except socket.error:
            raise RuntimeError(f"Client unable to connect to server at {hostname}:{port} ", __name__)

    def connect(self, hostname, port):
        try:
            self.sock.connect((hostname, port))
            print(f"Client connected to {hostname}:{port}")
        except socket.error:
            print(f"Client connection failed - {hostname}:{port}")
