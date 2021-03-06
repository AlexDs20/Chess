import numpy as np
import random
from pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King


class Board:
    """
    Board class

    TODO: implement castling rules to work with FEN notations
          number of half moves since capture (to implement 50 moves rule)
          Fullmove number: start at 1 and increase after each black move
          Good way to move save states of board
    """

    def __init__(self, boardSize, fen):
        self.player = []
        self.otherPlayer = []
        self.enPassant = []
        self.castling = 'KQkq'
        self.halfMoves = 0
        self.fullMoves = 1
        self.mate = False
        self.stalemate = False
        self.draw = False

        self.boardSize = boardSize
        self.array = np.empty([boardSize, boardSize], dtype=object)
        self.Configs = [fen]
        self.updateFENvariables()
        self.updateBoard()
        self.updateGameStatus()

    def updateFENvariables(self):
        """
        Init the variables with the input FEN
        """
        fen = self.Configs[-1]
        _, play, self.castling, enPassant, hM, fM = fen.split(' ')
        if play == 'w':
            self.player = 'white'
        else:
            self.player = 'black'
        self.otherPlayer = 'white' if self.player == 'black' else 'black'
        if len(enPassant) == 2:
            self.enPassant = [ord(enPassant[0])-97, int(enPassant[1])-1]
        else:
            self.enPassant = enPassant
        self.halfMoves = int(hM)
        self.fullMoves = int(fM)

    def updateBoard(self):
        """
        Update the board for the last state in in self.Configs
        """
        config = self.Configs[-1]
        self.array = np.empty([self.boardSize, self.boardSize], dtype=object)

        # Put the piece on the board
        i = 0
        j = self.boardSize-1
        for s in config:
            if s == ' ':
                break
            # skip empty squares
            if s.isnumeric():
                i += int(s)
                continue
            # Colour of piece
            if s.isupper():
                colour = 'white'
            else:
                colour = 'black'

            # Puts piece
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
            # New rank
            if s == '/':
                j -= 1
                i = 0

    def updateMoveCount(self, moveFrom, moveTo):
        """
        Update the move count for the different move rules
            - 50 moves rule:
                If no capture or pawn moves, update half moves by 1
                After 50 moves -> draw
            - full move:
                Starts at 1 and increase after each time black plays
        """
        squareTo = self.array[moveTo[0], moveTo[1]]
        PieceMove = self.array[moveFrom[0], moveFrom[1]]

        # If capture a piece or pawn move, reset counter
        if isinstance(squareTo, Piece) or isinstance(PieceMove, Pawn):
            self.halfMoves = 0
        else:
            self.halfMoves += 1

        if self.player == 'black':
            self.fullMoves += 1

    def pawnMove(self, moveFrom, moveTo):
        """
        Special pawn moves: Promote, en passant
        """
        # Promote
        if moveTo[1] == 0 or moveTo[1] == self.boardSize-1:
            # promoteTo = input('Promote into a:')
            # self.promotePawn(moveTo, promoteTo)
            self.promotePawn(moveTo, 'Queen')

        # If en passant: capture pawn
        if moveTo in [self.enPassant]:
            if self.array[moveTo[0], moveTo[1]].colour == 'white':
                self.array[moveTo[0], moveTo[1]-1] = None
            else:
                self.array[moveTo[0], moveTo[1]+1] = None

        # If moves 2 squares: save where the next pawn can go
        self.enPassant = '-'
        if abs(moveTo[1]-moveFrom[1]) == 2:
            if self.array[moveTo[0], moveTo[1]].colour == 'white':
                self.enPassant = [moveTo[0], moveTo[1]-1]
            else:
                self.enPassant = [moveTo[0], moveTo[1]+1]

    def kingMove(self, moveFrom, moveTo):
        if moveTo[0] - moveFrom[0] == -2:
            # Castle Queen side
            rookFrom = [0, moveTo[1]]
            rookTo = [moveTo[0]+1, moveTo[1]]
        elif moveTo[0] - moveFrom[0] == 2:
            # Castle King side
            rookFrom = [self.boardSize-1, moveTo[1]]
            rookTo = [moveTo[0]-1, moveTo[1]]

        # Move Rook
        self.array[rookTo[0], rookTo[1]] = self.array[rookFrom[0], rookFrom[1]]
        self.array[rookFrom[0], rookFrom[1]] = None
        self.array[rookTo[0], rookTo[1]].updateMove([rookTo[0], rookTo[1]])

    def updateCastlingVar(self, moveFrom, moveTo):
        piece = self.array[moveTo[0], moveTo[1]]

        if isinstance(piece, Rook):
            if moveFrom[0] == 0:
                side = 'q'
            elif moveFrom[0] == self.boardSize-1:
                side = 'k'
            else:
                side = ''
            if piece.colour == 'white':
                side = side.upper()
            self.castling = self.castling.replace(side, '')

        if isinstance(piece, King):
            if piece.colour == 'white':
                self.castling = self.castling.replace('K', '')
                self.castling = self.castling.replace('Q', '')
            else:
                self.castling = self.castling.replace('k', '')
                self.castling = self.castling.replace('q', '')

    def move(self, moveFrom, moveTo):
        """
        Make a move!
        + Pawn promotion
        and remember if either the king or the rook moved as it forbids castling
        """
        if (moveTo in self.array[moveFrom[0], moveFrom[1]].possibleMoves() and
           self.player == self.array[moveFrom[0], moveFrom[1]].colour):

            # 50 move rules and Full moves count
            self.updateMoveCount(moveFrom, moveTo)

            # Change who will play next turn
            self.player = self.array[moveFrom[0], moveFrom[1]].otherColour
            self.otherPlayer = self.array[moveFrom[0], moveFrom[1]].colour

            # Make move
            self.array[moveTo[0], moveTo[1]] = self.array[moveFrom[0], moveFrom[1]]
            self.array[moveFrom[0], moveFrom[1]] = None

            # Special moves:
            # Pawn moves
            if isinstance(self.array[moveTo[0], moveTo[1]], Pawn):
                self.pawnMove(moveFrom, moveTo)
            else:
                self.enPassant = '-'

            # Castling
            if isinstance(self.array[moveTo[0], moveTo[1]], King) and abs(moveTo[0] - moveFrom[0]) == 2:
                self.kingMove(moveFrom, moveTo)

            # update coordinates of moved piece
            self.array[moveTo[0], moveTo[1]].updateMove(moveTo)

            # update Castling rights
            self.updateCastlingVar(moveFrom, moveTo)

            # Save the new configuration
            self.Configs.append(self.getFEN())

            # Update checkmate/stalemate/50 moves rule status:
            self.updateGameStatus()

    def updateGameStatus(self):
        """
        Update the variables related to checkmate, stalemate and 50moves rule (halfmoves)
        """
        self.mate, self.stalemate = self.checkmate(self.player)

        if self.halfMoves == 100:
            self.draw = True

    def undoMove(self):
        """
        Undo the last move
        """
        self.Configs.pop()
        self.updateFENvariables()
        self.updateBoard()
        self.updateGameStatus()

    def promotePawn(self, coord, promoteTo):
        """
        Promote pawn to desired piece.
        TODO: GUI for suggesting which piece
        """
        self.array[coord[0], coord[1]] = Queen(
            [coord[0], coord[1]], self.array[coord[0], coord[1]].colour, self)
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
        """
        Checks if colour is in checkmate or stalemate
        """
        noMoves = True
        king = self.findKing(colour)
        check = self.isCheck(king, colour)
        for column in self.array:
            for square in column:
                if isinstance(square, Piece) and square.colour == colour and square.possibleMoves():
                    noMoves = False
                    break
            # Also break out of parent loop if needed
            if not noMoves:
                break

        checkmate, stalemate = False, False
        if noMoves and check:
            checkmate = True
        elif noMoves and not check:
            stalemate = True
        return checkmate, stalemate

    def eval(self):
        """
        Evaluates the state of the board
        """
        evaluation = 0
        for col in self.array:
            for square in col:
                if isinstance(square, Piece):
                    if square.colour == 'white':
                        evaluation += square.positionValue()
                    else:
                        evaluation -= square.positionValue()
        return evaluation/10.0

    def getAllMoves(self):
        """
        Get all the possible moves for the current player in a random order
        the format is:
            moves[i, 0] = starting position
            moves[i, 1] = end position
        """
        moves = []
        for i, col in enumerate(self.array):
            for j, square in enumerate(col):
                if isinstance(square, Piece) and square.colour == self.player:
                    pieceMoves = square.possibleMoves()
                    for m in pieceMoves:
                        moves.append([[i, j], m])
        random.shuffle(moves)
        return moves

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
                enPassant = chr(self.enPassant[0]+97) + str(self.enPassant[1]+1)
            else:
                enPassant = self.enPassant
            castling = '-' if self.castling == '' else self.castling
            fen = "%s %s %s %s %s %s" % (b[:-1], self.player[0], castling,
                                         enPassant, self.halfMoves, self.fullMoves)
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

    def __repr__(self):
        return "Board"
