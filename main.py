from src.bitboard import C4BitBoard
from src.mcts_bitboard import mcts_search


def print_board(board: C4BitBoard):
    print("\nCurrent board:")
    for row in reversed(range(board.height)):
        line = []
        for col in range(board.width):
            bit = 1 << (col * (board.height + 1) + row)
            if board.mask & bit:
                if board.current_player & bit:
                    line.append(" O ")
                else:
                    line.append(" X ")
            else:
                line.append(" . ")

        print(" ".join(line))
    print(" 0   1   2   3   4   5   6\n")


def human_move(board: C4BitBoard):
    while True:
        try:
            col = int(input("Your move (0-6): "))
            if col not in range(board.width):
                print("Column out of range")
                continue
            if not board.can_play(col):
                print("Column is full")
                continue
            return col
        except ValueError:
            print("Please enter a number.")


def bot_move(board: C4BitBoard, iterations=2000):
    print("Bot is thinking...")
    return mcts_search(board, iterations)


def check_game_over(board: C4BitBoard) -> int | None:
    last_player = board.mask ^ board.current_player

    if board.is_win(last_player):
        return last_player

    if not board.get_legal_moves():
        return 0  # draw

    return None


if __name__ == "__main__":
    board = C4BitBoard(width=7, height=6)

    print("You are X, Bot is O")

    while True:
        print_board(board)

        col = human_move(board)
        board.play(col)
        result = check_game_over(board)

        if result is not None:
            print_board(board)
            print("You win!" if result != 0 else "It's a draw!")
            break

        col = bot_move(board, iterations=100000)
        print(f"Bot plays column {col}")
        board.play(col)

        result = check_game_over(board)
        if result is not None:
            print_board(board)
            print("Bot wins 🤖" if result != 0 else "It's a draw!")
            break
