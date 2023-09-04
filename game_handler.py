from rps_throw import RpsError, RpsThrow

PROMPT_MESSAGE: str = 'Choose your play: (r)ock, (p)aper, (s)cissors'
OPENING_MESSAGE: str = " started a game of Rock, Paper, Scissors!\n\n\
Instructions:\n\
On your turn, enter (r)ock, (p)aper, or (s)cissors\n\
Paper beats rock, rock beats scissors, scissors beats paper\n\
Special Commands:\n\
/e to exit game\n\
/q to quit chat entirely\n\n"


class GameHandler:
    # Description: Takes over chat and runs a game of rock/paper/scissors until someone quits
    # Either player can exit the game early with:
    # '/e' to exit the game and return to normal chat
    # '/q' to quit chat entirely and close connection
    def __init__(self, connection, initiator):
        self.connection = connection
        self.initiator = initiator

    def broadcast(self, message):
        """
        Sends a message to both client and server, leaving both in RECV mode
        :param message: Message to send (str), max_length enforced
        :return: None
        """
        self.connection.send(message, 'XXXX')
        print(message)

    def mediate_game(self):
        """
        Mediates the game
        :return: Exit status for ChatHandler...
        'exit' - Someone exited chat entirely
        'client' - Client quit the game, return to chat and pass control to server
        'server' - Server quit the game, return to chat and pass control to client
        """
        self.broadcast(self.initiator + OPENING_MESSAGE)

        # Play objects to store plays.
        client_play = RpsThrow()
        server_play = RpsThrow()

        # Scores
        client_score = 0
        server_score = 0

        while True:
            client_play.reset()
            server_play.reset()
            self.broadcast("New game!")

            # Get plays from both players
            while client_play.shape is None:
                try:
                    self.connection.send(PROMPT_MESSAGE, "XXXX")
                    self.connection.send("", "WAKE")
                    code, play = self.connection.recv()

                    # Handle special commands
                    if play == '/e':
                        self.broadcast('<Client exited the game>')
                        return 'client'
                    if play == '/q':
                        print('<Client quit the chat>')
                        return 'quit'
                    client_play.set_shape(play)
                except RpsError:
                    self.connection.send("Invalid Play!", "XXXX")
            while server_play.shape is None:
                try:
                    print(PROMPT_MESSAGE)
                    play = input("Enter Message> ")

                    # Handle special commands
                    if play == '/e':
                        self.broadcast('<Server exited the game>')
                        return 'server'
                    if play == '/q':
                        self.broadcast('<Server quit the chat>')
                        return 'quit'
                    server_play.set_shape(play)

                except RpsError:
                    print("Invalid Play!")

            # Announce players and winner, adjust score
            play_summary = "Client play: " + client_play + " --- Server play: " + server_play
            self.broadcast(play_summary)

            if client_play > server_play:
                self.broadcast('Client wins!')
                client_score += 1
            if client_play < server_play:
                self.broadcast('Server wins!')
                server_score += 1
            if client_play == server_play:
                self.broadcast("It's a tie!")

            play_summary = "Client Score: " + str(client_score) + " --- Server Score: " + str(server_score) + "\n"
            self.broadcast(play_summary)
