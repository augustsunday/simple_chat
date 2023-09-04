from chat_socket import *
from chat_handler import *


def client():
    # The client does not create a connection - it simply attempts to connect to an assumed connection at HOST:PORT
    # Once connected, connection control is passed to a ChatHandler which mediates chat with the server-side ChatHandler

    # Set hostname and port to listen on
    HOST = "localhost"
    PORT = 59125

    try:
        # create an INET, STREAMing socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # We will reuse this socket
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
        s.connect((HOST, PORT))
    except socket.error:
        raise RuntimeError(f"Unable to connect to {HOST}:{PORT} ")

    connection = ChatSocket(s)

    # Pass our connection off to chat handler so it can mediate the conversation w/ server
    # Client goes first per specifications

    handler = ChatHandler(connection, 'XMIT', False)
    handler.mediate_chat()


if __name__ == '__main__':
    client()
