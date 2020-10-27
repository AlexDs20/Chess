#!/bin/python3
import numpy as np
from tkinter import Tk, Canvas, PhotoImage

from time import time

from board import Board
from pieces import Piece
from bots.minmax import minimax


class GraphicsInterface():
    def __init__(self):
        """
        Variables
        """
        self.padx = 50
        self.pady = 50
        self.height = 900
        self.width = 900
        self.bgColor = '#F7F7F7'
        self.boardSize = 8
        self.squareSize = np.min([(self.width - 2 * self.padx) // self.boardSize,
                                  (self.height - 2 * self.pady) // self.boardSize])
        self.color1 = '#E3C3A5'
        self.color2 = '#794532'
        self.pathImages = './images/'

        self.Images = np.empty([self.boardSize, self.boardSize], dtype=object)
        self.Pieces = np.empty([self.boardSize, self.boardSize], dtype=object)

        self.initFEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        # self.initFEN = 'rnbqkbnr/1ppppppp/8/p7/2B1P3/5Q2/PPPP1PPP/RNB1K1NR black KQkq - 0 1'

        self.click = np.empty(2, dtype=int)
        self.realeased = np.empty(2, dtype=int)
        self.selectedPiece = []
        self.possibleMovesWidget = []
        self.possibleMovesImg = []

        """
        Interface
        """
        self.root = Tk()
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack(padx=self.padx, pady=self.pady)

        """
        Setup board
        """
        self.board = Board(self.boardSize, self.initFEN)
        self.createCheckerboard()
        self.placePieces(self.initFEN)

        """
        Click actions
        """
        self.canvas.bind("<Button-1>", self.clicked)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.released)

        """
        Main loop
        """
        self.root.mainloop()

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
            if s.lower() == 'p':
                self.Images[i, j] = PhotoImage(file=self.pathImages+colour+'Pawn.png')
                self.Pieces[i, j] = self.canvas.create_image((x, y),
                                                             image=self.Images[i, j])
            elif s.lower() == 'r':
                self.Images[i, j] = PhotoImage(file=self.pathImages+colour+'Rook.png')
                self.Pieces[i, j] = self.canvas.create_image((x, y),
                                                             image=self.Images[i, j])
            elif s.lower() == 'n':
                self.Images[i, j] = PhotoImage(file=self.pathImages+colour+'Knight.png')
                self.Pieces[i, j] = self.canvas.create_image((x, y),
                                                             image=self.Images[i, j])
            elif s.lower() == 'b':
                self.Images[i, j] = PhotoImage(file=self.pathImages+colour+'Bishop.png')
                self.Pieces[i, j] = self.canvas.create_image((x, y),
                                                             image=self.Images[i, j])
            elif s.lower() == 'q':
                self.Images[i, j] = PhotoImage(file=self.pathImages+colour+'Queen.png')
                self.Pieces[i, j] = self.canvas.create_image((x, y),
                                                             image=self.Images[i, j])
            elif s.lower() == 'k':
                self.Images[i, j] = PhotoImage(file=self.pathImages+colour+'King.png')
                self.Pieces[i, j] = self.canvas.create_image((x, y),
                                                             image=self.Images[i, j])
            i += 1
            if s == '/':
                j -= 1
                i = 0
            if s == ' ':
                break

    def round_rectangle(self, x1, y1, x2, y2, r, **kwargs):
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

    def movePiecesGraphics(self, shift):
        """
        Snap the piece to the right square and set the graphical board in the right config
        In practice the first call is not needed but it makes the move smoother
        """
        self.canvas.coords(self.Pieces[self.click[0], self.click[1]], shift)
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

    def makeMove(self):
        if [self.released[0], self.released[1]] in self.selectedPiece.possibleMoves():
            self.board.move([self.click[0], self.click[1]], [
                            self.released[0], self.released[1]])
            xBoard, yBoard = self.coordToPixel(self.released[0], self.released[1])
        else:
            xBoard, yBoard = self.coordToPixel(self.click[0], self.click[1])
        self.movePiecesGraphics([xBoard, yBoard])

    def clicked(self, event):
        if self.board.player == 'black':
            start = time()
            evaluation, move = minimax(self.board, 3, False)
            end = time()
            print(end-start, evaluation, move)
            # Move on the board
            self.board.move(move[0], move[1])
            # Graphical moves
            x, y = self.coordToPixel(move[1][0], move[1][1])
            self.canvas.coords(self.Pieces[move[0][0], move[0][1]], [x, y])
            self.placePieces(self.board.getFEN())
        else:
            self.click = self.pixelToCoord(event.x, event.y)
            if self.click:
                self.selectedPiece = self.board.array[self.click[0], self.click[1]]
                if (isinstance(self.selectedPiece, Piece)) and self.selectedPiece.colour != self.board.player:
                    self.selectedPiece = []
                if isinstance(self.selectedPiece, Piece):
                    self.showPossibleMoves()

    def drag(self, event):
        if isinstance(self.selectedPiece, Piece):
            xMid, yMid = self.canvas.coords(self.Pieces[self.click[0], self.click[1]])
            self.canvas.move(self.Pieces[self.click[0], self.click[1]], event.x - xMid, event.y - yMid)

    def released(self, event):
        if isinstance(self.selectedPiece, Piece):
            self.released = self.pixelToCoord(event.x, event.y)
            if self.released:
                # makeMove on the board and graphically!
                self.makeMove()
                checkmate, stalemate = self.board.checkmate(self.selectedPiece.otherColour)
                if checkmate:
                    self.showCheckmate()
                elif stalemate:
                    pass
            self.possibleMovesWidget = []
            self.possibleMovesImg = []
        self.selectedPiece = []
        self.click = np.empty(2, dtype=int)
        self.released = np.empty(2, dtype=int)
