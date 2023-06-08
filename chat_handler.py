# Author: Colin Cummins
# Github Username: augustsunday
# Date: 6/7/2023
# Description: The chat handler class accepts a ChatSocket and uses it to mediate a conversation,
# implementing turn taking while sending and receiving messages, handling /q commands to quit, and /playrps
from game_handler import *


class ChatHandler:
    def __init__(self, connection, mode, current_turn='client'):
        """
        Class constructor
        :param connection: a ChatSocket to use for sending and receiving messages
        :param mode: Is this handler a 'client' or a 'server'. Also used for managing turn-taking.
        'client' - Client sends next message
        'server' - Server sends next message
        """
        self.connection = connection
        self.mode = mode
        self.current_turn = current_turn

        print("Welcome to SimpleChat")
        print("You may enter messages when the prompt appears")
        print()
        print("Special Commands:")
        print("/q.....(q)uit Chat")
        print("/p.....(p)lay 'Rock, Paper, Scissors' with chat partner")
        print("/x.....e(x)it 'Rock,Paper,Scissors' game")
        print()

    def ismyturn(self):
        return self.mode == self.current_turn

    def isserver(self):
        return self.mode == "server"

    def endturn(self):
        self.current_turn = 'client' if self.current_turn == 'server' else 'server'

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
                if self.ismyturn():
                    message = input("Enter Message> ")
                    if message == '/p' and self.isserver():
                        self.endturn()
                        game = GameHandler(self.current_turn, self.connection)
                        self.current_turn = game.play_rps()
                    elif message == '/q':
                        self.connection.send("", "QUIT")
                        print('<Exiting chat>')
                        return
                    else:
                        self.connection.send(message)
                        self.endturn()
                else:
                    code, message = self.connection.recv()
                    if code == 'PLAY' and self.isserver():
                        self.endturn()
                        game = GameHandler(self.current_turn, self.connection)
                        self.current_turn = game.play_rps()
                    elif code == "QUIT":
                        print('<Chat connection closed by partner>')
                        return
                    elif code == "OVER":
                        print("REPLY >", message)
                        self.endturn()
                    elif code == "XXXX":
                        print("REPLY >", message)
