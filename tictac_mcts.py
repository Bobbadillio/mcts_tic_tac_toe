import random
from board import Board
from player import Player
from referee import Referee
import math
import copy
import pickle as pkl

terminal_board_dict = {}
try:
    with open("board_dictionary.pkl",'rb') as check_dict:
        terminal_board_dict = pkl.load(check_dict)
        print(len(terminal_board_dict))
except Exception as e:
    print(e)

def raw_eval(board):
    if str(board) in terminal_board_dict:
        return terminal_board_dict[str(board)]
    player_a = Player()
    player_b = Player()
    ref = Referee()
    result = ref.playgame(
        player_a,
        player_b,
        board= board,
        lookup = terminal_board_dict
    )
    # print(len(terminal_board_dict))
    return result

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
            self.points += self.board.get_points()
            board_string = str(self.board)
            if board_string not in terminal_board_dict:
                terminal_board_dict[board_string] = self.board.get_result()
            return self.board.get_points()
        elif self.n_visits == 0:
            #print(self.board)
            #print(self.board.is_final())
            self.n_visits += 1
            # create child boards on first visit
            # notably, this assumes deterministic transition between states
            for move in self.board.get_available_moves():
                # consider each move
                # TODO: stop considering new moves if this is a forced win
                new_board = copy.deepcopy(self.board)
                new_board.enter_move(move)
                new_node = MCTSNode(not self.should_maximize, new_board)
                if new_board.is_final():
                    terminal_board_dict[str(new_board)] = new_board.get_result()
                if str(new_board) in terminal_board_dict:
                    new_result = terminal_board_dict[str(new_board)]
                    if self.should_maximize:
                        if new_result == 'x':
                            # x is to play, so only consider the force win
                            terminal_board_dict[str(self.board)] = 'x'
                            self.children = [(new_node,move)]
                            break
                        elif new_result == 'o':
                            # don't consider opponent wins
                            continue
                        else:
                            self.children.append((new_node,move))
                    elif not self.should_maximize:
                        # see above comments, and
                        # TODO: reduce code redundancy with above block
                        if new_result == 'o':
                            terminal_board_dict[str(self.board)] = 'o'
                            self.children = [(new_node,move)]
                            break
                        elif new_result == 'x':
                            continue
                        else:
                            self.children.append((new_node,move))

                    else:
                        self.children.append((new_node,move))
                else:
                    self.children.append((new_node,move))
            if len(self.children) == 0:
                # if only losing moves remain, pick one at random
                new_board = copy.deepcopy(self.board)
                new_move = random.choice(self.board.get_available_moves())
                new_board.enter_move(new_move)
                new_node = MCTSNode(not self.should_maximize, new_board)
                self.children.append((new_node,move))


            # return known winner for terminal positions
            # and return the random playout for unknown positions
            if str(self.board) in terminal_board_dict:
                # return known winner for terminal
                result = terminal_board_dict[str(self.board)]
            else:
                result = raw_eval(self.board)

            # process result of playout
            result_points = Board.point_translator(result)
            self.points += result_points
            return result_points
        elif str(self.board) in terminal_board_dict:
            winning_token = terminal_board_dict[str(self.board)]
            self.n_visits += 1
            terminal_points = Board.point_translator(winning_token)
            self.points += terminal_points

            return terminal_points

        elif self.board.is_final():
            raw_eval(self.board)
            self.n_visits += 1
            result_points = self.board.get_points()
            self.points += result_points
            return result_points

        elif (not self.is_fully_expanded):
            self.n_visits += 1
            # create a filter for children that have a forced win for me
            winning_children = filter(
                lambda a_child: (
                    str(a_child[0].board) in terminal_board_dict
                    ) and (
                        terminal_board_dict == 'x' if self.should_maximize else 'o'),
                self.get_child_nodes()
            )

            # move to that child and add this node to the list of forced
            # modify to filter for children that aren't forced for opponent
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
        # print(len(terminal_board_dict))
        mcts_master = MCTSNode(
            should_maximize = self.token == 'x',
            board = copy.deepcopy(board)
        )
        n_rollouts = 10
        for i in range(n_rollouts):
            # check if node solved, and return a winning move if it is
            for child in mcts_master.children:
                child_string = str(child[0].board)
                if ((child_string in terminal_board_dict)
                and (terminal_board_dict[child_string] == self.token)):
                    return child[1]
            # extend by monte carlo tree search
            mcts_master.extend()

        # choose a final move by whatever was most frequently visited
        most_visited = max(
            mcts_master.children,
            key = lambda a_child: a_child[0].n_visits
        )
        return most_visited[1]
    

if __name__ == '__main__':
    print("no tests defined in main yet")
