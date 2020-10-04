#!/bin/python3

import numpy as np
from tkinter import *


class Board:
    array = []
    boardSize = []
    info = []

    def __init__(self, boardSize):
        self.boardSize = boardSize
        self.initBoard()
        self.info = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}

    def initBoard(self):
        self.array = np.empty([self.boardSize, self.boardSize], dtype=object)
        for i in range(self.boardSize):
            self.array[i, 1] = Pawn([i, 1], "white", self)
            self.array[i, 6] = Pawn([i, 6], "black", self)
        self.array[0, 0] = Rook([0, 0], "white", self)
        self.array[7, 0] = Rook([7, 0], "white", self)
        self.array[1, 0] = Knight([1, 0], "white", self)
        self.array[6, 0] = Knight([6, 0], "white", self)
        self.array[2, 0] = Bishop([2, 0], "white", self)
        self.array[5, 0] = Bishop([5, 0], "white", self)
        self.array[3, 0] = King([3, 0], "white", self)
        self.array[4, 0] = Queen([4, 0], "white", self)
        self.array[0, 7] = Rook([0, 7], "black", self)
        self.array[7, 7] = Rook([7, 7], "black", self)
        self.array[1, 7] = Knight([1, 7], "black", self)
        self.array[6, 7] = Knight([6, 7], "black", self)
        self.array[2, 7] = Bishop([2, 7], "black", self)
        self.array[5, 7] = Bishop([5, 7], "black", self)
        self.array[3, 7] = Queen([3, 7], "black", self)
        self.array[4, 7] = King([4, 7], "black", self)

    def move(self, moveFrom, moveTo):
        if moveTo in self.array[moveFrom[0], moveFrom[1]].possibleMoves():
            self.array[moveTo[0], moveTo[1]] = self.array[moveFrom[0], moveFrom[1]]
            self.array[moveFrom[0], moveFrom[1]] = None

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
    coord = []
    colour = []
    otherColour = []
    board = []

    def __init__(self, coord, colour, board):
        self.colour = colour
        if self.colour == "black":
            self.otherColour = "white"
        elif self.colour == "white":
            self.otherColour == "black"

        self.coord = coord
        self.board = board


class Pawn(Piece):
    def __init__(self, coord, colour, board):
        Piece.__init__(self, coord, colour, board)

    def possibleMoves(self):
        possibleMoves = []
        array = self.board.array
        x = self.coord[0]
        y = self.coord[1]
        if self.colour == "white":
            if array[x, y+1] is None:
                possibleMoves.append([x, y+1])
            if y == 1 and array[x, y+2] is None:
                possibleMoves.append([x, y+2])
            if x >= 1 and isinstance(array[x-1, y+1], Piece)\
                    and array[x-1, y+1].colour == "black":
                possibleMoves.append([x-1, y+1])
            if x <= 6 and isinstance(array[x+1, y+1], Piece)\
                    and array[x+1, y+1].colour == "black":
                possibleMoves.append([x+1, y+1])
        elif self.colour == "black":
            if array[x, y-1] is None:
                possibleMoves.append([x, y-1])
            if y == 6 and array[x, y-2] is None:
                possibleMoves.append([x, y-2])
            if x >= 1 and isinstance(array[x-1, y-1], Piece)\
                    and array[x-1, y-1].colour == "white":
                possibleMoves.append([x-1, y-1])
            if x <= 6 and isinstance(array[x+1, y-1], Piece)\
                    and array[x+1, y-1].colour == "white":
                possibleMoves.append([x+1, y-1])
        return possibleMoves


class Rook(Piece):
    def possibleMoves(self):
        possibleMoves = []
        array = self.board.array
        x = self.coord[0]
        y = self.coord[1]
        # Moves along the ranks
        for i in range(x+1, self.board.boardSize):
            if array[i, y] is None:
                possibleMoves.append([i, y])
            elif array[i, y].colour == self.otherColour:
                possibleMoves.append([i, y])
                break
            else:
                break
        for i in range(x-1, -1, -1):
            if array[i, y] is None:
                possibleMoves.append([i, y])
            elif array[i, y].colour == self.otherColour:
                possibleMoves.append([i, y])
                break
            else:
                break
        # Moves along the files
        for i in range(y+1, self.board.boardSize):
            if array[x, i] is None:
                possibleMoves.append([x, i])
            elif array[x, i].colour == self.otherColour:
                possibleMoves.append([x, i])
                break
            else:
                break
        for i in range(y-1, -1, -1):
            if array[x, i] is None:
                possibleMoves.append([x, i])
            elif array[x, i].colour == self.otherColour:
                possibleMoves.append([x, i])
                break
            else:
                break
        return possibleMoves


