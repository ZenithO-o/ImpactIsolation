from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .board import Board

import random


class Agent:
    """
    The Default agent. Returns a random move.
    """

    def __init__(self, position: tuple[int, int]) -> None:
        self._position = position
        self._board_ref = None

    def set_board(self, board: Board):
        self._board_ref = board

    def valid_moves(self):
        return self._board_ref.valid_moves(self._position)

    def make_move(self):
        self._position = random.choice(self.valid_moves())
        return self._position
