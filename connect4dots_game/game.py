"""
Connect Four - Core Game Logic
--------------------------------
Handles the board state, move validation, and win/draw detection.
Kept independent of any AI or GUI code so it can be reused/tested standalone.
"""

ROWS = 6
COLS = 7

EMPTY = 0
PLAYER = 1      # Human
AI = 2           # Computer


class Connect4:
    def __init__(self):
        # board[row][col], row 0 = top, row ROWS-1 = bottom
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.game_over = False
        self.winner = None  # None, PLAYER, AI, or 'draw'

    def copy(self):
        new_game = Connect4()
        new_game.board = [row[:] for row in self.board]
        new_game.game_over = self.game_over
        new_game.winner = self.winner
        return new_game

    def valid_moves(self):
        """Return list of column indices that aren't full."""
        return [c for c in range(COLS) if self.board[0][c] == EMPTY]

    def is_valid_move(self, col):
        return 0 <= col < COLS and self.board[0][col] == EMPTY

    def drop_piece(self, col, piece):
        """Drop a piece into the given column. Returns the row it landed on, or None if invalid."""
        if not self.is_valid_move(col):
            return None
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][col] == EMPTY:
                self.board[row][col] = piece
                self._check_game_over(row, col, piece)
                return row
        return None

    def _check_game_over(self, row, col, piece):
        if self.check_win(piece):
            self.game_over = True
            self.winner = piece
        elif len(self.valid_moves()) == 0:
            self.game_over = True
            self.winner = 'draw'

    def check_win(self, piece):
        """Check whether the given piece has 4 in a row anywhere on the board."""
        b = self.board
        # Horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(b[r][c + i] == piece for i in range(4)):
                    return True
        # Vertical
        for c in range(COLS):
            for r in range(ROWS - 3):
                if all(b[r + i][c] == piece for i in range(4)):
                    return True
        # Diagonal (down-right)
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(b[r + i][c + i] == piece for i in range(4)):
                    return True
        # Diagonal (up-right)
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if all(b[r - i][c + i] == piece for i in range(4)):
                    return True
        return False

    def is_terminal(self):
        return self.game_over or len(self.valid_moves()) == 0

    def print_board(self):
        symbols = {EMPTY: '.', PLAYER: 'X', AI: 'O'}
        for row in self.board:
            print(' '.join(symbols[cell] for cell in row))
        print(' '.join(str(i) for i in range(COLS)))
