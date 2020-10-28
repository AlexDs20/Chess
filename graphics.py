#!/bin/python3
import numpy as np
from tkinter import Tk, Canvas, PhotoImage

from time import time

from board import Board
from pieces import Piece
from bots.minimax import minimax


class GraphicsInterface():
    def __init__(self):
        """
        Players: either: 'human', 'minimax'
        """
        self.playerWhite = 'human'
        self.playerBlack = 'minimax'
        self.minimaxDepth = 2

        """
        Window
        """
        self.padx = 50
        self.pady = 50
        self.height = 900
        self.width = 900
        self.bgColor = '#F7F7F7'

        """
        Board
        """
        self.boardSize = 8
        self.squareSize = np.min([(self.width - 2 * self.padx) // self.boardSize,
                                  (self.height - 2 * self.pady) // self.boardSize])
        self.color1 = '#E3C3A5'
        self.color2 = '#794532'
        self.pathImages = './images/'

        self.Images = np.empty([self.boardSize, self.boardSize], dtype=object)
        self.Pieces = np.empty([self.boardSize, self.boardSize], dtype=object)

        self.initFEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

        """
        Action
        """
        self.click = np.empty(2, dtype=int)
        self.release = np.empty(2, dtype=int)
        self.selectedPiece = []
        self.possibleMovesWidget = []
        self.possibleMovesImg = []

        """
        Interface
        """
        self.root = Tk()
        self.root.title('PyChess')
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack(padx=self.padx, pady=self.pady)

        """
        Setup board
        """
        self.board = Board(self.boardSize, self.initFEN)
        self.createCheckerboard()
        self.placePieces(self.initFEN)

        """
        PLAY
        """
        self.play()

    def play(self):
        checkmate = False
        while not checkmate:
            if ((self.board.player == 'white' and self.playerWhite == 'human') or
               (self.board.player == 'black' and self.playerBlack == 'human')):
                self.humanMove()

            if ((self.board.player == 'white' and self.playerWhite == 'minimax') or
               (self.board.player == 'black' and self.playerBlack == 'minimax')):
                self.minimaxMove()

            self.root.update_idletasks()
            self.root.update()

    def humanMove(self):
        self.canvas.bind("<Button-1>", self.clicked)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.released)

    def minimaxMove(self):
        maximize = {'black': 'False', 'white': 'True'}
        start = time()
        val, move = minimax(self.board, self.minimaxDepth, float('-inf'), float('inf'),
                            maximize[self.board.player])
        end = time()
        print(end-start, val, move)
        self.makeMove(move)

    def createCheckerboard(self):
        for i in range(0, self.boardSize):
            for j in range(0, self.boardSize):
                if (i + j) % 2 == 0:
                    color = self.color1
                else:
                    color = self.color2
                self.canvas.create_rectangle(self.padx + i * self.squareSize, self.pady + j * self.squareSize,
                                             self.padx + (i + 1) * self.squareSize, self.pady + (j + 1)
                                             * self.squareSize, fill=color)

    def placePieces(self, fen):
        """
        Places graphical pieces according to fen configuration
        """
        pieces = {'p': 'Pawn', 'r': 'Rook', 'n': 'Knight', 'b': 'Bishop', 'q': 'Queen', 'k': 'King'}
        i = 0
        j = self.boardSize-1
        for s in fen:
            if s.isnumeric():
                self.Images[i:i+int(s)+1, j] = None
                self.Pieces[i:i+int(s)+1, j] = None
                i += int(s)
                continue
            x, y = self.coordToPixel(i, j)
            if s.isupper():
                colour = 'white'
            else:
                colour = 'black'
            if s.isalpha():
                self.Images[i, j] = PhotoImage(file=self.pathImages+colour+pieces[s.lower()]+'.png')
                self.Pieces[i, j] = self.canvas.create_image((x, y),
                                                             image=self.Images[i, j])
            i += 1
            if s == '/':
                j -= 1
                i = 0
            if s == ' ':
                break

    def round_rectangle(self, x1, y1, x2, y2, r, **kwargs):
        """
        To display who wins
        """
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2,
                  y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r,
                  x1, y1+r, x1, y1+r, x1, y1)
        return self.canvas.create_polygon(points, **kwargs, smooth=True)

    def showCheckmate(self):
        rw = 4 * self.squareSize
        rh = 1.5 * self.squareSize
        bgColour = "#ACA7A6"
        w = (self.width // 2) - rw // 2
        h = (self.height // 2) - rh // 2

        self.round_rectangle(w, h, w + rw, h + rh, r=self.squareSize // 2, fill=bgColour)
        self.canvas.create_text(self.width // 2, self.height // 2,
                                text=f'{self.selectedPiece.colour} won!'.title(),
                                font=("Helvetica", 40))

    def showPossibleMoves(self):
        for coord in self.board.array[self.click[0], self.click[1]].possibleMoves():
            imgWidget = PhotoImage(file=self.pathImages + 'possibleMove.png')
            self.possibleMovesWidget.append(imgWidget)
            X, Y = self.coordToPixel(coord[0], coord[1])
            img = self.canvas.create_image((X, Y), image=imgWidget)
            self.possibleMovesImg.append(img)

    def movePiecesGraphics(self, shift, m):
        """
        Snap the piece to the right square and set the graphical board in the right config
        In practice the first call is not needed but it makes the move smoother
        """
        self.canvas.coords(self.Pieces[m[0][0], m[0][1]], shift)
        self.placePieces(self.board.getFEN())

    def coordToPixel(self, x, y):
        """
        Returns center of square at coord [x, y] in Pixels
        """
        xPix = self.padx + (x + 0.5) * self.squareSize
        yPix = self.pady + (self.boardSize - 1 - y + 0.5) * self.squareSize
        return xPix, yPix

    def pixelToCoord(self, x, y):
        x = int(np.floor((x - self.padx) / self.squareSize))
        y = int(self.boardSize - 1 - np.floor((y - self.pady) / self.squareSize))
        if x < 0 or x >= self.boardSize or y < 0 or y >= self.boardSize:
            x = []
            y = []
        return x, y

    def makeMove(self, m):
        """
        Make the move on the board and graphically
        """
        if list(m[1]) in self.board.array[m[0][0], m[0][1]].possibleMoves():
            self.board.move(list(m[0]), list(m[1]))
            xBoard, yBoard = self.coordToPixel(m[1][0], m[1][1])
        else:
            xBoard, yBoard = self.coordToPixel(m[0][0], m[0][1])
        self.movePiecesGraphics([xBoard, yBoard], m)
        checkmate, stalemate = self.board.checkmate(self.board.player)
        if checkmate:
            self.showCheckmate()
        elif stalemate:
            pass
        self.resetVariables()
        print(self.board.getFEN())

    def resetVariables(self):
        self.possibleMovesWidget = []
        self.possibleMovesImg = []
        self.selectedPiece = []
        self.click = np.empty(2, dtype=int)
        self.release = np.empty(2, dtype=int)

    def clicked(self, event):
        """
        When click on piece of the color that should play, display the possible moves
        """
        self.click = self.pixelToCoord(event.x, event.y)
        if self.click:
            self.selectedPiece = self.board.array[self.click[0], self.click[1]]
            if (isinstance(self.selectedPiece, Piece)) and self.selectedPiece.colour != self.board.player:
                self.selectedPiece = []
            if isinstance(self.selectedPiece, Piece):
                self.showPossibleMoves()

    def drag(self, event):
        """
        Make the selected piece follow the mouse
        """
        if isinstance(self.selectedPiece, Piece):
            xMid, yMid = self.canvas.coords(self.Pieces[self.click[0], self.click[1]])
            self.canvas.move(self.Pieces[self.click[0], self.click[1]], event.x - xMid, event.y - yMid)

    def released(self, event):
        """
        If allowed move, make move on the board and on the GUI
        + reset the variables
        """
        if isinstance(self.selectedPiece, Piece):
            self.release = self.pixelToCoord(event.x, event.y)
            if self.release:
                move = [self.click, self.release]
                self.makeMove(move)
