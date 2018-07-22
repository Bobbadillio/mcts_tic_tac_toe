# design idea:
from board import Board
from player import Player
from tictac_mcts import MCTSPlayer
from referee import Referee
import copy

### Entities
# Board - contains game state
# Ref - creates board, asks for move, checks move legality, updates board etc
# Player - takes board, asks evaluator's input, revalues actions returns best
# Evaluator - evaluates board, returns 

if __name__ == '__main__':
    board = Board()
    moves = [(0,0),(0,1),(0,2)]
    for move in moves:
        board.enter_move(move,'x')
    assert(board.is_final())
    
    board = Board()
    moves_2 = [(0,0),(1,1),(2,2)]
    for move in moves_2:
        board.enter_move(move,'x')
    assert board.is_final(), "board should be terminal for x"

    board = Board()
    moves_3 = [(0,2),(1,1),(2,0)]
    for move in moves_3:
        board.enter_move(move,'x')
    assert board.is_final(), "board should be terminal for x"
    
    board = Board()
    moves = [(0,0),(0,1),(0,2)]
    for move in moves:
        board.enter_move(move,'o')
    assert board.is_final(), "board should be terminal for o"
    
    board = Board()
    moves_2 = [(0,0),(1,1),(2,2)]
    for move in moves_2:
        board.enter_move(move,'o')
    assert board.is_final(), "board should be terminal for o"

    board = Board()
    moves_3 = [(0,2),(1,1),(2,0)]
    for move in moves_3:
        board.enter_move(move,'o')
    assert board.is_final(), "board should be terminal for o"


    n_games = 10
    player_a = Player()
    player_b = MCTSPlayer()
    ref = Referee()
    results = []
    print ("begin to play!")
    for i in range(n_games):
        player_a.reseed(i)
        player_b.reseed(i)
        result = ref.playgame(player_a,player_b)
        results.append(result)
    for i in range(n_games):
        player_a.reseed(i)
        player_b.reseed(i)
        result = ref.playgame(player_b,player_a)
        results.append(result)
    print(results)
        







