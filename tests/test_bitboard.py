import pytest
from src.bitboard import C4BitBoard
from src.mcts_bitboard import mcts_search


def test_bottom_cell_mask():
    bb = C4BitBoard(width=7, height=6)

    # Bottom bits for each column in sequence
    bottom_bits = [0, 7, 14, 21, 28, 35, 42]
    for i in range(len(bottom_bits)):
        assert bb.bottom_cell_mask(i) == 1 << bottom_bits[i]


def test_top_playable_cell_mask():
    bb = C4BitBoard(width=7, height=6)

    # Top playable bits for each column in sequence. Should be col*(height+1) + height - 1
    top_bits = [5, 12, 19, 26, 33, 40, 47]
    for i in range(len(top_bits)):
        assert bb.top_playable_cell_mask(i) == 1 << top_bits[i]


def test_can_play_initial():
    """Test if all columns are playable at the initial state"""
    bb = C4BitBoard()
    for col in range(bb.width):
        assert bb.can_play(col)


def test_get_legal_moves_initial():
    bb = C4BitBoard()
    assert bb.get_legal_moves() == list(range(bb.width))


def test_blocking():
    bb = C4BitBoard()
    moves = [0, 1, 1, 2, 2]


@pytest.mark.parametrize(
    "moves, winning_col",
    [
        # Horizontal win
        ([0, 6, 1, 6, 2, 6], 3),
        # Vertical win
        ([6, 0, 6, 1, 6, 2], 6),
        # Down-right diagonal win
        ([6, 5, 5, 4, 4, 3, 4, 3, 3, 2], 3),
        # Up-right diagonal win
        ([0, 1, 1, 2, 2, 3, 2, 3, 3, 4], 3),
    ],
)
def test_is_winning_move(moves, winning_col):
    bb = C4BitBoard(width=7, height=6)
    for col in moves:
        bb.play(col)
    assert bb.is_winning_move(winning_col)


@pytest.mark.parametrize(
    "moves, expected_move",
    [
        # Horizontal win
        ([0, 6, 1, 6, 2, 6], 3),
        # Vertical win
        ([6, 0, 6, 1, 6, 2], 6),
        # Down-right diagonal win
        ([6, 5, 5, 4, 4, 3, 4, 3, 3, 2], 3),
        # Up-right diagonal win
        ([0, 1, 1, 2, 2, 3, 2, 3, 3, 4], 3),
    ],
)
def test_mcts_winning_move(moves, expected_move):
    bb = C4BitBoard(width=7, height=6)
    for col in moves:
        bb.play(col)

    # Run MCTS
    move = mcts_search(bb, iterations=2000)
    assert move == expected_move


@pytest.mark.parametrize(
    "moves, blocking_col",
    [
        ([0, 1, 2, 3, 4, 5, 6, 0, 1, 0, 1, 0], 0),
    ],
)
def test_mcts_blocking(moves, blocking_col):
    bb = C4BitBoard(width=7, height=6)
    for col in moves:
        bb.play(col)

    # Run MCTS
    move = mcts_search(bb, iterations=2000)
    bb.print_player()
    bb.print_mask()
    # Assert AI blocks the immediate threat
    assert move == blocking_col
