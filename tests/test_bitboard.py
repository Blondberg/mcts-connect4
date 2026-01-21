import pytest
from src.bitboard import C4BitBoard


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


def test_is_winning_move():
    bb = C4BitBoard(width=7, height=6)

    # Horizontal check
    moves = [0, 6, 1, 6, 2, 6]
    for col in moves:
        bb.play(col)

    assert bb.is_winning_move(3)

    # Vertical check
    moves = [6, 0, 6, 1, 6, 2]
    for col in moves:
        bb.play(col)

    assert bb.is_winning_move(6)

    # Down right check
    moves = [6, 5, 5, 4, 4, 3, 4, 3, 3, 2]
    for col in moves:
        bb.play(col)

    assert bb.is_winning_move(3)

    # Up right check
    moves = [0, 1, 1, 2, 2, 3, 2, 3, 3, 4]
    for col in moves:
        bb.play(col)

    assert bb.is_winning_move(3)
