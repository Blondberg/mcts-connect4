from copy import deepcopy
import random


class Board:
    def __init__(self, board=None):
        if board is None:
            self.board = [[0] * 7 for _ in range(6)]
        else:
            self.board = board
        self.n_rows = len(self.board)
        self.n_cols = len(self.board[0])

    def print(self):
        for row in self.board:
            print(row)

    def is_valid_col(self, col):
        return 0 <= col < self.n_cols and self.board[0][col] == 0

    def get_valid_row(self, col):
        for row in range(self.n_rows - 1, -1, -1):
            if self.board[row][col] == 0:
                return row
        return -1

    def get_legal_moves(self):
        return [col for col in range(self.n_cols) if self.is_valid_col(col)]

    def drop_token(self, col, token):
        row = self.get_valid_row(col)
        if row != -1:
            self.board[row][col] = token

    def get_current_player(self):
        flat_board = [x for row in self.board for x in row if x != 0]
        return 1 if flat_board.count(2) >= flat_board.count(1) else 2

    def check_for_winner(self):
        # check rows
        for row in self.board:
            for col in range(self.n_cols - 3):
                window = row[col : col + 4]
                if window[0] != 0 and len(set(window)) == 1:
                    return window[0]

        # check columns
        for col in range(self.n_cols):
            for row in range(self.n_rows - 3):
                window = [self.board[row + i][col] for i in range(4)]
                if window[0] != 0 and len(set(window)) == 1:
                    return window[0]

        # check down-right diagonals
        for row in range(self.n_rows - 3):
            for col in range(self.n_cols - 3):
                window = [self.board[row + i][col + i] for i in range(4)]
                if window[0] != 0 and len(set(window)) == 1:
                    return window[0]

        # check up-right diagonals
        for row in range(3, self.n_rows):
            for col in range(self.n_cols - 3):
                window = [self.board[row - i][col + i] for i in range(4)]
                if window[0] != 0 and len(set(window)) == 1:
                    return window[0]

        return 0
