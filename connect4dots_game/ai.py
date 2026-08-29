"""
Connect Four AI - Minimax with Alpha-Beta Pruning
---------------------------------------------------
Implements:
  1. Plain minimax (minimax_plain) - for benchmarking / comparison
  2. Minimax with alpha-beta pruning (minimax_ab) - used by the actual game
  3. A heuristic evaluation function for non-terminal (depth-limited) states

Node counters are included so you can empirically demonstrate how much
alpha-beta pruning reduces the search space vs. plain minimax - useful
for a report/benchmark section.
"""

import math
from game import ROWS, COLS, EMPTY, PLAYER, AI

WINDOW_LENGTH = 4


# ---------------------------------------------------------------------------
# Heuristic evaluation
# ---------------------------------------------------------------------------

def evaluate_window(window, piece):
    """Score a 4-cell window based on piece counts."""
    opponent = PLAYER if piece == AI else AI
    score = 0

    piece_count = window.count(piece)
    empty_count = window.count(EMPTY)
    opp_count = window.count(opponent)

    if piece_count == 4:
        score += 100
    elif piece_count == 3 and empty_count == 1:
        score += 5
    elif piece_count == 2 and empty_count == 2:
        score += 2

    if opp_count == 3 and empty_count == 1:
        score -= 4

    return score


def score_position(board, piece):
    """Heuristic score of the whole board from `piece`'s perspective."""
    score = 0

    # Center column preference (center control is strategically strong)
    center_col = [board[r][COLS // 2] for r in range(ROWS)]
    score += center_col.count(piece) * 3

    # Horizontal
    for r in range(ROWS):
        row_array = board[r]
        for c in range(COLS - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Vertical
    for c in range(COLS):
        col_array = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Diagonal (down-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Diagonal (up-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            window = [board[r - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _order_moves(valid_moves):
    """Search center columns first - improves alpha-beta pruning efficiency."""
    center = COLS // 2
    return sorted(valid_moves, key=lambda c: abs(c - center))


def _simulate_drop(game, col, piece):
    """Return a new game copy with the piece dropped in col."""
    new_game = game.copy()
    new_game.drop_piece(col, piece)
    return new_game


# ---------------------------------------------------------------------------
# Plain Minimax (no pruning) - for benchmarking only, gets slow past depth ~5
# ---------------------------------------------------------------------------

class NodeCounter:
    def __init__(self):
        self.count = 0


def minimax_plain(game, depth, maximizing_player, counter: NodeCounter):
    counter.count += 1
    valid_moves = game.valid_moves()
    is_terminal = game.is_terminal()

    if depth == 0 or is_terminal:
        if is_terminal:
            if game.winner == AI:
                return (None, 10_000_000)
            elif game.winner == PLAYER:
                return (None, -10_000_000)
            else:
                return (None, 0)
        else:
            return (None, score_position(game.board, AI))

    if maximizing_player:
        value = -math.inf
        best_col = valid_moves[0]
        for col in valid_moves:
            new_game = _simulate_drop(game, col, AI)
            _, new_score = minimax_plain(new_game, depth - 1, False, counter)
            if new_score > value:
                value = new_score
                best_col = col
        return best_col, value
    else:
        value = math.inf
        best_col = valid_moves[0]
        for col in valid_moves:
            new_game = _simulate_drop(game, col, PLAYER)
            _, new_score = minimax_plain(new_game, depth - 1, True, counter)
            if new_score < value:
                value = new_score
                best_col = col
        return best_col, value


# ---------------------------------------------------------------------------
# Minimax with Alpha-Beta Pruning - used by the actual game (fast)
# ---------------------------------------------------------------------------

def minimax_ab(game, depth, alpha, beta, maximizing_player, counter: NodeCounter = None):
    if counter is not None:
        counter.count += 1

    valid_moves = _order_moves(game.valid_moves())
    is_terminal = game.is_terminal()

    if depth == 0 or is_terminal:
        if is_terminal:
            if game.winner == AI:
                return (None, 10_000_000)
            elif game.winner == PLAYER:
                return (None, -10_000_000)
            else:
                return (None, 0)
        else:
            return (None, score_position(game.board, AI))

    if maximizing_player:
        value = -math.inf
        best_col = valid_moves[0]
        for col in valid_moves:
            new_game = _simulate_drop(game, col, AI)
            _, new_score = minimax_ab(new_game, depth - 1, alpha, beta, False, counter)
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # beta cut-off
        return best_col, value
    else:
        value = math.inf
        best_col = valid_moves[0]
        for col in valid_moves:
            new_game = _simulate_drop(game, col, PLAYER)
            _, new_score = minimax_ab(new_game, depth - 1, alpha, beta, True, counter)
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break  # alpha cut-off
        return best_col, value


def get_best_move(game, depth):
    """Convenience wrapper used by the GUI."""
    col, _ = minimax_ab(game, depth, -math.inf, math.inf, True)
    return col
