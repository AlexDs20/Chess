def minimaxRoot(board, depth, alpha, beta, maximizing):
    """
    TODO:   multiprocessing -> split the root branching between processes
    """
    if maximizing:
        maxEval = float('-inf')
        moveMax = []
        for m in board.getAllMoves():
            board.move(m[0], m[1])
            evaluation = minimax(board, depth-1, alpha, beta, False)
            board.undoMove()
            maxEval = max(evaluation, maxEval)
            if maxEval == evaluation:
                moveMax = m
        return maxEval, moveMax
    else:
        minEval = float('inf')
        moveMin = []
        for m in board.getAllMoves():
            board.move(m[0], m[1])
            evaluation = minimax(board, depth-1, alpha, beta, True)
            board.undoMove()
            minEval = min(evaluation, minEval)
            if minEval == evaluation:
                moveMin = m
        return minEval, moveMin


def minimax(board, depth, alpha, beta, maximizing):
    """
    give the board and use minimax to return the best move for a given depth.
    If maximizing is True, we maximize the move, otherwise, we minimize
    """

    getCheckmate, _ = board.checkmate(board.player)
    setCheckmate, _ = board.checkmate(board.otherPlayer)

    if depth == 0 or setCheckmate or getCheckmate:
        value = board.eval()
        if setCheckmate and board.player == 'white':
            value = float('inf')
        elif setCheckmate and board.player == 'black':
            value = float('-inf')
        if getCheckmate and board.player == 'white':
            value = float('-inf')
        elif getCheckmate and board.player == 'black':
            value = float('inf')
        return value

    if maximizing:
        maxEval = float('-inf')
        for m in board.getAllMoves():
            board.move(m[0], m[1])
            evaluation = minimax(board, depth-1, alpha, beta, False)
            board.undoMove()
            maxEval = max(evaluation, maxEval)
            alpha = max(alpha, maxEval)
            if alpha >= beta:
                break
        return maxEval
    else:
        minEval = float('inf')
        for m in board.getAllMoves():
            board.move(m[0], m[1])
            evaluation = minimax(board, depth-1, alpha, beta, True)
            board.undoMove()
            minEval = min(evaluation, minEval)
            beta = min(beta, minEval)
            if beta <= alpha:
                break
        return minEval
