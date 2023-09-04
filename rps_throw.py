class RpsError(Exception):
    "Raised when trying to assign an invalid shape (other than: rock, paper, scissors, none) to an RpsThrow"


class RpsThrow:
    # Description: Implements a simple object to represent the 'throw' a player makes
    # in a game of 'Rock, Paper, Scissors'
    # Used by game handler to compare and display player throws
    shape: str

    def __init__(self):
        self.shape = None
        self.shape_dict = {
            'r': 'rock',
            'rock': 'rock',
            'p': 'paper',
            'paper': 'paper',
            's': 'scissors',
            'scissors': 'scissors',
        }

    def set_shape(self, shape):
        if shape not in self.shape_dict.keys():
            raise RpsError

        self.shape = self.shape_dict[shape]

    def reset(self):
        self.shape = None

    def __eq__(self, other):
        return self.shape == other.shape

    def __gt__(self, other):
        return (self.shape == 'rock' and other.shape == 'scissors') or (
                self.shape == 'scissors' and other.shape == 'paper') or (
                       self.shape == 'paper' and other.shape == 'rock')

    def __lt__(self, other):
        return (self.shape == 'rock' and other.shape == 'paper') or (
                self.shape == 'scissors' and other.shape == 'rock') or (
                       self.shape == 'paper' and other.shape == 'scissors')

    def __str__(self):
        return self.shape

    def __add__(self, other):
        return self.shape + other

    def __radd__(self, other):
        return other + self.shape
