import random
from board import Board
from player import Player
from referee import Referee
import math
import copy

class MCTSNode():
    def __init__(
            self, 
            should_maximize = True, 
            board=None, 
            ucb_c = math.sqrt(2)
        ):
        if board == None:
            self.board = Board()
        else:
            self.board = copy.deepcopy(board)
        self.is_visited = False
        self.is_fully_expanded = False
        self.should_maximize = should_maximize
        self.points = 0
        self.n_visits = 0
        self.children = []

    # value and ucb functions should never be called without at least
    #  one visit on the node
    def value(self):
        return self.points/float(self.n_visits)
    def ucb(self, N_parent):
        return math.sqrt(2)*math.sqrt(math.log(N_parent)/self.n_visits)

    def get_child_nodes(self):
        return [child[0] for child in self.children]

    def extend(self):
        if self.board.is_final():
            self.n_visits += 1
            self.n_points = self.board.get_points()
            return self.board.get_points()
        if self.n_visits == 0:
            # created child boards on first visit
            # notably, this assumes deterministic transition between states
            for move in self.board.get_available_moves():
#                print( self.board.get_available_moves())
                new_board = copy.deepcopy(self.board)
                new_board.enter_move(move)
                new_node = MCTSNode(not self.should_maximize, new_board)
                self.children.append((new_node,move))
            #playout
            player_a = Player()
            player_b = Player()
            ref = Referee()
            result = ref.playgame(
                player_a,
                player_b,
                board= self.board
            )
            if result == 'cat':
                result_points = .5
            if result == 'x':
                result_points = 1
            if result == 'o':
                result_points = 0
            self.n_visits = 1
            self.points = result_points
            return result_points

        elif (not self.is_fully_expanded):
            unexplored_children = filter(
                lambda a_child: a_child.n_visits == 0,
                self.get_child_nodes()
            )
            to_extend = next(unexplored_children)
            result_points = to_extend.extend()
            self.n_visits += 1
            self.points += result_points 
            if not next(unexplored_children,False):
                # unexplored children are empty
                self.is_fully_expanded = True
            return result_points

        elif self.should_maximize:
            best_child = max(
                self.get_child_nodes(),
                key= lambda x: x.value()+x.ucb(self.n_visits)
            )
            result_points = best_child.extend()
            self.n_visits += 1
            self.points += result_points
            return result_points
        else:
            best_child = min(
                self.get_child_nodes(), 
                key = lambda x: x.value() - x.ucb(self.n_visits)
            )
            result_points = best_child.extend()
            self.n_visits += 1
            self.points += result_points
            return result_points

class MCTSPlayer(Player):

    def get_move(self,board):
        mcts_master = MCTSNode(
            should_maximize=self.token == 'x',
            board = copy.deepcopy(board)
        )
        for i in range(40):
            mcts_master.extend()
        most_visited = max(
            mcts_master.children,
            key = lambda a_child: a_child[0].n_visits
        )
        return most_visited[1]
#        available = board.get_available_moves()
#        return random.choice(available)


if __name__ == '__main__':
    print("no tests defined in main yet")
