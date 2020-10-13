#!/bin/python3

import numpy as np
from tkinter import PhotoImage
import copy


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


class Piece:
    def __init__(self, coord, colour, board):
        self.colour = colour
        self.otherColour = None
        self.hasMoved = False
        if self.colour == 'white':
            self.otherColour = 'black'
        else:
            self.otherColour = 'white'

        self.coord = coord
        self.board = board

        # Graphics
        self.displayImage = None       # Created with PhotoImage
        self.Image = None              # Created with canvas.create_image

    def updateMove(self, moveTo):
        self.coord = moveTo
        self.hasMoved = True

    def resize(self):
        """
        TODO: Implement the resize function once svg files are done
        """
        # old_size = max(self.displayImage.width(), self.displayImage.height())
        # self.displayImage = self.displayImage.zoom(int(self.board.UI.squareSize * 0.9))
        # self.displayImage = self.displayImage.subsample(old_size)
        pass

    def possibleMoves(self):
        """
        From all the moves (allMoves), remove those that are such that the king is in check

        TODO: to better implemented!
                the moves are not correct. Should use the self.board.move function.
        """
        moves = self.baseMoves().copy()
        initPiece = copy.copy(self)
        moveFrom = initPiece.coord
        for m in self.baseMoves().copy():
            endPiece = copy.copy(self.board.array[m[0], m[1]])
            # self.board.move(moveFrom, m)
            self.board.array[m[0], m[1]] = copy.copy(self)
            self.board.array[m[0], m[1]].coord = m
            self.board.array[moveFrom[0], moveFrom[1]] = None

            kingCoord = self.board.findKing(initPiece.colour)
            check = self.board.isCheck(kingCoord, initPiece.colour)

            self.board.array[moveFrom[0], moveFrom[1]] = initPiece
            self.board.array[m[0], m[1]] = endPiece
            if isinstance(endPiece, Piece):
                self.board.array[m[0], m[1]].coord = m

            if check is True:
                moves.remove(m)

        if isinstance(self, King):
            castlingMoves = self.castleMoves()
            moves.append(castlingMoves)
            moves = [x for x in moves if x]
        return moves


class Pawn(Piece):
    def __init__(self, coord, colour, board):
        Piece.__init__(self, coord, colour, board)
        # Graphics
        self.displayImage = PhotoImage(file=board.UI.pathImages+colour+'Pawn.png')
        self.resize()
        X, Y = board.UI.coordToPixel(self.coord[0], self.coord[1])
        self.Image = board.UI.canvas.create_image((X, Y), image=self.displayImage)

    def baseMoves(self):
    #def allMoves(self):
        """
        TODO: Need to include en passant moves but for that need to save previous moves
        """
        allMoves = []
        array = self.board.array
        boardSize = self.board.boardSize-1
        x = self.coord[0]
        y = self.coord[1]
        if self.colour == 'white':
            if array[x, y+1] is None:
                allMoves.append([x, y+1])
            if y == 1 and array[x, y+2] is None:
                allMoves.append([x, y+2])
            # Captures
            if (x >= 1 and
                    isinstance(array[x-1, y+1], Piece) and array[x-1, y+1].colour == 'black'):
                allMoves.append([x-1, y+1])
            if (x <= boardSize-1 and
                    isinstance(array[x+1, y+1], Piece) and array[x+1, y+1].colour == 'black'):
                allMoves.append([x+1, y+1])
            # En Passant
            if [x+1, y+1] in self.board.enPassant:
                allMoves.append([x+1, y+1])
            if [x-1, y+1] in self.board.enPassant:
                allMoves.append([x-1, y+1])
        elif self.colour == 'black':
            if array[x, y-1] is None:
                allMoves.append([x, y-1])
            if y == boardSize-1 and array[x, y-2] is None:
                allMoves.append([x, y-2])
            if (x >= 1 and
                    isinstance(array[x-1, y-1], Piece) and array[x-1, y-1].colour == 'white'):
                allMoves.append([x-1, y-1])
            if (x <= boardSize-1 and
                    isinstance(array[x+1, y-1], Piece) and array[x+1, y-1].colour == 'white'):
                allMoves.append([x+1, y-1])
            # En Passant
            if [x+1, y-1] in self.board.enPassant:
                allMoves.append([x+1, y-1])
            if [x-1, y-1] in self.board.enPassant:
                allMoves.append([x-1, y-1])
        return allMoves


