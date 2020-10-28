# Chess
A chess game in python

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
- [x] Black and white must play alternatively
- [x] minimax bot with alpha-beta pruning
- [x] Randomize the order of the moves that are passed to minimax bot
- [x] Better implement the playing interface (graphics.py)! Some things
  can/should still be improved but that can wait
- [x] Implement castling using the FEN notations instead, now I get a bug when
  undoing a move as the king and rooks are considered to note have moved yet

What must be done:
- [ ] minimax does not return the good moves... (for black at least)
- [ ] Stalemate
- [ ] 3x repeated configuration = draw
- [ ] 50 moves rule
- [ ] Implement deep learning bot

What could be done:
- [ ] minimax bot: multiprocessing (non-trivial as minimax is sequential...)
- [ ] Make the graphics scaling with the window