class Knight(Piece):
    def possibleMoves(self):
        possibleMoves = []
        array = self.board.array
        x = self.coord[0]
        y = self.coord[1]
        if x+1 <= 7 and y+2 <= 7 and board[x+1, y+2] == 0:
            possibleMoves.append([x+1, y+2])
        if x-1 >= 0 and y+2 <= 7 and board[x-1, y+2] == 0:
            possibleMoves.append([x-1, y+2])
        if x+1 <= 7 and y-2 >= 0 and board[x+1, y-2] == 0:
            possibleMoves.append([x+1, y-2])
        if x-1 >= 0 and y-2 >= 0 and board[x-1, y-2] == 0:
            possibleMoves.append([x-1, y-2])
        if x+2 <= 7 and y+1 <= 7 and board[x+2, y+1] == 0:
            possibleMoves.append([x+2, y+1])
        if x+2 <= 7 and y-1 >= 0 and board[x+2, y-1] == 0:
            possibleMoves.append([x+2, y-1])
        if x-2 >= 0 and y+1 <= 7 and board[x-2, y+1] == 0:
            possibleMoves.append([x-2, y+1])
        if x-2 >= 0 and y-1 >= 0 and board[x-2, y-1] == 0:
            possibleMoves.append([x-2, y-1])
        return possibleMoves


class Bishop(Piece):
    def possibleMoves(self):
        possibleMoves = []
        array = self.board.array
        x = self.coord[0]
        y = self.coord[1]
        # Up right
        for i in range(1, min(7-x, 7-y)+1):
            if array[x+i, y+i] is None:
                possibleMoves.append([x+i, y+i])
            elif array[x+i, y+i].colour == self.otherColour:
                possibleMoves.append([x+i, y+i])
                break
            else:
                break
        # Up left
        for i in range(1, min(x, 7-y)+1):
            if array[x-i, y+i] is None:
                possibleMoves.append([x-i, y+i])
            elif array[x-i, y+i].colour == self.otherColour:
                possibleMoves.append([x-i, y+i])
                break
            else:
                break
        # Bottom right
        for i in range(1, min(y, 7-x)+1):
            if array[x+i, y-i] is None:
                possibleMoves.append([x+i, y-i])
            elif array[x+i, y-i].colour == self.otherColour:
                possibleMoves.append([x+i, y-i])
                break
            else:
                break
        # Bottom left
        for i in range(1, min(x, y)+1):
            if array[x-i, y-i] is None:
                possibleMoves.append([x-i, y-i])
            elif array[x-i, y-i].colour == self.otherColour:
                possibleMoves.append([x-i, y-i])
                break
            else:
                break
        return possibleMoves


class King(Piece):
    inCheck = []

    def __init__(self, coord, colour, board):
        Piece.__init__(self, coord, colour, board)
        self.inCheck = False

    def possibleMoves(self):
        # TODO: Castling
        #       Check if new case is in check
        possibleMoves = []
        array = self.board.array
        x = self.coord[0]
        y = self.coord[1]
        if x+1 <= 7 and (board[x+1, y] == 0 or board[x+1, y].colour == self.otherColour):
            possibleMoves.append([x+1, y])
        if x-1 >= 0 and board[x-1, y] == 0 or board[x+1, y].colour == self.otherColour:
            possibleMoves.append([x-1, y])
        if y+1 <= 7 and board[x, y+1] == 0 or board[x+1, y].colour == self.otherColour:
            possibleMoves.append([x, y+1])
        if y-1 >= 0 and board[x, y-1] == 0 or board[x+1, y].colour == self.otherColour:
            possibleMoves.append([x, y-1])
        if x+1 <= 7 and y+1 <= 7 and (board[x+1, y+1] == 0 or board[x+1, y].colour == self.otherColour):
            possibleMoves.append([x+1, y+1])
        if x+1 <= 7 and y-1 >= 0 and (board[x+1, y-1] == 0 or board[x+1, y].colour == self.otherColour):
            possibleMoves.append([x+1, y-1])
        if x-1 >= 0 and y+1 <= 7 and (board[x-1, y+1] == 0 or board[x+1, y].colour == self.otherColour):
            possibleMoves.append([x-1, y+1])
        if x-1 >= 0 and y-1 <= 7 and (board[x-1, y-1] == 0 or board[x+1, y].colour == self.otherColour):
            possibleMoves.append([x-1, y-1])
        return possibleMoves


class Queen(Piece):
    def possibleMoves(self):
        moveRook = Rook(self.coord, self.colour, self.board).possibleMoves()
        moveBishop = Bishop(self.coord, self.colour, self.board).possibleMoves()
        for i in range(len(moveBishop)):
            moveRook.append(moveBishop[i])
        return moveRook


boardSize = 8
board = Board(boardSize)


x = 3
y = 5
board.array[x, y] = Pawn([x, y], "white", board)
pM = board.array[x, y].possibleMoves()
pM
pM[0]
board.move([x, y], pM[0])
board.print()
