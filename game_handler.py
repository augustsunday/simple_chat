# Author: Colin Cummins
# Github Username: augustsunday
# Date: 6/8/2023
# Description: Takes over chat and runs a game of rock/paper/scissors until someone quits
PROMPT_MESSAGE = 'Choose your play: (r)ock, (p)aper, (s)cissors'

class GameHandler:
    from rps_throw import RpsError, RpsThrow
    def __init__(self, current_turn, connection):
        self.current_turn = current_turn
        self.connection = connection
        self.mode = 'server'
        self.winner = None

    def get_play(self):
        if self.current_turn == 'client':
            self.connection.send(PROMPT_MESSAGE)
            return self.connection.recv()

        if self.current_turn == 'server':
            return input(PROMPT_MESSAGE)


    def play_rps(self):
        p1 = self.current_turn
        p2 = 'client' if self.current_turn == 'server' else 'server'
        with self.connection:
            p1_play = None
            p2_play = None
            while True:
                while p1_play is None:
                    current_play = self.get_play()
                    p1_play = RpsThrow(current_play)
                self.flip_mode()
                while p2_play is None:
                    current_play = self.get_play()
                    p2_play = RpsThrow(current_play)
                self.flip_mode()
