import random

class Player():

    def __init__(self):
        # Do nothing! Someday this should probably load a file or something
        # That will probably matter for a game that isn't trivially solved
        self.token = None

    def ready(self,token='1'):
        self.token= token

    def get_move(self,board):
        available = board.get_available_moves()
        return random.choice(available)



