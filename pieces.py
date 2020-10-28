import copy
import numpy as np


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

    def positionValue(self):
        if self.colour == 'white':
            map = self.valueMap
        else:
            # Flip the values on the board if black
            map = [file[::-1] for file in self.valueMap]
        squareValue = map[self.coord[0]][self.coord[1]]
        return self.value + squareValue

    def printMap(self):
        if self.colour == 'white':
            map = self.valueMap
        else:
            map = [file[::-1] for file in self.valueMap]
        b = np.zeros([self.board.boardSize, self.board.boardSize], dtype=float)
        for i in range(self.board.boardSize):
            for j in range(self.board.boardSize):
                b[i, j] = map[i][j]
        print(b)

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
    valueMap = [[0.0, 0.5, 0.5, 0.0, 0.5, 1.0, 5.0, 0.0],
                [0.0, 1.0, -0.5, 0.0, 0.5, 1.0, 5.0, 0.0],
                [0.0, 1.0, -1.0, 0.0, 1.0, 2.0, 5.0, 0.0],
                [0.0, -2.0, 0.0, 2.0, 2.5, 3.0, 5.0, 0.0],
                [0.0, -2.0, 0.0, 2.0, 2.5, 3.0, 5.0, 0.0],
                [0.0, 1.0, -1.0, 0.0, 1.0, 2.0, 5.0, 0.0],
                [0.0, 1.0, -0.5, 0.0, 0.5, 1.0, 5.0, 0.0],
                [0.0, 0.5, 0.5, 0.0, 0.5, 1.0, 5.0, 0.0]]
    value = 10

    def baseMoves(self):
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
            if y == 1 and all(pos is None for pos in array[x, y+1: y+3]):
                allMoves.append([x, y+2])
            # Captures
            if (x >= 1 and
                    isinstance(array[x-1, y+1], Piece) and array[x-1, y+1].colour == 'black'):
                allMoves.append([x-1, y+1])
            if (x <= boardSize-1 and
                    isinstance(array[x+1, y+1], Piece) and array[x+1, y+1].colour == 'black'):
                allMoves.append([x+1, y+1])
            # En Passant
            if [x+1, y+1] in [self.board.enPassant]:
                allMoves.append([x+1, y+1])
            if [x-1, y+1] in [self.board.enPassant]:
                allMoves.append([x-1, y+1])
        elif self.colour == 'black':
            if array[x, y-1] is None:
                allMoves.append([x, y-1])
            if y == boardSize-1 and all(pos is None for pos in array[x, y-1: y-3: -1]):
                allMoves.append([x, y-2])
            if (x >= 1 and
                    isinstance(array[x-1, y-1], Piece) and array[x-1, y-1].colour == 'white'):
                allMoves.append([x-1, y-1])
            if (x <= boardSize-1 and
                    isinstance(array[x+1, y-1], Piece) and array[x+1, y-1].colour == 'white'):
                allMoves.append([x+1, y-1])
            # En Passant
            if [x+1, y-1] in [self.board.enPassant]:
                allMoves.append([x+1, y-1])
            if [x-1, y-1] in [self.board.enPassant]:
                allMoves.append([x-1, y-1])
        return allMoves


class Rook(Piece):
    valueMap = [[0.0, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                [0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                [0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                [0.0, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5, 0.0]]
    value = 50

    def baseMoves(self):
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
    valueMap = [[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
                [-4.0, -2.0, 0.5, 0.0, 0.5, 0.0, -2.0, -4.0],
                [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
                [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
                [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
                [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
                [-4.0, -2.0, 0.5, 0.0, 0.5, 0.0, -2.0, -4.0],
                [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]]

    value = 30

    def baseMoves(self):
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
    valueMap = [[-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
                [-1.0, 0.5, 1.0, 0.0, 0.5, 0.0, 0.0, -1.0],
                [-1.0, 0.0, 1.0, 1.0, 0.5, 0.5, 0.0, -1.0],
                [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
                [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
                [-1.0, 0.0, 1.0, 1.0, 0.5, 0.5, 0.0, -1.0],
                [-1.0, 0.5, 1.0, 0.0, 0.5, 0.0, 0.0, -1.0],
                [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]]
    value = 35

    def baseMoves(self):
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
    """
    King class
    It is given a value superior to all other pieces combined of the same colour
    """
    valueMap = [[2.0, 2.0, -1.0, -2.0, -3.0, -3.0, -3.0, -3.0],
                [3.0, 2.0, -2.0, -3.0, -4.0, -4.0, -4.0, -4.0],
                [1.0, 0.0, -2.0, -3.0, -4.0, -4.0, -4.0, -4.0],
                [0.0, 0.0, -2.0, -4.0, -5.0, -5.0, -5.0, -5.0],
                [0.0, 0.0, -2.0, -4.0, -5.0, -5.0, -5.0, -5.0],
                [1.0, 0.0, -2.0, -3.0, -4.0, -4.0, -4.0, -4.0],
                [3.0, 2.0, -2.0, -3.0, -4.0, -4.0, -4.0, -4.0],
                [2.0, 2.0, -1.0, -2.0, -3.0, -3.0, -3.0, -3.0]]

    value = 900

    def baseMoves(self):
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
            For castling, check if it is allowed and if none of the squares are in check
        """
        moves = []
        array = self.board.array
        x = self.coord[0]
        y = self.coord[1]
        if self.colour == 'white':
            sides = [char.lower() for char in self.board.castling if char.isupper()]
        else:
            sides = [char for char in self.board.castling if char.islower()]

        if 'k' in sides:
            # Castle king side: check if squares empty and not in check!
            castle = True
            for i in range(x + 1, x + 3):
                if array[i, y] is not None or self.board.isCheck([i, y], self.colour):
                    castle = False
                    break
            if castle:
                moves.extend([x + 2, y])

        if 'q' in sides:
            # Castle queen side
            castle = True
            for i in range(x - 1, x - 4, -1):
                if array[i, y] is not None or self.board.isCheck([i, y], self.colour):
                    castle = False
                    break
            if castle:
                moves.extend([x - 2, y])
        return moves


class Queen(Piece):
    valueMap = [[-2.0, -1.0, -1.0, 0.0, -0.5, -1.0, -1.0, -2.0],
                [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
                [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
                [-2.0, -1.0, -1.0, 0.0, -0.5, -1.0, -1.0, -2.0]]

    value = 90

    def baseMoves(self):
        moveRook = Rook(self.coord, self.colour, self.board).baseMoves()
        moveBishop = Bishop(self.coord, self.colour, self.board).baseMoves()
        moveRook.extend(moveBishop)
        return moveRook
