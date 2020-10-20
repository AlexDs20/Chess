import numpy as np


def minimax(board, depth, maximizing):
    """
    give the board and use minimax to return the best move for a given depth.
    If maximizing is True, we maximize the move, otherwise, we minimize

    TODO:   returning the move to be played
            pruning tree
            multiprocessing -> split the branching between threads
    """
    checkmate, stalemate = board.checkmate()
    if depth == 0 or checkmate:
        return board.eval()

    if maximizing:
        maxEval = -np.inf
        for nextConfig in board.nextConfigs:
            evaluation = minimax(nextConfig, depth-1, False)    # False because next is black to play
            maxEval = max(evaluation, maxEval)
        return maxEval

    if not maximizing:
        minEval = np.inf
        for nextConfig in board.nextConfigs:
            evaluation = minimax(nextConfig, depth-1, True)    # False because next is white to play
            minEval = min(evaluation, minEval)
        return minEval
