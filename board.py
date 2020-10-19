import numpy as np
from pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King


class Board:
    """
    Board class

    TODO: function to return a list of boards where the next possible move has been done
          number of half moves since capture (to implement 50 moves rule)
          Fullmove number: start at 1 and increase after each black move
          Alternate move between white and black
    """

    def __init__(self, boardSize, fen):
        self.enPassant = []
        self.lastPiecesMoved = []
        self.player = []
        self.castling = []
        self.halfMoves = []
        self.fullMoves = []
        self.boardSize = boardSize
        self.initBoard(fen)

    def initBoard(self, fen):
        """
        Initiate the board for the given configuration
        TODO: implement the additional properties in the FEN format, not just the pieces posiitons
        """
        self.array = np.empty([self.boardSize, self.boardSize], dtype=object)
        i = 0
        j = self.boardSize-1
        config, self.player, self.castling, enPassant, self.halfMoves, self.fullMoves = fen.split(' ')
        if len(enPassant) == 2:
            self.enPassant = [ord(enPassant[0])-97, int(enPassant[1])]
        else:
            self.enPassant = enPassant

        for s in config:
            if s.isnumeric():
                i += int(s)
                continue
            if s.isupper():
                colour = 'white'
            else:
                colour = 'black'

            if s.lower() == 'p':
                self.array[i, j] = Pawn([i, j], colour, self)
            elif s.lower() == 'r':
                self.array[i, j] = Rook([i, j], colour, self)
            elif s.lower() == 'n':
                self.array[i, j] = Knight([i, j], colour, self)
            elif s.lower() == 'b':
                self.array[i, j] = Bishop([i, j], colour, self)
            elif s.lower() == 'q':
                self.array[i, j] = Queen([i, j], colour, self)
            elif s.lower() == 'k':
                self.array[i, j] = King([i, j], colour, self)
            i += 1
            if s == '/':
                j -= 1
                i = 0

    def move(self, moveFrom, moveTo):
        """
        Make a move!
        + Pawn promotion
        and remember if either the king or the rook moved as it forbids castling
        """
        if moveTo in self.array[moveFrom[0], moveFrom[1]].possibleMoves():
            # Append the piece at start and end of the move to move back if needed
            self.lastPiecesMoved = []
            self.lastPiecesMoved.append(self.array[moveTo[0], moveTo[1]])
            self.lastPiecesMoved.append(self.array[moveFrom[0], moveFrom[1]])

            self.array[moveTo[0], moveTo[1]] = self.array[moveFrom[0], moveFrom[1]]
            self.array[moveFrom[0], moveFrom[1]] = None

            if isinstance(self.array[moveTo[0], moveTo[1]], Pawn):
                # If Pawn on first/last rank: Promote
                if ((self.array[moveTo[0], moveTo[1]].colour == 'black' and moveTo[1] == 0) or
                        (self.array[moveTo[0], moveTo[1]].colour == 'white' and moveTo[1] == self.boardSize-1)):
                    promoteTo = input('Promote into a:')
                    self.promotePawn(moveTo, promoteTo)
                # If pawn moves en passant: remove pawn
                if moveTo in [self.enPassant]:
                    if self.array[moveTo[0], moveTo[1]].colour == 'white':
                        self.array[moveTo[0], moveTo[1]-1] = None
                    else:
                        self.array[moveTo[0], moveTo[1]+1] = None
                # If enPassant possible: save where the next pawn can go
                self.enPassant = '-'
                if abs(moveTo[1]-moveFrom[1]) == 2:
                    if self.array[moveTo[0], moveTo[1]].colour == 'white':
                        self.enPassant = [moveTo[0], moveTo[1]-1]
                    else:
                        self.enPassant = [moveTo[0], moveTo[1]+1]
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

                # Save the move
                self.lastPiecesMoved.append(self.array[rookTo[0], rookTo[1]])
                self.lastPiecesMoved.append(self.array[rookFrom[0], rookFrom[1]])

                # Make move
                self.array[rookTo[0], rookTo[1]] = self.array[rookFrom[0], rookFrom[1]]
                self.array[rookFrom[0], rookFrom[1]] = None
                self.array[rookTo[0], rookTo[1]].updateMove([rookTo[0], rookTo[1]])

    def undoMove(self):
        """
        Undo the last move
        """
        for piece in self.lastPiecesMoved:
            if isinstance(piece, Piece):
                self.array[piece.coord[0], piece.coord[1]] = piece

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

    def eval(self):
        """
        Evaluates the state of the board
        """
        evaluation = 0
        for col in self.array:
            for square in col:
                if isinstance(square, Piece):
                    if square.colour == 'white':
                        evaluation += square.value
                    else:
                        evaluation -= square.value
        return evaluation

    def nextConfigs(self):
        """
        Return a list of boards where the next possible move is already played
        Each returned board are obtained from a different move
        """
        Configs = []
        for i, col in enumerate(self.array):
            for j, square in enumerate(col):
                if isinstance(square, Piece):
                    moves = square.possibleMoves()
                    for m in moves:
                        # b = copy.deepcopy(self)
                        # b.move([i, j], m)
                        # b.undoMove()
                        pass
        return Configs

    def getFEN(self):
        """
        Returns the configuration of the board in the Forsyth-Edwards Notation
        """
        b = ''
        for i in range(self.boardSize-1, -1, -1):
            empty = 0
            for j in range(self.boardSize):
                square = self.array[j, i]
                if isinstance(square, Piece) and empty != 0:
                    b += str(empty)
                    empty = 0
                if isinstance(square, Pawn):
                    b += 'p'
                elif isinstance(square, Rook):
                    b += 'r'
                elif isinstance(square, Knight):
                    b += 'n'
                elif isinstance(square, Bishop):
                    b += 'b'
                elif isinstance(square, King):
                    b += 'k'
                elif isinstance(square, Queen):
                    b += 'q'
                elif square is None:
                    empty += 1
                if isinstance(square, Piece) and square.colour == 'white':
                    b = b[0: -1] + b[-1].upper()
            if empty != 0:
                b += str(empty)
                empty = 0
            b += '/'
        if i == 0 and j == self.boardSize-1:
            if len(self.enPassant) == 2:
                enPassant = chr(self.enPassant[0]+97) + str(self.enPassant[1])
            else:
                enPassant = self.enPassant
            fen = "%s %s %s %s %s %s" % (b[:-1], self.player, self.castling, enPassant, self.halfMoves, self.fullMoves)
        return fen

    def __str__(self):
        checkerBoard = np.zeros([self.boardSize, self.boardSize], dtype=str)
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if isinstance(self.array[i, j], Pawn):
                    checkerBoard[i, j] = 'p'
                elif isinstance(self.array[i, j], Rook):
                    checkerBoard[i, j] = 'r'
                elif isinstance(self.array[i, j], Knight):
                    checkerBoard[i, j] = 'n'
                elif isinstance(self.array[i, j], Bishop):
                    checkerBoard[i, j] = 'b'
                elif isinstance(self.array[i, j], King):
                    checkerBoard[i, j] = 'k'
                elif isinstance(self.array[i, j], Queen):
                    checkerBoard[i, j] = 'q'
                elif self.array[i, j] is not None:
                    checkerBoard[i, j] = 0
                if (isinstance(self.array[i, j], Piece) and
                   self.array[i, j].colour == 'white'):
                    checkerBoard[i, j] = checkerBoard[i, j].upper()
        return np.array_str(checkerBoard)
