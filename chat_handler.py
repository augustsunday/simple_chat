# Author: Colin Cummins
# Github Username: augustsunday
# Date: 6/7/2023
# Description: The chat handler class accepts a ChatSocket and uses it to mediate a conversation,
# implementing turn taking while sending and receiving messages, handling /q commands to quit, and /playrps
#
# Citations: None. While ChatSocket uses outside code, this class is original.
from game_handler import *


class ChatHandler:
    def __init__(self, connection, mode:str, server:bool=False):
        """
        Class constructor
        :param connection: a ChatSocket to use for sending and receiving messages
        :param mode: Are we accepting messages, or is the channel clear for us to transmit?
                    one of 'RECV' or 'XMIT' (str)
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
        print()

    def is_server(self):
        """
        Is this handler being as a server?
        """
        return self.server

    def flip_mode(self):
        """
        Flip mode from transmit to receive, and vice versa
        """
        self.mode = 'XMIT' if self.mode == 'RECV' else 'RECV'

    def handle_game_exit(self, game_exit_status):
        """
        Passes control back to ChatHandler after GameHandler is done
        When we leave the game, both client and server should be in RECV mode
        If the client _exits_ the game, chat control is given back to server, and vice versa
        If either quits the game, final closing messages are sent and the chat_handler shuts down
        :param game_exit_status:
        :return:
        """
        if game_exit_status == 'quit':
            try:
                self.connection.send("", "QUIT")
            finally:
                print('<Exiting chat>')
                exit(0)
        elif game_exit_status == 'server':
            self.connection.send("", "WAKE")
        elif game_exit_status == 'client':
            self.flip_mode()
        else:
            raise RuntimeError

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
                        self.connection.send("/q", "QUIT")
                        print('<Exiting chat>')
                        exit(0)
                    elif message == '/p' and self.is_server():
                        rps_game = GameHandler(self.connection, "server")
                        self.flip_mode()
                        game_exit_status = rps_game.mediate_game()
                        self.handle_game_exit(game_exit_status)

                    elif message == '/p':
                        self.connection.send("", "PLAY")
                        self.flip_mode()
                    else:
                        self.connection.send(message)
                        self.flip_mode()
                elif self.mode == 'RECV':
                    code, message = self.connection.recv()
                    if code == "QUIT":
                        print('<Chat connection closed by partner>')
                        exit(0)
                    elif code == "PLAY" and self.is_server():
                        rps_game = GameHandler(self.connection, "client")
                        game_exit_status = rps_game.mediate_game()
                        self.handle_game_exit(game_exit_status)
                    elif code == "XXXX":
                        print(message)
                    elif code == "WAKE":
                        self.flip_mode()
                    elif code == "OVER":
                        print("REPLY >", message)
                        self.flip_mode()
                    else:
                        raise RuntimeError
