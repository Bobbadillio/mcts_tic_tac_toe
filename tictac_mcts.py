import random
from board import Board
from player import Player

class MCTSNode():
    def __init__(self):
        n_visits = 0
        n_wins = 0

    def value(self):
        return 0

class MCTSPlayer(Player):

    def get_move(self,board):
        mcts_master = MCTSNode()
        available = board.get_available_moves()
        return random.choice(available)


if __name__ == '__main__':
    board = Board()
    moves = [(0,0),(0,1),(0,2)]
    for move in moves:
        board.enter_move(move,'x')
        print(board)
        print(board.is_final())
    assert(board.is_final())
