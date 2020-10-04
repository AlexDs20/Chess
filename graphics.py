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
        self.pathImages = '/home/alexandre/Documents/Chess/images/'

        self.Images = np.empty([self.boardSize, self.boardSize], dtype=object)
        self.Pieces = np.empty([self.boardSize, self.boardSize], dtype=object)

        self.click = []
        self.realeased = []
        self.selectedPiece = []
        # -----------

        # Interface
        self.root = Tk()
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack(padx=self.padx, pady=self.pady)

        # Setup board
        self.createCheckerboard()
        self.board = Board(self)
        # self.createPieces()

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

    def createPieces(self):
        image = PhotoImage(file=r'/home/alexandre/Documents/Chess/images/pawn.png')
        for i in range(8):
            self.Images[i, 6] = image.subsample(int(800/(0.9*self.squareSize)))
            X, Y = self.coordToPixel(i, 6)
            self.Pieces[i, 6] = self.canvas.create_image((X, Y), image=self.Images[i, 6])

    def coordToPixel(self, x, y):
        # Returns center of square at coord [x, y] in Pixels
        xPix = (x+0.5)*self.squareSize
        yPix = (7-y+0.5)*self.squareSize
        return xPix, yPix

    def pixelToCoord(self, x, y):
        xCoord = int(np.floor(x/self.squareSize))
        yCoord = int(abs(7-np.floor(y/self.squareSize)))
        return xCoord, yCoord

    def clicked(self, event):
        self.click = self.pixelToCoord(event.x, event.y)
        self.selectedPiece = self.board.array[self.click[0], self.click[1]]

    def drag(self, event):
        x = self.click[0]
        y = self.click[1]
        xMid, yMid = self.canvas.coords(self.selectedPiece.Image)
        self.canvas.move(self.selectedPiece.Image, event.x-xMid, event.y-yMid)

    def released(self, event):
        self.released = self.pixelToCoord(event.x, event.y)
        self.board.array[self.released[0], self.released[1]] = self.board.array[self.click[0], self.click[1]]
        self.board.array[self.click[0], self.click[1]] = None
        xs = -(event.x % self.squareSize) + self.squareSize/2
        ys = -(event.y % self.squareSize) + self.squareSize/2
        self.canvas.move(self.selectedPiece.Image, xs, ys)


GraphicsInterface()
