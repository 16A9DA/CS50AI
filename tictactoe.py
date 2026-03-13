"""
Tic Tac Toe Player
"""

import math
import copy

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
    X = "X"
    O = "O"
    count_of_X = 0
    count_of_O = 0
    """
    Returns player who has the next turn on a board.
    """
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                count_of_X+=1
            elif board[i][j] == O:
                count_of_O +=1 

    if count_of_X > count_of_O:
        return O
    elif count_of_X == count_of_O:
        return X
    else:
        return X


def actions(board):
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                actions.add((i,j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    i,j = action
    new_board[i][j] = player(board)

    return new_board

def winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0] 
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] and board[0][j] is not None:
            return board[0][j]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    
    return None
   

def terminal(board):
    if winner(board) != None:
        return True
    elif len(actions(board)) == 0:
        return True
    else:
        return False


def utility(board):
    if winner(board) == "X":
        return 1
    elif winner(board) == "O":
        return -1
    else:
        return 0


def minimax(board):
    if terminal(board):
        return None
    if len(actions(board)) == 0:
        return (0,0)

    if player(board) == "X":
        best_action = None
        best_score = -math.inf
        for action in actions(board):
            score = minplayer(result(board,action))
            if score > best_score:
                best_score = score
                best_action = action
        return best_action
    elif player(board) == "O":
        best_action = None
        best_score = math.inf
        for action in actions(board):
            score = max_player(result(board,action))
            if score < best_score:
                best_score = score
                best_action = action
        return best_action




def max_player(board):
    if terminal(board):
       return utility(board)
    else:
        v = -math.inf
        for action in actions(board):
            v = max(v,minplayer(result(board,action)))
    return v

def minplayer(board):
    if terminal(board):
        return utility(board)
    else:
        v = math.inf
        for action in actions(board):
            v  = min(v,max_player(result(board,action)))
    return v