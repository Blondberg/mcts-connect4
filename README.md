# Connect 4 - Bitboard + Monte Carlo Tree Search (MCTS)

[![Tests](https://github.com/Blondberg/mcts-connect4/actions/workflows/python-app.yml/badge.svg)](
https://github.com/Blondberg/mcts-connect4/actions/workflows/python-app.yml
)
[![License](https://img.shields.io/github/license/blondberg/mcts-connect4)](LICENSE)

A Python implementation of **Connect 4** using a bitboard representation.

The bitboard representation is heavily inspired by the explanations/implementations of:
* [Dominikus Herzberg](https://github.com/denkspuren/BitboardC4/blob/master/BitboardDesign.md)
* [Pascal Pons](http://blog.gamesolver.org/solving-connect-four/06-bitboard/)


## Getting started
### Prerequisites
With the exception of [Pytest](https://github.com/pytest-dev/pytest), the project uses no external packages—only pure Python and bit manipulation.
### Installation
1. Clone the repository
    ```bash
    git clone https://github.com/Blondberg/mcts-connect4.git
    cd mcts-connect4/
    ```
2. Create a virtual environment (not needed due to lack of packages, but I usually recommend it)
    ```bash
    python -m venv venv
    source venv/bin/activate        # Linux / macOS
    venv\Scripts\activate           # Windows
    ```
3. Install pytest
    ```bash
    pip install pytest
    ```

## Usage
* Play against the bot
    ```bash
    python main.py
    ```

* To run testing with Pytest
    ```bash
    pytest
    ```

## Roadmap
Possible future development/improvements:
- [ ] Create graphical interface using e.g. PyGame.
- [ ] Visualize MCTS process.
- [ ] Play around with similar search algorithms such as Mini-Max, and use alpha-beta pruning.
