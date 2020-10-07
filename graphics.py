#!/bin/python3
import numpy as np
from tkinter import *
from chessRules import *


class GraphicsInterface():
    def __init__(self):
        # -----------
        # Variables
        self.padx = 50
        self.pady = 50
        self.height = 800
        self.width = 800
        self.bgColor = '#F7F7F7'
        self.boardSize = 8
        self.squareSize = 64
        self.shiftX = 64
        self.shiftY = 64
        self.color1 = '#E3C3A5'
        self.color2 = '#794532'
        self.pathImages = './images/'

        self.Images = np.empty([self.boardSize, self.boardSize], dtype=object)
        self.Pieces = np.empty([self.boardSize, self.boardSize], dtype=object)

        self.click = np.empty(2, dtype=int)
        self.realeased = np.empty(2, dtype=int)
        self.selectedPiece = []
        self.possibleMovesWidget = []
        self.possibleMovesImg = []
        # -----------

        # Interface
        self.root = Tk()
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack(padx=self.padx, pady=self.pady)

        # Setup board
        self.createCheckerboard()
        self.board = Board(self)

        # Click actions
        self.canvas.bind("<Button-1>", self.clicked)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.released)

        # Main loop
        self.root.mainloop()

    def createCheckerboard(self):
        for i in range(0, self.boardSize):
            for j in range(0, self.boardSize):
                if (i+j) % 2 == 0:
                    color = self.color1
                else:
                    color = self.color2
                self.canvas.create_rectangle(i*self.squareSize, j*self.squareSize,
                                             (i+1)*self.squareSize, (j+1)*self.squareSize,
                                             fill=color)

    def showPossibleMoves(self):
        for coord in self.board.array[self.click[0], self.click[1]].possibleMoves():
            imgWidget = PhotoImage(file=self.pathImages+'possibleMove.png')
            self.possibleMovesWidget.append(imgWidget)
            X, Y = self.coordToPixel(coord[0], coord[1])
            img = self.canvas.create_image((X, Y), image=imgWidget)
            self.possibleMovesImg.append(img)

    def coordToPixel(self, x, y):
        # Returns center of square at coord [x, y] in Pixels
        xPix = (x+0.5)*self.squareSize
        yPix = (self.boardSize-1-y+0.5)*self.squareSize
        return xPix, yPix

    def pixelToCoord(self, x, y):
        x = int(np.floor(x/self.squareSize))
        y = int(self.boardSize-1-np.floor(y/self.squareSize))
        if x<0 or x>=self.boardSize or y<0 or y>=self.boardSize:
            x = []
            y = []
        return x, y

    def clicked(self, event):
        self.click = self.pixelToCoord(event.x, event.y)
        if self.click:
            self.selectedPiece = self.board.array[self.click[0], self.click[1]]
            if isinstance(self.selectedPiece, Piece):
                print(self.selectedPiece.__class__.__name__+' at: '+str(self.selectedPiece.coord))
                self.showPossibleMoves()

    def drag(self, event):
        if isinstance(self.selectedPiece, Piece):
            x = self.click[0]
            y = self.click[1]
            xMid, yMid = self.canvas.coords(self.selectedPiece.Image)
            self.canvas.move(self.selectedPiece.Image, event.x-xMid, event.y-yMid)

    def released(self, event):
        if isinstance(self.selectedPiece, Piece):
            self.released = self.pixelToCoord(event.x, event.y)
            if self.released:
                if [self.released[0], self.released[1]] in self.selectedPiece.possibleMoves():
                    self.board.move([self.click[0], self.click[1]], [
                                    self.released[0], self.released[1]])
                    xBoard, yBoard = self.coordToPixel(self.released[0], self.released[1])
                    if self.board.checkMate(self.selectedPiece.otherColour):
                        print("Checkmate, " + self.selectedPiece.otherColour + "  looses!")
                else:
                    xBoard, yBoard = self.coordToPixel(self.click[0], self.click[1])
                self.canvas.coords(self.selectedPiece.Image, [xBoard, yBoard])
            self.possibleMovesWidget = []
            self.possibleMovesImg = []
        self.selectedPiece = []
        self.click = np.empty(2, dtype=int)
        self.released = np.empty(2, dtype=int)


GraphicsInterface()