class Rook(Piece):
    def __init__(self, coord, colour, board):
        Piece.__init__(self, coord, colour, board)
        # Graphics
        self.displayImage = PhotoImage(file=board.UI.pathImages+colour+'Rook.png')
        self.resize()
        X, Y = board.UI.coordToPixel(self.coord[0], self.coord[1])
        self.Image = board.UI.canvas.create_image((X, Y), image=self.displayImage)

    def baseMoves(self):
    #def allMoves(self):
        allMoves = []
        array = self.board.array
        boardSize = self.board.boardSize
        x = self.coord[0]
        y = self.coord[1]
        # Moves along the ranks
        for i in range(x+1, boardSize):
            if array[i, y] is None:
                allMoves.append([i, y])
            elif array[i, y].colour == self.otherColour:
                allMoves.append([i, y])
                break
            else:
                break
        for i in range(x-1, -1, -1):
            if array[i, y] is None:
                allMoves.append([i, y])
            elif array[i, y].colour == self.otherColour:
                allMoves.append([i, y])
                break
            else:
                break
        # Moves along the files
        for i in range(y+1, boardSize):
            if array[x, i] is None:
                allMoves.append([x, i])
            elif array[x, i].colour == self.otherColour:
                allMoves.append([x, i])
                break
            else:
                break
        for i in range(y-1, -1, -1):
            if array[x, i] is None:
                allMoves.append([x, i])
            elif array[x, i].colour == self.otherColour:
                allMoves.append([x, i])
                break
            else:
                break
        return allMoves


class Knight(Piece):
    def __init__(self, coord, colour, board):
        Piece.__init__(self, coord, colour, board)
        # Graphics
        self.displayImage = PhotoImage(file=board.UI.pathImages+colour+'Knight.png')
        self.resize()
        X, Y = board.UI.coordToPixel(self.coord[0], self.coord[1])
        self.Image = board.UI.canvas.create_image((X, Y), image=self.displayImage)

    def baseMoves(self):
    #def allMoves(self):
        allMoves = []
        array = self.board.array
        x = self.coord[0]
        y = self.coord[1]
        boardSize = self.board.boardSize-1
        if (x+1 <= boardSize and y+2 <= boardSize and
                (array[x+1, y+2] is None or array[x+1, y+2].colour == self.otherColour)):
            allMoves.append([x+1, y+2])
        if (x-1 >= 0 and y+2 <= boardSize and
                (array[x-1, y+2] is None or array[x-1, y+2].colour == self.otherColour)):
            allMoves.append([x-1, y+2])
        if (x+1 <= boardSize and y-2 >= 0 and
                (array[x+1, y-2] is None or array[x+1, y-2].colour == self.otherColour)):
            allMoves.append([x+1, y-2])
        if (x-1 >= 0 and y-2 >= 0 and
                (array[x-1, y-2] is None or array[x-1, y-2].colour == self.otherColour)):
            allMoves.append([x-1, y-2])
        if (x+2 <= boardSize and y+1 <= boardSize and
                (array[x+2, y+1] is None or array[x+2, y+1].colour == self.otherColour)):
            allMoves.append([x+2, y+1])
        if (x+2 <= boardSize and y-1 >= 0 and
                (array[x+2, y-1] is None or array[x+2, y-1].colour == self.otherColour)):
            allMoves.append([x+2, y-1])
        if (x-2 >= 0 and y+1 <= boardSize and
                (array[x-2, y+1] is None or array[x-2, y+1].colour == self.otherColour)):
            allMoves.append([x-2, y+1])
        if (x-2 >= 0 and y-1 >= 0 and
                (array[x-2, y-1] is None or array[x-2, y-1].colour == self.otherColour)):
            allMoves.append([x-2, y-1])
        return allMoves


class Bishop(Piece):
    def __init__(self, coord, colour, board):
        Piece.__init__(self, coord, colour, board)
        # Graphics
        self.displayImage = PhotoImage(file=board.UI.pathImages+colour+'Bishop.png')
        self.resize()
        X, Y = board.UI.coordToPixel(self.coord[0], self.coord[1])
        self.Image = board.UI.canvas.create_image((X, Y), image=self.displayImage)

    def baseMoves(self):
    #def allMoves(self):
        allMoves = []
        array = self.board.array
        boardSize = self.board.boardSize-1
        x = self.coord[0]
        y = self.coord[1]
        # Up right
        for i in range(1, min(boardSize-x, boardSize-y)+1):
            if array[x+i, y+i] is None:
                allMoves.append([x+i, y+i])
            elif array[x+i, y+i].colour == self.otherColour:
                allMoves.append([x+i, y+i])
                break
            else:
                break
        # Up left
        for i in range(1, min(x, boardSize-y)+1):
            if array[x-i, y+i] is None:
                allMoves.append([x-i, y+i])
            elif array[x-i, y+i].colour == self.otherColour:
                allMoves.append([x-i, y+i])
                break
            else:
                break
        # Bottom right
        for i in range(1, min(y, boardSize-x)+1):
            if array[x+i, y-i] is None:
                allMoves.append([x+i, y-i])
            elif array[x+i, y-i].colour == self.otherColour:
                allMoves.append([x+i, y-i])
                break
            else:
                break
        # Bottom left
        for i in range(1, min(x, y)+1):
            if array[x-i, y-i] is None:
                allMoves.append([x-i, y-i])
            elif array[x-i, y-i].colour == self.otherColour:
                allMoves.append([x-i, y-i])
                break
            else:
                break
        return allMoves


