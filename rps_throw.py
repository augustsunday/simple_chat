# Author: Colin Cummins
# Github Username: augustsunday
# Date: 6/8/2023
# Description: Implements a simple object to represent the 'throw' a player makes in a game of 'Rock, Paper, Scissors'
# Used by game handler to compare and print player throws
class RpsError(Exception):
    "Raised when trying to assign an invalid shape (other than: rock, paper, scissors, none) to an RpsThrow"

class RpsThrow:
    shape: str

    def __init__(self, shape):
        if shape not in ('rock', 'paper', 'scissors'):
            raise RpsError

        self.shape = shape

    def set_shape(self, shape):
        if shape not in ('rock', 'paper', 'scissors'):
            raise RpsError

        self.shape = shape

    def __eq__(self, other):
        return self.shape == other.shape

    def __gt__(self, other):
        return (self.shape == 'rock' and other.shape == 'scissors') or (self.shape == 'scissors' and other.shape == 'paper') or (self.shape == 'paper' and other.shape == 'rock')

    def __lt__(self, other):
        return (self.shape == 'rock' and other.shape == 'paper') or (
                self.shape == 'scissors' and other.shape == 'rock') or (
                self.shape == 'paper' and other.shape == 'scissors')

    def __repr__(self):
        return self.shape
