"""
Tic Tac Toe Player
"""

import math

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
    xCount = 0
    oCount = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == "X":
                xCount = xCount + 1
            elif board[i][j] == "O":
                oCount = oCount + 1
    
    if xCount == oCount:
        return "X"
    else:
        return "O"
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibleActions = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                possibleActions.append((i, j))
    return possibleActions
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board. 
    """
    nextMove = player(board)
    newBoard = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
    for i in range(3):
        for j in range(3):
            newBoard[i][j] = board[i][j]
    if newBoard[action[0]][action[1]] is not EMPTY:
        raise ValueError("Invalid Action")
    newBoard[action[0]][action[1]] = nextMove
    return newBoard
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] is not None and (board[0][0] == board[0][1] == board[0][2]):#horizontal check
        return board[0][0]
    elif board [1][0] is not None and (board[1][0] == board[1][1] == board[1][2]):#horizontal check
        return board[1][0]
    elif board [2][0] is not None and (board[2][0] == board[2][1] == board[2][2]):#horizontal check
        return board[2][0]
    elif board[0][0] is not None and (board[0][0] == board[1][0] == board[2][0]):#vertical check
        return board[0][0]
    elif board[0][1] is not None and (board[0][1] == board[1][1] == board[2][1]):#vertical check
        return board[0][1]
    elif board[0][2] is not None and (board[0][2] == board[1][2] == board[2][2]):#vertical check
        return board[0][2]
    elif board[0][0] is not None and (board[0][0] == board[1][1] == board[2][2]):#diagonal check
        return board[0][0]
    elif board[0][2] is not None and (board[0][2] == board[1][1] == board[2][0]):#diagonal check
        return board[0][2]
    else:
        return None
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    xCounter = 0
    oCounter = 0
    if winner(board) == None:
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == "X":
                    xCounter = xCounter + 1
                elif board[i][j] == "O":
                    oCounter = oCounter + 1
        if xCounter == 5 and oCounter == 4:
            return True
        else:
            return False
    else:
        return True
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == "X":
        return 1
    elif winner(board) == "O":
        return -1
    else:
        return 0
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if player(board) == X:
        v = -2
        for action in actions(board):
            v2 =  max(v,minValue(result(board,action)))
            if v < v2:
                v = v2
                bestAction = action
        return bestAction
    else:
        v = 2
        for action in actions(board):
            v2 = min(v,maxValue(result(board,action)))
            if v > v2:
                v = v2
                bestAction = action
        return bestAction
    raise NotImplementedError

def maxValue(board):
    v = -2
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, minValue(result(board,action)))
    return v

def minValue(board):
    v = 2
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, maxValue(result(board,action)))
    return v

            
   
