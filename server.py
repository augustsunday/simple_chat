from chat_handler import ChatHandler
from chat_socket import *


def server():
    # Creates a server listening at HOSTNAME:PORT for a single client connection.
    # Once a connection is established the server passes control of the connection to a chat handler, allowing the
    # server-side user to chat with the client-side user
    HOSTNAME = "localhost"
    PORT = 59125

    # Establish Server Socket and listen for a connection
    try:
        # create an INET, STREAMing socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # We will reuse this socket
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
        # bind the socket to a public host, and a well-known port
        sock.bind((HOSTNAME, PORT))
        # become a server socket with 1 connection available
        sock.listen(1)
        print(f"Server socket opened at {HOSTNAME}:{PORT}")
    except socket.error:
        raise RuntimeError(f"Unable to create server socket at {HOSTNAME}:{PORT} ", __name__)

    print("Listening for client connection...")

    try:
        clientsocket, address = sock.accept()
        print(f"Client connected from {address}")
    except socket.error:
        raise RuntimeError("Unable to accept connection from client!")

    connection = ChatSocket(clientsocket)

    # Pass our connection off to chat handler so it can mediate the conversation w/ server
    # Client goes first by default

    handler = ChatHandler(connection, 'RECV', True)
    handler.mediate_chat()


if __name__ == '__main__':
    server()
