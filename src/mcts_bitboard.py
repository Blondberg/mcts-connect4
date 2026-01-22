from src.bitboard import C4BitBoard
import math
import random


class MCTSNode:
    def __init__(self, state: C4BitBoard, parent: MCTSNode = None, move: int = None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children: list[MCTSNode] = []
        self.visits = 0
        self.value = 0.0  # Value of node based on win/loss/draw
        self.untried_moves = state.get_legal_moves()

    def ucb1_score(self, exploration=1.4):
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
        player = sim.current_player

        while True:
            moves = sim.get_legal_moves()
            if not moves:
                return 0  # draw

            move = random.choice(moves)
            sim.play_without_switch(move)

            # Check if the player who just played won
            if sim.is_win(player):
                return player

            # Switch player
            player = sim.mask ^ sim.current_player

    def backpropagate(self, winner, root_player):
        self.visits += 1
        if winner & root_player:
            self.value += 1
        elif winner == 0:
            self.value += 0.5
        # else:
        #     self.value -= 1

        if self.parent:
            self.parent.backpropagate(winner, root_player)


def mcts_search(root_state: C4BitBoard, iterations=2000):
    root = MCTSNode(root_state)
    root_player = (
        root_state.current_player
    )  # bitboard for current player (the one being simulated)

    for _ in range(iterations):
        node = root

        # Selection
        while node.untried_moves == [] and node.children:
            node = max(node.children, key=lambda n: n.ucb1_score())

        # Expansion
        if node.untried_moves:
            node = node.expand()

        # Simulation
        winner = node.rollout()

        # Backpropagation
        node.backpropagate(winner, root_player)

    return max(root.children, key=lambda c: c.visits).move
