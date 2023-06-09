# Author: Colin Cummins
# Github Username: augustsunday
# Date: 6/7/2023
# Description: The chat handler class accepts a ChatSocket and uses it to mediate a conversation,
# implementing turn taking while sending and receiving messages, handling /q commands to quit, and /playrps
from game_handler import *

max_message_len = 4096


class ChatHandler:
    def __init__(self, connection, mode, server=False):
        """
        Class constructor
        :param connection: a ChatSocket to use for sending and receiving messages
        :param mode: Are we accepting messages, or is the channel clear for us to transmit?
                    one of 'RECV' or 'XMIT'
        :param server: Is this handler running for a server? Mostly used to determine how to handle
        requests to play a game [bool]
        """
        self.connection = connection
        self.mode = mode
        self.server = server

        print("Welcome to SimpleChat")
        print("You may enter messages when the prompt appears")
        print()
        print("Special Commands:")
        print("/q.....(q)uit Chat")
        print("/p.....(p)lay 'Rock, Paper, Scissors' with chat partner")
        print("/x.....e(x)it 'Rock,Paper,Scissors' game")
        print()

    def is_server(self):
        return self.server

    def flip_mode(self):
        self.mode = 'XMIT' if self.mode == 'RECV' else 'RECV'

    def mediate_chat(self):
        """
        Mediates chat until someone quits or someone requests a game. On exit, returns a status to determine what to do next
        :return: Why did we exit the chat?
        'exit' - Someone quit the chat. Begin shutdown procedures
        'gclient' - Game mode activated, client is up first
        'gserver' - Game mode activated, server is up first
        """

        with self.connection:
            while True:
                if self.mode == 'XMIT':
                    message = input("Enter Message> ")
                    if message == '/q':
                        self.connection.send("", "QUIT")
                        print('<Exiting chat>')
                        return
                    else:
                        self.connection.send(message)
                        self.flip_mode()
                elif self.mode == 'RECV':
                    code, message = self.connection.recv()
                    if code == "QUIT":
                        print('<Chat connection closed by partner>')
                        return
                    elif code == "WAKE":
                        self.mode == 'XMIT'
                    elif code == "OVER":
                        print("REPLY >", message)
                        self.flip_mode()
                    elif code == "XXXX":
                        print("REPLY >", message)
                    else:
                        raise RuntimeError
