# tictactoe AI
## implemented with MCTS + lookup table of observed outcomes

This project is an effort towards creating a board game playing agent.

## TODO
* Store game histories and terminal states to disk
	* exploring TFRecord and hdf5 for this. It would be nice to ensure that each board state is matched up to its result.
* Load terminal states from disk at start
* Replace evaluator with a function of board state, instead of random policy playout.

