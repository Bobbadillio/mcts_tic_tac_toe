"""
board.py is an implementation of a tic-tac-toe board for experimentation
  with MCTS and reinforcement learning.
"""
def constant_sequence_check_generator(constant):
    el_is_constant = lambda an_element: an_element == constant
    # checking a row to see if everything in that row is the constant we want
    #  is what a constant sequence checker does
    # construct and return a function that does that, based on the constant
    return lambda an_input: all(map(el_is_constant,an_input))

is_x = constant_sequence_check_generator('x')
is_y = constant_sequence_check_generator('y')

class Board():
    def __init__(self):
        self.game_name = "tic-tac-toe"
        self.board_dim = 3
        self.tokens = ['x','o']
        self.to_move = 'x'
        self.rows = [["_" for j in range(3)] for i in range(3)]

    def __str__(self):
        return "\n".join(["".join(row) for row in self.rows])

    def get_token_to_move(self):
        return self.to_move
    
    def set_token_to_move(self,token):
        self.to_move = token 

    def get_result(self):
        # zipping the rows together gives the columns, since zip makes n lists
        #  from a list of length m, consisting of sub-lists of length n
        cols = zip(*[self.rows[i] for i in range(3)])
        diag1 = [self.rows[0][0],self.rows[1][1],self.rows[2][2]]
        diag2 = [self.rows[0][2],self.rows[1][1],self.rows[2][0]]
        is_x = constant_sequence_check_generator('x')
        is_o = constant_sequence_check_generator('o')
        
        lines = self.rows + list(cols) + [diag1,diag2]
        if (any(map(lambda line: is_x(line), lines))):
            return 'x'
        elif (any(map(lambda line: is_o(line),lines))):  
            return 'o'
        elif len(self.get_available_moves()) == 0:
            return 'cat'
        else:
            return 'unf'

    def get_points(self):
        result = self.get_result()
        if result == 'cat':
            return .5
        if result == 'x':
            return 1
        if result == 'o':
            return 0
        else:
            print("debug this, get_points was called from nonterminal")
            return .5
        

    def is_final(self):
        
        # zipping the rows together gives the columns, since zip makes n lists
        #  from a list of length m, consisting of sub-lists of length n
        cols = zip(*[self.rows[i] for i in range(3)])
        diag1 = [self.rows[0][0],self.rows[1][1],self.rows[2][2]]
        diag2 = [self.rows[0][2],self.rows[1][1],self.rows[2][0]]
        is_x = constant_sequence_check_generator('x')
        is_o = constant_sequence_check_generator('o')
        
        lines = self.rows + list(cols) + [diag1,diag2]
        if (any(map(lambda line: is_x(line) or is_o(line),lines)) or
            len(self.get_available_moves()) == 0 ):
            return True
        else:
            return False

    def get_available_moves(self):
        available_moves = []
        for i, row in enumerate(self.rows):
            for j, entry in enumerate(row):
                if entry not in ('x','o'):
                    available_moves.append((i,j))
        return available_moves

    def enter_move(self,move_tuple):
        i, j = move_tuple
        active_token = self.get_token_to_move()
        self.rows[i][j] = active_token
        if active_token == 'x':
            self.set_token_to_move('o')
        else:
            self.set_token_to_move('x')
