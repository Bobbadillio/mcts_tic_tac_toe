# design idea:
from board import Board
from player import Player
import copy
### Entities
# Board - contains game state
# Ref - creates board, asks for move, checks move legality, updates board etc
# Player - takes board, asks evaluator's input, revalues actions returns best
# Evaluator - evaluates board, returns 

class Referee():
    
    def __init__(self):
        self.board = None
        self.players = []


    def playgame(self,player1,player2):
        # playgame takes two players, asks them to get ready,
        self.board = Board()

        player1.ready(token='x')
        player2.ready(token='o')
        
        player_dict = {
            "x": player1,
            "o": player2
        }
        player1_tuple = (player1,'x')
        player2_tuple = (player2,'o')

        active_player_tuple = player1_tuple
        print("starting game!")
        print(self.board)
        while not self.board.is_final():
            active_token  = self.board.get_token_to_move()
            print ("player to move: %s" % active_token)
            active_player = player_dict[active_token]
            player_move   = active_player.get_move(copy.copy(self.board))
            self.board.enter_move(player_move, active_token)
            print(self.board)





if __name__ == '__main__':
    board = Board()
    moves = [(0,0),(0,1),(0,2)]
    for move in moves:
        board.enter_move(move,'x')
        print(board)
        print(board.is_final())
    print(board.get_available_moves())
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

    n_games = 10
    player_a = Player()
    player_b = Player()
    ref = Referee()
    print ("begin to play!")
    for _ in range(n_games):
        ref.playgame(player_a,player_b)
        







