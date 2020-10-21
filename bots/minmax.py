def minimax(board, depth, maximizing):
    """
    give the board and use minimax to return the best move for a given depth.
    If maximizing is True, we maximize the move, otherwise, we minimize

    TODO:   pruning tree
            multiprocessing -> split the branching between threads
    """
    checkmate, stalemate = board.checkmate(board.player)
    if depth == 0 or checkmate:
        return board.eval(), []

    if maximizing:
        maxEval = float('-inf')
        moveMax = []
        for nextConfig in board.nextConfigs():
            evaluation, _ = minimax(nextConfig[0], depth-1, False)    # False because next is black to play
            maxEval = max(evaluation, maxEval)
            moveMax = nextConfig[1] if maxEval == evaluation else moveMax
        return maxEval, moveMax

    if not maximizing:
        minEval = float('inf')
        moveMin = []
        for nextConfig in board.nextConfigs():
            evaluation, _ = minimax(nextConfig[0], depth-1, True)    # False because next is white to play
            minEval = min(evaluation, minEval)
            moveMin = nextConfig[1] if minEval == evaluation else moveMin
        return minEval, moveMin
