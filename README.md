# Chess
A chess game in python

![Graphical interface of the game. White is a human and black is a bot using minimax.](https://github.com/AlexDs20/Chess/tree/dev/gif/Chess-human-vs-bot.gif)

# How to play you ask?
**1. Clone the project:**
```
git clone https://github.com/AlexDs20/Chess
```
**2. Start the game:**

There are two possibilities.
Either you make it executable and run it:
```
chmod +x main.py
./main.py
```
or you can run it with python3 directly:
```
python3 main.py
```


## Variables:
Some properties can be set in the graphics.py (not optimal, I know).
Those are:

Variables   |  Values             | Effect
------------|---------------------|----------
playerWhite | 'human', 'minimax'  |  Defines whether white is a human or a bot
playerBlack | 'human', 'minimax'  |  Defines whether white is a human or a bot
minimaxDepth| integer: 1, 2, 3, ... | Depth at which a minimax player would investigate (how many moves in advances it looks)
minimaxPara | True or False       |  Whether to use a parallel implementation of minimax of not


## In Development
What is done:
- [x] Basic motion of the pieces
- [x] Graphical interface
- [x] Link graphics to game rules
- [x] Pawn Promotion
- [x] Checks
- [x] Checkmate
- [x] Show possible moves on screen
- [x] Make svg files for each of the pieces
- [x] En passant
- [x] Castle
- [x] Black and white play alternatively
- [x] minimax bot with alpha-beta pruning
- [x] Randomize order moves used by minimax bot
- [x] Castling using the FEN notations
- [x] minimax multiprocess at root
- [x] Stalemate
- [x] 50 moves rule

What must be done:
- [ ] 3x repeated configuration = draw
- [ ] Implement deep learning bot

What could be done:
- [ ] minimax bot: multiprocessing (non-trivial as minimax is sequential...)
- [ ] Make the graphics scaling with the window
