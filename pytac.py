# design idea:

### Entities
# Board - contains game state
# Ref - creates board, asks for move, checks move legality, updates board, etc
# Player - accepts board, asks evaluator for input, updates move values, returns best move 
# Evaluator - evaluates board, returns 

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
        board_dim = 3
        self.rows = [["_" for j in range(3)] for i in range(3)]

    def __str__(self):
        return "\n".join(["".join(row) for row in self.rows])

    def is_final(self):
        
        # zipping the rows together gives the columns, since zip makes n lists
        #  from a list of length m, consisting of sub-lists of length n
        cols = zip(*[self.rows[i] for i in range(3)])
        diag1 = [self.rows[0][0],self.rows[1][1],self.rows[2][2]]
        diag2 = [self.rows[0][2],self.rows[1][1],self.rows[2][0]]
        is_x = constant_sequence_check_generator('x')
        is_y = constant_sequence_check_generator('y')
        
        lines = self.rows + list(cols) + [diag1,diag2]
        if any(map(lambda line: is_x(line) or is_y(line),lines)):
            return True
        else:
            return False


    def enter_move(self,move_tuple,player):
        i, j = move_tuple
        
        if   player == "x":
            self.rows[i][j] = "x"
        elif player == "o":
            self.rows[i][j] = "o"
        else:
           raise ValueError("expected player x or o, received {}".format(player))



if __name__ == '__main__':
    board = Board()
    moves = [(0,0),(0,1),(0,2)]
    for move in moves:
        board.enter_move(move,'x')
        print(board)
        print(board.is_final())
    assert(board.is_final())
    
    board = Board()
    moves_2 = [(0,0),(1,1),(2,2)]
    for move in moves_2:
        board.enter_move(move,'x')
        print(board)
        print(board.is_final())
    assert(board.is_final())

    board = Board()
    moves_3 = [(0,2),(1,1),(2,0)]
    for move in moves_3:
        board.enter_move(move,'x')
        print(board)
        print(board.is_final())
    assert(board.is_final())









