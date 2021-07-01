# Tic-Tac-Toe
My goal was to create Tic-Tac-Toe Game and make AI as opponent of the user, which calculates all the possible moves and choose the best of them. 
I reached my goal, after playing too much game, I convinced that AI is mathematically impossible to defeat.

# Description
Tic-tac-toe is a very simple game.

At first you have empty 3x3 board, where you have to place X or O, depends of which player are you. the X one, allways starts first and then O turn to play.
Players placing X or O, untill game ends.

If one of the players, fills horizontal, vertical or diagonal lines with their symbol, player wins.
If players fill up entire board, without winning, that's draw.

For more information: https://en.wikipedia.org/wiki/Tic-tac-toe

# Getting started
If you want to run my game at your device for some reasons, you just need to clone my project and run main.py.
 
# Using
At first, you have to choose your symbol, you select the symbol with one click and choose it after click again.

After choosing your symbol, you will see game board, X starts first, if you choose O, you have to wait before AI makes a move.
If you choose X, you have to start the game and AI makes move then.

You make move by clicking empty spot at the board.

# How AI works
I am using Minimax algorithm, which is the best in 2v2 games.

This algorithm calculates all the possible moves and sorts them from the worst to the best, when choose the best one, but it's making that dynamically,
so we do not need to save possible moves.

I am using this algorithm with pruning, which means that, i am baning already bad branch of the tree depends of other branches, before go to the end of the branch, 
which gives calculation more time and makes AI faster.

For more information: https://en.wikipedia.org/wiki/Minimax

# Credits
@inc. all by myself
