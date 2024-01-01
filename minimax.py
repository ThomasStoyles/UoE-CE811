# Connect 4 implementation for MCTS and Minimiz.
# University of Essex.
# M. Fairbank November 2021 for course CE811 Game Artificial Intelligence
# 
# Acknowedgements: 
# All of the graphics and some other code for the main game loop and minimax came from https://github.com/KeithGalli/Connect4-Python
# Some of the connect4Board logic and MCTS algorithm came from https://github.com/floriangardin/connect4-mcts 
# Other designs are implemented from the Millington and Funge Game AI textbook chapter on Minimax.
import random
from connect4Board import Board
import math
import numpy as np

def static_evaluator(board, piece):
    grid = board.grid
    opponent_piece = 1 if piece == 2 else 2  # Determine opponent's piece
    score = 0

    # Check for wins
    for row in range(6):
        for col in range(4):
            window = list(grid[row, col:col + 4])
            score += evaluate_window(window, piece)

    for col in range(7):
        for row in range(3):
            window = list(grid[row:row + 4, col])
            score += evaluate_window(window, piece)

    for row in range(3):
        for col in range(4):
            window = [grid[row + i, col + i] for i in range(4)]
            score += evaluate_window(window, piece)

    for row in range(3):
        for col in range(3, 7):
            window = [grid[row + i, col - i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def evaluate_window(window, piece):
    opponent_piece = 1 if piece == 2 else 2

    # Score the window based on the number of pieces and empty slots
    score = 0
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2
    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 4
    return score # TODO enhance this logic so that your static evaluator gives useful recommendations.

def minimax(board, current_depth, max_depth, player, alpha=-math.inf, beta=math.inf):
    if player == board.get_player_turn():
        maximiser = True
    else:
        maximiser = False

    is_terminal = board.is_game_over()
    if current_depth == max_depth or is_terminal:
        if is_terminal:
            opponent = 3 - player
            if board.get_victorious_player() == player:
                return (None, +100000000)
            elif board.get_victorious_player() == opponent:
                return (None, -100000000)
            else:
                return (None, 0)
        else:
            return (None, static_evaluator(board, player))

    valid_moves = board.valid_moves()
    if maximiser:
        best_move = None
        best_value = -math.inf
        for move in valid_moves:
            new_board = board.play(move)
            _, value = minimax(new_board, current_depth + 1, max_depth, player, alpha, beta)
            
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
            if alpha >= beta:
                break
        return best_move, best_value
    else:  # Minimising player
        best_move = None
        best_value = math.inf
        for move in valid_moves:
            new_board = board.play(move)
            _, value = minimax(new_board, current_depth + 1, max_depth, player, alpha, beta)
            
            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_move, best_value
