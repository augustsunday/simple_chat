# Author: Colin Cummins
# Github Username: augustsunday
# Date: 6/7/2023
# Description: The chat handler class accepts a ChatSocket and uses it to mediate a conversation.

class ChatHandler:
    def __init__(self, connection, myturn):
        """
        Class constructor
        :param connection: a ChatSocket to use for sending and receiving messages
        :param myturn: Is it this handler's turn to talk? [bool]
        'client' - Client sends next message
        'server' - Server sends next message
        """
        self.connection = connection
        self.myturn = myturn

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
                if self.myturn:
                    message = input("Enter Message> ")
                    self.connection.send(message)
                    if message == '/q':
                        print('Exiting chat...')
                else:
                    message = self.connection.recv()
                    if message == '/q':
                        print('Chat connection closed by partner')
                        return
                    print("REPLY >", message)

                self.myturn = not self.myturn
