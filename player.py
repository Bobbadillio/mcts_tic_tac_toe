import random
from board import Board

class Player():

    def __init__(self):
        # Do nothing! Someday this should probably load a file or something
        # That will probably matter for a game that isn't trivially solved
        self.token = None
        self.randomizer = random.Random()

    def ready(self,token='x'): 
        self.token= token

    def reseed(self,seed):
        self.randomizer = random.Random(seed)

    def get_move(self,board):
        available = board.get_available_moves()
        return random.choice(available)


if __name__ == '__main__':
    board = Board()
    moves = [(0,0),(0,1),(0,2)]
    for move in moves:
        board.enter_move(move,'x')
    assert(board.is_final())
