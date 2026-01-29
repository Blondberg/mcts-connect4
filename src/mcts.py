from board import Board
from copy import deepcopy
import math
import random


class MCTSNode:
    def __init__(self, state: Board, move=None, parent=None):
        self.state = state  # state represented by node
        self.parent = parent  # parent node
        self.move = move  # move that led to this node
        self.player = state.get_current_player()
        self.children = []  # expanded children of node
        self.visits = 0  # number of visits to node
        self.value = 0.0  # value of node based on win/loss/draw
        self.untried_moves = state.get_legal_moves()

    def is_fully_expanded(self) -> bool:
        """Check if node is fully expanded.

        Returns:
            bool: True if fully expanded, else False.
        """
        return len(self.untried_moves) == 0

    def is_terminal(self) -> bool:
        """Check if corresponding state of node is terminal

        Returns:
            bool: True if terminal, else False
        """
        return self.state.check_for_winner() != 0 or not self.state.get_legal_moves()

    def expand(self):
        move = self.untried_moves.pop()
        new_state = deepcopy(self.state)
        new_state.drop_token(move, self.player)
        child = MCTSNode(new_state, move=move, parent=self)
        self.children.append(child)
        return child

    def best_child(self, c_param=1.4):
        choices_weights = [
            (child.value / child.visits)
            + c_param * math.sqrt((2 * math.log(self.visits) / child.visits))
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

    def rollout(self):
        state = deepcopy(self.state)
        player = self.player

        while True:
            winner = state.check_for_winner()
            if winner != 0:
                return winner

            moves = state.get_legal_moves()
            if not moves:
                return 0

            move_chosen = None

            move_chosen = random.choice(moves)

            # Make the move and switch player
            state.drop_token(move_chosen, player)
            player = 1 if player == 2 else 2

    def backpropagate(self, winner):
        self.visits += 1
        if winner == self.player:
            self.value += 1
        elif winner != 0:
            self.value += -1
        elif winner == 0:
            self.value += 0.5
        if self.parent:
            self.parent.backpropagate(winner)


def mcts_search(board: Board, iterations=1000):
    root = MCTSNode(deepcopy(board))

    for _ in range(iterations):
        node = root
        # Selection / Expansion
        while not node.is_terminal():
            if not node.is_fully_expanded():
                node = node.expand()
                break
            else:
                node = node.best_child()

        # Simulation
        winner = node.rollout()

        # Backpropagation
        node.backpropagate(winner)

    # Collect stats for visualization
    stats = {}
    for child in root.children:
        stats[child.move] = {
            "visits": child.visits,
            "avg_value": child.value / child.visits if child.visits > 0 else 0,
        }

    # Best move
    if root.children:
        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.move, stats
    else:
        return random.choice(board.get_legal_moves()), stats
