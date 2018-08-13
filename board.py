"""
board.py is an implementation of a tic-tac-toe board for experimentation
  with MCTS and reinforcement learning.
"""
import numpy as np

def constant_sequence_check_generator(constant):
    el_is_constant = lambda an_element: an_element == constant
    # checking a row to see if everything in that row is the constant we want
    #  is what a constant sequence checker does
    # construct and return a function that does that, based on the constant
    return lambda an_input: all(map(el_is_constant,an_input))

is_x = constant_sequence_check_generator('x')
is_y = constant_sequence_check_generator('y')

point_dict = {
        "x":1,
        "cat":.5,
        "o":0
    }

class Board():
    def point_translator(result_string):
        return point_dict.get(result_string)

    def __init__(self):
        """
        use a rank-3 tensor to store 3, 3x3 boards
        1st 3x3 is all 0 or all 1, for x to move or o to move respectively
        2nd 3x3 is 1 for locations with an x in them
        3rd 3x3 is 1 for locations with on o in them
        """
        self.game_name = "tic-tac-toe"
        self.board_dim = 3
        self.tokens = ['x','o']
        self.board_state = np.zeros((3,3,3), dtype= np.bool)
#        self.to_move = 'x'
        self.rows = [["_" for j in range(3)] for i in range(3)]

    def __str__(self):
        rep = self.board_state[2,:,:]*2 + self.board_state[1,:,:]*1
        return str(rep)

    def get_token_to_move(self):
        return 'o' if self.board_state[0,0,0] else 'x'
#        return self.to_move
    
    def set_token_to_move(self,token):
        self.board_state[0,:,:] = False if token == 'x' else True
#        self.to_move = token 

    def get_result(self):
        # zipping the rows together gives the columns, since zip makes n lists
        #  from a list of length m, consisting of sub-lists of length n
        token_dims = self.board_state[1:,:,:]
        rows = np.sum(token_dims,axis=1)
        columns = np.sum(token_dims,axis=2)
        diagonal = np.trace(token_dims,axis1=1,axis2=2)
        back_diagonal = np.trace(np.fliplr(token_dims),axis1=1,axis2=2)

        if np.any(rows==3):
            if np.any(rows[0,:]==3):
                return 'x'
            else:
                return 'o'
        elif np.any(columns==3):
            if np.any(columns[0,:]==3):
                return 'x'
            else:
                return 'o'
        elif np.any(diagonal == 3):
            if diagonal[0]==3:
                return 'x'
            else:
                return 'o'
        elif np.any(back_diagonal==3):
            if diagonal[0] == 3:
                return 'x'
            else:
                return 'o'
        elif np.sum(token_dims) ==9:
            return 'cat'
        else:
            return 'unf'

#        cols = zip(*[self.rows[i] for i in range(3)])
#        diag1 = [self.rows[0][0],self.rows[1][1],self.rows[2][2]]
#        diag2 = [self.rows[0][2],self.rows[1][1],self.rows[2][0]]
#        is_x = constant_sequence_check_generator('x')
#        is_o = constant_sequence_check_generator('o')
#        
#        lines = self.rows + list(cols) + [diag1,diag2]
#        if (any(map(lambda line: is_x(line), lines))):
#            return 'x'
#        elif (any(map(lambda line: is_o(line),lines))):  
#            return 'o'
#        elif len(self.get_available_moves()) == 0:
#            return 'cat'
#        else:
#            return 'unf'

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
        result = self.get_result()
        return result != 'unf'
        
#        # zipping the rows together gives the columns, since zip makes n lists
#        #  from a list of length m, consisting of sub-lists of length n
#        cols = zip(*[self.rows[i] for i in range(3)])
#        diag1 = [self.rows[0][0],self.rows[1][1],self.rows[2][2]]
#        diag2 = [self.rows[0][2],self.rows[1][1],self.rows[2][0]]
#        is_x = constant_sequence_check_generator('x')
#        is_o = constant_sequence_check_generator('o')
#        
#        lines = self.rows + list(cols) + [diag1,diag2]
#        if (any(map(lambda line: is_x(line) or is_o(line),lines)) or
#            len(self.get_available_moves()) == 0 ):
#            return True
#        else:
#            return False

    def get_available_moves(self):
        indices = np.nonzero(
            np.logical_not(
                np.any(
                    self.board_state[1:,:,:],axis=0
                )
            )
        )
        available_moves = [(i,j) for i,j in np.transpose(indices)] 
#        print(self)
#        print(available_moves)
        return available_moves

    def enter_move(self,move_tuple):
        i, j = move_tuple
        active_token = self.get_token_to_move()
        if active_token == 'x':
            self.board_state[1,i,j] = True
            self.set_token_to_move('o')
        else:
            self.board_state[2,i,j] = True
            self.set_token_to_move('x')
