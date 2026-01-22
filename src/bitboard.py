"""
A bitboard implementation of Connect 4 made in Python.

The code is heavily inspired by the explanations of:
* Dominikus Herzberg (https://github.com/denkspuren/BitboardC4/blob/master/BitboardDesign.md)
* Pascal Pons (http://blog.gamesolver.org/solving-connect-four/06-bitboard/)

I highly recommend checking them out!

"""


class C4BitBoard(object):
    def __init__(self, player: int = 0, mask: int = 0, width=7, height=6):
        """Constructor for bitboard

        Args:
            player (int, optional): Mask for bits where current player's tokens are. Defaults to 0.
            mask (int, optional): Mask for bits where any tokens are. Defaults to 0.
            width (int, optional): Width of board. Defaults to 7.
            height (int, optional): Height of playable board. A sentinel row will be added. Defaults to 6.
        """
        self.width = width
        self.height = height

        self.current_player = player  # current player tokens
        self.mask = mask  # all tokens

    def top_playable_cell_mask(self, col: int) -> int:
        """Returns a bitmask with the top playable cell (i.e. disregarding the sentinel row).

        E.g. top_mask(1) for a 4x4 bitboard would return 0b100000000 marking
            | 0 | 1 | 2 | 3 |
            |---|---|---|---|
            | . | . | . | . |
            | . | x | . | . |
            | . | . | . | . |
            | . | . | . | . |
            | . | . | . | . |
        as that is the top playable cell for that column.

        Args:
            col (int): Column to check.

        Returns:
            int: Bitmask of top playable cell of column.
        """
        return 1 << self.height - 1 << col * (self.height + 1)

    def bottom_cell_mask(self, col: int) -> int:
        """Returns a bitmask with the bottom cell.

        E.g. bottom_mask(1) for a 4x4 bitboard would return 0b100000 marking
            | 0 | 1 | 2 | 3 |
            |---|---|---|---|
            | . | . | . | . |
            | . | . | . | . |
            | . | . | . | . |
            | . | . | . | . |
            | . | x | . | . |

        Args:
            col (int): Column to check.

        Returns:
            int: Bitmask of bottom cell of column.
        """
        return 1 << col * (self.height + 1)

    def play(self, col: int):
        self.current_player ^= self.mask  # Switch to opponent player
        move = self.mask + self.bottom_cell_mask(col)
        self.mask |= move

    def play_without_switch(self, col: int):
        """Drop a token for the current_player without switching players.

        Args:
            col (int): Column to drop into.
        """
        move = self.mask + self.bottom_cell_mask(col)
        self.mask |= move
        self.current_player |= move

    def is_win(self, bitboard) -> bool:
        """Check if bitboard has a winning position.

        It is done by shifting the bitboard 3 times in the direction of the check
        and looking for overlaps each time.

        Returns:
            bool: True if current position is a win, else False
        """

        # Horizontal
        pairs = bitboard & (bitboard >> (self.height + 1))
        if pairs & (pairs >> (2 * (self.height + 1))):
            return True

        # Vertical
        pairs = bitboard & (bitboard >> 1)
        if pairs & (pairs >> 2):
            return True

        # Down right
        pairs = bitboard & (bitboard >> (self.height))
        if pairs & (pairs >> (2 * (self.height))):
            return True

        # Up right
        pairs = bitboard & (bitboard >> (self.height + 2))
        if pairs & (pairs >> (2 * (self.height + 2))):
            return True

        return False

    def can_play(self, col: int) -> bool:
        """Check if chosen column is playable, i.e. no token at top playable cell.

        Args:
            col (int): Column to check

        Returns:
            bool: True if playable, else False
        """

        return (self.mask & self.top_playable_cell_mask(col)) == 0

    def is_winning_move(self, col: int) -> bool:
        """Check whether playing a column results in a win.

        Args:
            col (int): Column to test.

        Returns:
            bool: True if it is a win, else False.
        """
        pos = self.current_player
        move = self.mask + self.bottom_cell_mask(col)
        pos |= move

        return self.is_win(pos)

    def print_mask(self):
        """Prints bitboard for mask"""
        print("###### MASK ######")
        for row in reversed(range(self.height + 1)):
            line = []
            for col in range(self.width):
                bit = 1 << (col * (self.height + 1) + row)
                line.append("1" if (self.mask & bit) else ".")
            print(" ".join(line))
        print("##################")

    def print_player(self):
        """Prints bitboard for current player"""
        print("###### Player ######")
        for row in reversed(range(self.height + 1)):
            line = []
            for col in range(self.width):
                bit = 1 << (col * (self.height + 1) + row)
                line.append("1" if (self.current_player & bit) else ".")
            print(" ".join(line))
        print("##################")

    def get_legal_moves(self):
        return [col for col in range(self.width) if self.can_play(col)]

    def clone(self):
        return C4BitBoard(
            player=self.current_player,
            mask=self.mask,
            width=self.width,
            height=self.height,
        )

    def make_move(self, col: int):
        new = self.clone()
        move = new.mask + new.bottom_cell_mask(col)
        new.mask |= move
        new.current_player ^= new.mask
        return new


if __name__ == "__main__":
    bitboard = C4BitBoard(width=4, height=4)

    bitboard.play(3)
    bitboard.print_mask()
    bitboard.print_player()

    bitboard.play(3)
    bitboard.print_mask()
    bitboard.print_player()
    print(bin(bitboard.mask))
