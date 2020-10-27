def minimax(board, depth, maximizing):
    """
    give the board and use minimax to return the best move for a given depth.
    If maximizing is True, we maximize the move, otherwise, we minimize

    TODO:   alpha-beta pruning tree
            multiprocessing -> split the root branching between threads
    """

    checkmate, stalemate = board.checkmate(board.player)
    if depth == 0 or checkmate:
        return board.eval(), []

    if maximizing:
        maxEval = float('-inf')
        moveMax = []
        """
        for nextConfig in board.nextConfigs():
            evaluation, _ = minimax(nextConfig[0], depth-1, False)
                moveMax = nextConfig[1]
        """
        for m in board.getAllMoves():
            board.move(m[0], m[1])
            evaluation, _ = minimax(board, depth-1, False)
            board.undoMove()
            maxEval = max(evaluation, maxEval)
            if maxEval == evaluation:
                moveMax = m
        return maxEval, moveMax
    else:
        minEval = float('inf')
        moveMin = []
        """
        for nextConfig in board.nextConfigs():
            evaluation, _ = minimax(nextConfig[0], depth-1, True)
                moveMin = nextConfig[1]
        """
        for m in board.getAllMoves():
            board.move(m[0], m[1])
            evaluation, _ = minimax(board, depth-1, True)
            board.undoMove()
            minEval = min(evaluation, minEval)
            if minEval == evaluation:
                moveMin = m
        return minEval, moveMin
