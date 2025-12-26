"""
Tic Tac Toe Player
"""

from copy import deepcopy
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
    x_count = 0
    o_count = 0
    for row in board:
        for cell in row:
            if cell == X:
                x_count +=1
            elif cell == O:
                o_count +=1
    if x_count > o_count:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for rows in range(3):
        for columns in range(3):
            if board[rows][columns] ==  EMPTY:
                moves.add((rows,columns))
    return moves
    


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    Does not modify the original board.
    Raises an exception if the action is invalid.
    """
    i,j = action
    if board[i][j] != None:
        raise Exception("The place is already full")
    
    new_board = deepcopy(board)
    new_board[i][j] = player(board)
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]
    
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] and board[0][j] is not None:
            return board[0][j]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    for rows in board:
        if EMPTY in rows:
            return False
    
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board): 
        return None
    
    if player(board) == X:
        value,move = max_value(board)
        return move
    else:
        value,move = min_value(board)
        return move

def max_value(board):
    if terminal(board):
        utility(board),None

    value = float("-inf")
    move = None
    for action in actions(board):
        score,a = min_value(result(board,action))
        if score > value:
            value = score
            move = action
    
    return value,move



def min_value(board):
    if terminal(board):
        utility(board),None

    value = float("inf")
    move = None
    for action in actions(board):
        score,a = max_value(result(board,action))
        if score < value:
            value = score
            move = action
    
    return value,move