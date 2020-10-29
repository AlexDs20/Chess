import concurrent.futures
from itertools import repeat


def movesEval(m, board, depth, alpha, beta, maximizing):
    board.move(m[0], m[1])
    evaluation = minimax(board, depth-1, alpha, beta, not maximizing)
    board.undoMove()
    return evaluation


def minimaxPara(board, depth, alpha, beta, maximizing):
    """
    Run minimax in parallel at the root and alpha-beta pruning below
    """
    allMoves = board.getAllMoves()
    b = repeat(board)
    d = repeat(depth)
    a = repeat(alpha)
    bet = repeat(beta)
    maxs = repeat(maximizing)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        evals = list(executor.map(movesEval, allMoves, b, d, a, bet, maxs))
        index = evals.index(max(evals)) if maximizing else evals.index(min(evals))
        return evals[index], allMoves[index]


def minimaxRoot(board, depth, alpha, beta, maximizing):
    bestEval = float('-inf') if maximizing else float('inf')
    bestMove = []
    for m in board.getAllMoves():
        evaluation = movesEval(m, board, depth, alpha, beta, maximizing)
        bestEval = max(evaluation, bestEval) if maximizing else min(evaluation, bestEval)
        if bestEval == evaluation:
            bestMove = m
    return bestEval, bestMove


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

    bestEval = float('-inf') if maximizing else float('inf')
    for m in board.getAllMoves():
        evaluation = movesEval(m, board, depth, alpha, beta, maximizing)
        bestEval = max(evaluation, bestEval) if maximizing else min(evaluation, bestEval)
        if maximizing:
            alpha = max(alpha, bestEval)
        else:
            beta = min(beta, bestEval)
        if alpha >= beta:
            break
    return bestEval