class King(Piece):
    def __init__(self, coord, colour, board):
        Piece.__init__(self, coord, colour, board)
        # Graphics
        self.displayImage = PhotoImage(file=board.UI.pathImages+colour+'King.png')
        self.resize()
        X, Y = board.UI.coordToPixel(self.coord[0], self.coord[1])
        self.Image = board.UI.canvas.create_image((X, Y), image=self.displayImage)

    def baseMoves(self):
    #def allMoves(self):
        # TODO: Castling
        allMoves = []
        array = self.board.array
        boardSize = self.board.boardSize-1
        x = self.coord[0]
        y = self.coord[1]

        # Normal moves
        if x+1 <= boardSize and (array[x+1, y] is None or array[x+1, y].colour == self.otherColour):
            allMoves.append([x+1, y])
        if x-1 >= 0 and (array[x-1, y] is None or array[x-1, y].colour == self.otherColour):
            allMoves.append([x-1, y])
        if y+1 <= boardSize and (array[x, y+1] is None or array[x, y+1].colour == self.otherColour):
            allMoves.append([x, y+1])
        if y-1 >= 0 and (array[x, y-1] is None or array[x, y-1].colour == self.otherColour):
            allMoves.append([x, y-1])
        if (x+1 <= boardSize and y+1 <= boardSize and
                (array[x+1, y+1] is None or array[x+1, y+1].colour == self.otherColour)):
            allMoves.append([x+1, y+1])
        if (x+1 <= boardSize and y-1 >= 0 and
                (array[x+1, y-1] is None or array[x+1, y-1].colour == self.otherColour)):
            allMoves.append([x+1, y-1])
        if (x-1 >= 0 and y+1 <= boardSize and
                (array[x-1, y+1] is None or array[x-1, y+1].colour == self.otherColour)):
            allMoves.append([x-1, y+1])
        if (x-1 >= 0 and y-1 >= 0 and
                (array[x-1, y-1] is None or array[x-1, y-1].colour == self.otherColour)):
            allMoves.append([x-1, y-1])
        return allMoves

    def castleMoves(self):
        """
            All moves are the base moves + castling.
        """
        moves = []
        array = self.board.array
        boardSize = self.board.boardSize-1
        x = self.coord[0]
        y = self.coord[1]
        if not self.hasMoved:
            # King Side
            castle = True
            if not isinstance(array[boardSize, y], Rook) or (isinstance(array[boardSize, y], Rook) and
                                                             array[boardSize, y].hasMoved):
                castle = False
            for i in range(x + 1, x + 3):
                if array[i, y] is not None or self.board.isCheck([i, y], self.colour):
                    castle = False
            if castle:
                moves.extend([x + 2, y])
            # Queen Side
            castle = True
            if not isinstance(array[0, y], Rook) or (isinstance(array[0, y], Rook) and
                                                     array[0, y].hasMoved):
                castle = False
            for i in range(x - 1, x - 4, -1):
                if array[i, y] is not None or self.board.isCheck([i, y], self.colour):
                    castle = False
            if castle:
                moves.extend([x - 2, y])
        return moves

class Queen(Piece):
    def __init__(self, coord, colour, board):
        Piece.__init__(self, coord, colour, board)
        # Graphics
        self.displayImage = PhotoImage(file=board.UI.pathImages+colour+'Queen.png')
        self.resize()
        X, Y = board.UI.coordToPixel(self.coord[0], self.coord[1])
        self.Image = board.UI.canvas.create_image((X, Y), image=self.displayImage)

    def baseMoves(self):
    #def allMoves(self):
        moveRook = Rook(self.coord, self.colour, self.board).baseMoves()
        moveBishop = Bishop(self.coord, self.colour, self.board).baseMoves()
        moveRook.extend(moveBishop)
        return moveRook
