"""
Tic Tac Toe Player
"""

import copy
import math
import random

from numpy import Infinity

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    
    movesMade = 0
    for i in range(len(board)):
        for j in range (len(board[i])):
            if(board[i][j] != EMPTY):
                movesMade+=1

    return X if movesMade == 0 or movesMade%2 == 0  else O
    
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    openSpaces = set()
    currentOpenSpace = tuple()
    for i in range(len(board)):
        for j in range (len(board[i])):
            if(board[i][j] == EMPTY):
                currentOpenSpace = (i, j)
                openSpaces.add(currentOpenSpace)
    return openSpaces

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    boardState = actions(board)
    isValid = action in boardState
    if isValid:
        playerXorO = player(board)
        newBoard = copy.deepcopy(board)
        newBoard[action[0]][action[1]] = playerXorO
        return newBoard
    else:
        raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    checkEachPlayer = 0
    checkForPlayer = X
    trackH = 0
    trackV = 0
    winner = False
    while checkEachPlayer < 2 and not winner:
    #check horizontal & vertical: 
        for i in range(len(board)):
            if winner:
                break
            trackH = 0
            trackV = 0
            for j in range(len(board)):
                if(board[i][j] == checkForPlayer):
                    trackH += 1
                if(board[j][i] == checkForPlayer):
                    trackV += 1
                if trackH == 3 or trackV == 3:
                    winner = True
                    break

        # check diagnals
        if not winner:
            winner = board[0][0] == checkForPlayer and board[1][1] == checkForPlayer and board[2][2] == checkForPlayer
        if not winner:
            winner = board[0][2] == checkForPlayer and board[1][1] == checkForPlayer and board[2][0] == checkForPlayer

        if not winner:
            checkEachPlayer += 1
            checkForPlayer = O
    return checkForPlayer if winner else None

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    usedSpaces = 0
    for i in range(len(board)):
        for j in range (len(board[i])):
            if(board[i][j] != EMPTY):
                usedSpaces+=1

    return True if winner(board) is not None or usedSpaces == 9 else False
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    gameWinner = winner(board)
    if gameWinner == X:
        return 1
    elif gameWinner == O:
        return -1
    else:
        return 0
    raise NotImplementedError

# this function is only called for AI, no need to check for user
# however, AI could be X or O so need to check if user is mini or Max
def miniMaxScore(board, player):
    """
    Returns the optimal action for the current player on the board.
    """ 
    #Check if borad is a Winner or All spaces taken up 
    # this will be the last layer when looking at all possible stages
    if terminal(board) == True:
        score = utility(board)
        return [-1, -1, score]

    # default for max - x or mini - o
    if  player == X:
        best = [-1, -1, -Infinity]
    else:
        best = [-1, -1, +Infinity]

    # loop through all open spaces
    for space in list(actions(board)):
        # send current open space and current board to get new board
        newBoard = result(board, space) 
        # recursive call to get next depth layer and value
        score = miniMaxScore(newBoard,  O if player == X else X) # now search next move
        # if the borad is won or all spaces are taken up, then [-1, -1, score] (set above)
        # so set the move to space[0] space[1]
        score[0], score[1] = space[0], space[1]

        # is user x-max or o-min then set the value
        if player == X:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score
    # recursive call return
    return best

    raise NotImplementedError


def minimax(board):
    # if stage is terminal, return None
    if terminal(board):
        return None

    # is player x - max or o - min
    xOrO = player(board) 
    
    #get the next move
    nextMove = miniMaxScore(board, xOrO)
    #return next move
    return (nextMove[0], nextMove[1])
