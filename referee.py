from board import Board
import copy

class Referee():
    
    def __init__(self):
        self.board = None
        self.players = []


    def playgame(
            self,
            player1,
            player2,
            board= None,
            should_print = False,
            lookup = None
        ):
        # playgame takes two players, asks them to get ready,
        if board is None:
            self.board = Board()
        else:
            self.board = copy.deepcopy(board)

        player1.ready(token='x')
        player2.ready(token='o')
        
        player_dict = {
            "x": player1,
            "o": player2
        }
#        player1_tuple = (player1,'x')
#        player2_tuple = (player2,'o')

#        active_player_tuple = player1_tuple
        while not self.board.is_final():
            active_token  = self.board.get_token_to_move()
            active_player = player_dict[active_token]
            player_move   = active_player.get_move(copy.deepcopy(self.board))
            self.board.enter_move(player_move)
            if should_print:
                print("\n")
                print(self.board)
        game_result = self.board.get_result()
        if lookup is not None:
            if str(self.board) not in lookup:
                lookup[str(self.board)] = self.board.get_result()
                #print("known terminal states in lookup after addition: ", len(lookup))
        return self.board.get_result()


