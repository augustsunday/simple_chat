# Author: Colin Cummins
# Github Username: augustsunday
# Date: 6/6/2023
# Description:
# Citations: Adapted from the 'MySocket' Class in 'Socket Programming HOWTO' by Gordon McMillan
# https://docs.python.org/3/howto/sockets.html
import socket


class ChatSocket:
    """
    The chat socket sends and receives messages.

    Messages consist of a string of utf-8 ascii characters of the format:
    LLLLCCCC[DDD...]

    L = Length code in decimal, left-filled with zeroes. This is the length of the actual data portion of the message.
    C = Special instruction codes:
        'XXXX' = Normal transmission. Do not transmit - keep connection clear for further incoming transmissions.
        'WAKE' = No message content, just wake up by going into XMIT mode.
        'OVER' = Transmission complete. Ready to receive replies.
        'QUIT' = Transmitter has quit the chat and closed their connection. (Usually a signal for receiver to quit too)
        'PLAY' = Transmitter requesting switch to game mode.
        'EXIT' = Transmitter requesting end game mode.
    """
    # init/enter/exit allow us to use keyword 'with'
    def __init__(self, sock: socket):
        self.sock = sock

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()

    def send(self, msg="", code="OVER"):
        """
        Sends a fully formed message with length code and instruction code
        Code is set for "OVER" by default since back-and-forth conversation is the norm
        Use "XXXX" for sending multiple messages, broadcasting, etc.
        :param msg: Human-readable content of message
        :param code: Special instructions to receiving handler
        :return: None
        """
        payload_length = len(msg)
        length_code = str(payload_length).zfill(4)
        msg = length_code + code + msg
        total_length = payload_length + 8

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
        Receive a message of arbitrary length from the connection
        :return:
        """
        # Get the length code first
        payload_length = int(self.recv_length(4))

        # Get the message code
        code = self.recv_length(4)
        message = self.recv_length(payload_length)

        return code, message
