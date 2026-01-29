from src.connect4 import Board

# import numpy as np


# def test_test():
#     assert True


# def test_is_valid_col():
#     board_array = [
#         [0, 0, 0, 1, 0],
#         [0, 0, 0, 1, 0],
#         [0, 0, 0, 1, 0],
#         [0, 0, 0, 1, 0],
#         [1, 0, 1, 1, 0],
#     ]

#     board = Board(board_array)

#     assert board.is_valid_col(0)
#     assert board.is_valid_col(1)
#     assert board.is_valid_col(2)
#     assert not board.is_valid_col(3)
#     assert board.is_valid_col(4)


# def test_get_valid_row():
#     board_array = [
#         [0, 0, 0, 1, 0],
#         [0, 0, 1, 1, 0],
#         [0, 0, 1, 1, 0],
#         [0, 1, 1, 1, 0],
#         [1, 1, 1, 1, 0],
#     ]

#     board = Board(board_array)

#     assert board.get_valid_row(0) == 3
#     assert board.get_valid_row(1) == 2
#     assert board.get_valid_row(2) == 0
#     assert board.get_valid_row(3) == -1
#     assert board.get_valid_row(4) == 4


# def test_get_legal_moves():
#     board_array = [
#         [0, 0, 0, 1, 0],
#         [0, 0, 1, 1, 0],
#         [0, 0, 1, 1, 0],
#         [0, 1, 1, 1, 0],
#         [1, 1, 1, 1, 0],
#     ]

#     board = Board(board_array)

#     assert board.get_legal_moves() == [0, 1, 2, 4]
#     assert not board.get_legal_moves() == [3]


# def test_check_for_winner():
#     board_array_vertical_win = [
#         [0, 0, 0, 1, 0],
#         [0, 0, 0, 1, 0],
#         [0, 0, 1, 1, 0],
#         [0, 1, 1, 1, 0],
#         [0, 1, 1, 0, 0],
#     ]

#     board_array_horizontal_win = [
#         [0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0],
#         [0, 0, 1, 1, 0],
#         [0, 1, 1, 1, 0],
#         [1, 1, 1, 1, 0],
#     ]

#     board_array_down_right_win = [
#         [1, 0, 0, 0, 0],
#         [0, 1, 0, 0, 0],
#         [0, 0, 1, 1, 0],
#         [0, 1, 1, 1, 0],
#         [0, 1, 1, 1, 0],
#     ]

#     board_array_up_right_win = [
#         [0, 0, 0, 0, 0],
#         [0, 1, 0, 0, 1],
#         [0, 0, 1, 1, 0],
#         [0, 1, 1, 1, 0],
#         [0, 1, 1, 1, 0],
#     ]

#     board = Board(board_array_horizontal_win)
#     assert board.check_for_winner() == 1

#     board = Board(board_array_vertical_win)
#     assert board.check_for_winner() == 1

#     board = Board(board_array_down_right_win)
#     assert board.check_for_winner() == 1

#     board = Board(board_array_up_right_win)
#     assert board.check_for_winner() == 1


# def test_current_player():
#     board_array_2 = [
#         [0, 0, 0, 0, 0],
#         [0, 1, 0, 0, 1],
#         [0, 0, 1, 1, 0],
#         [0, 1, 1, 1, 0],
#         [0, 1, 1, 1, 0],
#     ]

#     board = Board(board_array_2)

#     assert board.get_current_player() == 2
