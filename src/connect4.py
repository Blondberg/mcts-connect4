"""
Two implementations of the game Connect 4 against the computer using Monte Carlo Tree Search (MCTS).

One using a "conventional" array representation of a board, and one using a bitboard.
"""

import random
from board import Board
from mcts import mcts_search


def play_game():
    board = Board()
    current_player = 1
    game_over = False

    while not game_over:
        board.print()
        print("-----------")

        if current_player == 1:
            move = mcts_search(board, iterations=2000)
            print(f"MCTS plays: {move}")
        else:

            # Human plays
            legal_moves = board.get_legal_moves()
            move = None
            while move not in legal_moves:
                try:
                    move = int(input(f"Your turn! Choose a column {legal_moves}: "))
                except ValueError:
                    print("Please enter a valid integer.")
            # Random player
            # move = random.choice(board.get_legal_moves())
            # print(f"Random plays: {move}")

        board.drop_token(move, current_player)

        winner = board.check_for_winner()
        if winner:
            board.print()
            print(f"Player {winner} wins!")
            return

        current_player = 1 if current_player == 2 else 2

    print("Draw")


if __name__ == "__main__":
    play_game()
