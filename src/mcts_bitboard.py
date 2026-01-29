from src.bitboard import C4BitBoard
import math
import random

CENTER_ORDER = [3, 2, 4, 1, 5, 0, 6]


class MCTSNode:
    def __init__(self, state: C4BitBoard, parent: "MCTSNode" = None, move: int = None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children: list[MCTSNode] = []
        self.visits = 0
        self.value = 0.0  # Value of node based on win/loss/draw

        self.untried_moves = sorted(
            state.get_legal_moves(), key=lambda c: abs(c - state.width // 2)
        )

    def ucb1_score(self, exploration=0.8):
        if self.visits == 0:
            return float("inf")
        return self.value / self.visits + exploration * math.sqrt(
            math.log(self.parent.visits) / self.visits
        )

    def expand(self):
        move = self.untried_moves.pop()
        next_state = self.state.clone()
        next_state.play(move)
        child_node = MCTSNode(next_state, parent=self, move=move)
        self.children.append(child_node)
        return child_node

    def rollout(self):
        """Simulate a random game from the current node, return winner."""
        sim = self.state.clone()

        while True:
            moves = sim.get_legal_moves()
            if not moves:
                return 0  # draw

            played_move = None

            # Check if possible to win
            for m in moves:
                if sim.is_winning_move(m):
                    sim.play(m)
                    last_player = sim.mask ^ sim.current_player
                    return last_player

            # Check if possible to block a win
            opponent = sim.mask ^ sim.current_player
            for m in moves:
                move = (sim.mask + sim.bottom_cell_mask(m)) & sim.column_mask(m)
                if sim.is_win(opponent | move):
                    sim.play(m)
                    played_move = m
                    break

            # Random move if no win or block
            if played_move is None:
                sim.play(random.choice(moves))

            # # Check if the player who just played won
            last_player = sim.mask ^ sim.current_player
            if sim.is_win(last_player):
                return last_player

    def backpropagate(self, winner, root_player):
        self.visits += 1

        if winner == 0:
            self.value += 0.5
        elif winner & root_player:
            self.value += 1

        if self.parent:
            self.parent.backpropagate(winner, root_player)


def mcts_search(root_state: C4BitBoard, iterations=2000):
    root = MCTSNode(root_state)
    root_player = root_state.current_player

    moves = root_state.get_legal_moves()

    root_state.print_current_player()

    # Check if it is possible to win
    for m in moves:
        if root_state.is_winning_move(m):
            return m

    # Check if it is possible to block a win
    temp = root_state.clone()
    temp.switch_player()

    for m in moves:
        if temp.is_winning_move(m):
            return m

    for _ in range(iterations):
        node = root

        # Selection
        while not node.untried_moves and node.children:
            node = max(node.children, key=lambda n: n.ucb1_score())

        # Expansion
        if node.untried_moves:
            node = node.expand()

        # Simulation
        winner = node.rollout()

        # Backpropagation
        node.backpropagate(winner, root_player)

    return max(root.children, key=lambda c: c.visits).move
