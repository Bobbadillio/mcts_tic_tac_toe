from board import Board
import copy

class Referee():
    
    def __init__(self):
        self.board = None
        self.players = []


    def playgame(self,player1,player2, board= None):
        # playgame takes two players, asks them to get ready,
        if board is None:
            self.board = Board()
        else:
            self.board = board

        player1.ready(token='x')
        player2.ready(token='o')
        
        player_dict = {
            "x": player1,
            "o": player2
        }
        player1_tuple = (player1,'x')
        player2_tuple = (player2,'o')

        active_player_tuple = player1_tuple
#        print("starting game!")
#        print(self.board)
        while not self.board.is_final():
            active_token  = self.board.get_token_to_move()
#            print ("player to move: %s" % active_token)
            active_player = player_dict[active_token]
            player_move   = active_player.get_move(copy.copy(self.board))
            self.board.enter_move(player_move, active_token)
#            print(self.board)
#        print(self.board)
        return self.board.get_result()


