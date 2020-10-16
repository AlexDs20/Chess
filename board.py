import numpy as np
from pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King


class Board:
    def __init__(self, UI):
        self.boardSize = UI.boardSize
        self.UI = UI
        self.initBoard()
        self.enPassant = []
        # Not used
        self.info = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}

    def initBoard(self):
        self.array = np.empty([self.boardSize, self.boardSize], dtype=object)

        for i in range(self.boardSize):
            self.array[i, 1] = Pawn([i, 1], 'white', self)
            self.array[i, self.boardSize-2] = Pawn([i, self.boardSize-2], 'black', self)
        self.array[0, 0] = Rook([0, 0], 'white', self)
        self.array[7, 0] = Rook([7, 0], 'white', self)
        self.array[1, 0] = Knight([1, 0], 'white', self)
        self.array[6, 0] = Knight([6, 0], 'white', self)
        self.array[2, 0] = Bishop([2, 0], 'white', self)
        self.array[5, 0] = Bishop([5, 0], 'white', self)
        self.array[3, 0] = Queen([3, 0], 'white', self)
        self.array[4, 0] = King([4, 0], 'white', self)
        self.array[0, self.boardSize-1] = Rook([0, self.boardSize-1], 'black', self)
        self.array[7, self.boardSize-1] = Rook([7, self.boardSize-1], 'black', self)
        self.array[1, self.boardSize-1] = Knight([1, self.boardSize-1], 'black', self)
        self.array[6, self.boardSize-1] = Knight([6, self.boardSize-1], 'black', self)
        self.array[2, self.boardSize-1] = Bishop([2, self.boardSize-1], 'black', self)
        self.array[5, self.boardSize-1] = Bishop([5, self.boardSize-1], 'black', self)
        self.array[3, self.boardSize-1] = Queen([3, self.boardSize-1], 'black', self)
        self.array[4, self.boardSize-1] = King([4, self.boardSize-1], 'black', self)

    def move(self, moveFrom, moveTo):
        """
        Make a move!
        + Pawn promotion
        and remember if either the king or the rook moved as it forbids castling
        """
        if moveTo in self.array[moveFrom[0], moveFrom[1]].possibleMoves():
            self.array[moveTo[0], moveTo[1]] = self.array[moveFrom[0], moveFrom[1]]
            self.array[moveFrom[0], moveFrom[1]] = None

            if isinstance(self.array[moveTo[0], moveTo[1]], Pawn):
                # If Pawn on first/last rank: Promote
                if ((self.array[moveTo[0], moveTo[1]].colour == 'black' and moveTo[1] == 0) or
                        (self.array[moveTo[0], moveTo[1]].colour == 'white' and moveTo[1] == self.boardSize-1)):
                    promoteTo = input('Promote into a:')
                    self.promotePawn(moveTo, promoteTo)
                # If pawn moves en passant: remove pawn
                if moveTo in self.enPassant:
                    if self.array[moveTo[0], moveTo[1]].colour == 'white':
                        self.array[moveTo[0], moveTo[1]-1] = None
                    else:
                        self.array[moveTo[0], moveTo[1]+1] = None
                # If enPassant possible: save where the next pawn can go
                self.enPassant = []
                if abs(moveTo[1]-moveFrom[1]) == 2:
                    if self.array[moveTo[0], moveTo[1]].colour == 'white':
                        self.enPassant = [[moveTo[0], moveTo[1]-1]]
                    else:
                        self.enPassant = [[moveTo[0], moveTo[1]+1]]
            self.array[moveTo[0], moveTo[1]].updateMove(moveTo)

            if isinstance(self.array[moveTo[0], moveTo[1]], King) and abs(moveTo[0] - moveFrom[0]) == 2:
                if moveTo[0] - moveFrom[0] == -2:
                    # Castle Queen side
                    rookFrom = [0, moveTo[1]]
                    rookTo = [moveTo[0]+1, moveTo[1]]
                elif moveTo[0] - moveFrom[0] == 2:
                    # Castle King side
                    rookFrom = [self.boardSize-1, moveTo[1]]
                    rookTo = [moveTo[0]-1, moveTo[1]]

                self.array[rookTo[0], rookTo[1]] = self.array[rookFrom[0], rookFrom[1]]
                self.array[rookFrom[0], rookFrom[1]] = None
                self.array[rookTo[0], rookTo[1]].updateMove([rookTo[0], rookTo[1]])
                # Move rook on the UI
                X, Y = self.UI.coordToPixel(rookTo[0], rookTo[1])
                self.UI.canvas.coords(self.array[rookTo[0], rookTo[1]].Image, [X, Y])

    def promotePawn(self, coord, promoteTo):
        """
        Promote pawn to desired piece.
        TODO: GUI for suggesting which piece
        """
        if promoteTo.lower() == "queen":
            self.array[coord[0], coord[1]] = Queen(
                [coord[0], coord[1]], self.array[coord[0], coord[1]].colour, self)
        elif promoteTo.lower() == "rook":
            self.array[coord[0], coord[1]] = Rook(
                [coord[0], coord[1]], self.array[coord[0], coord[1]].colour, self)
        elif promoteTo.lower() == "knight":
            self.array[coord[0], coord[1]] = Knight(
                [coord[0], coord[1]], self.array[coord[0], coord[1]].colour, self)
        elif promoteTo.lower() == "bishop":
            self.array[coord[0], coord[1]] = Bishop(
                [coord[0], coord[1]], self.array[coord[0], coord[1]].colour, self)

    def findKing(self, colour):
        """
        Find the coordinate of the king of colour colour
        """
        coord = None
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if isinstance(self.array[i, j], King) and self.array[i, j].colour == colour:
                    coord = [i, j]
                    break
        return coord

    def isCheck(self, coord, colour):
        """
        To look if a piece of colour at square coord is in check or not
        Needed for castle, checks and checkmate
        """
        check = False
        for i, col in enumerate(self.array):
            for j, square in enumerate(col):
                if square is not None and square.colour != colour:
                    moves = square.baseMoves().copy()
                    if isinstance(square, Pawn):
                        if [i, j+1] in moves:
                            moves.remove([i, j+1])
                        if [i, j+2] in moves:
                            moves.remove([i, j+2])
                        if [i, j-1] in moves:
                            moves.remove([i, j-1])
                        if [i, j-2] in moves:
                            moves.remove([i, j-2])
                    if coord in moves:
                        check = True
                        break
        return check

    def checkmate(self, colour):
        checkmate = True
        for column in self.array:
            for square in column:
                if isinstance(square, Piece) and square.colour == colour and square.possibleMoves():
                    checkmate = False
                    break
        return checkmate

    def print(self):
        checkerBoard = np.zeros([self.boardSize, self.boardSize])
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if isinstance(self.array[i, j], Pawn):
                    checkerBoard[i, j] = 1
                elif isinstance(self.array[i, j], Rook):
                    checkerBoard[i, j] = 2
                elif isinstance(self.array[i, j], Knight):
                    checkerBoard[i, j] = 3
                elif isinstance(self.array[i, j], Bishop):
                    checkerBoard[i, j] = 4
                elif isinstance(self.array[i, j], King):
                    checkerBoard[i, j] = 5
                elif isinstance(self.array[i, j], Queen):
                    checkerBoard[i, j] = 6
                elif self.array[i, j] is not None:
                    checkerBoard[i, j] = 9
        print(checkerBoard)
