import random
from board import Board
from player import Player

class MCTSNode():
    def __init__(self,board=Board()):
        self.is_visited = False
        self.points = 0
        self.n_visits = 0
        self.children = []

    def value(self):
        if n_visits > 0:
            return n_points/float(n_visits)

    def extend(self,player_token):
        
        if self.n_visits == 0:
           player_a = Player()
           player_b = Player()


        if should_maximize:
            best_child = max(self.children, key= lambda x: x.value())
        else:
            best_child = min(self.children, key = lambda x: x.value())
        result = best_child.extend(not should_maximize)
        self.n_wins

class MCTSPlayer(Player):

    def get_move(self,board):
        mcts_master = MCTSNode(board)
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
