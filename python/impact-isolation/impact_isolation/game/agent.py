from __future__ import annotations

from typing import TYPE_CHECKING

from impact_isolation.game.models import EMPTY_MOVE, Move

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
        self._valid_moves = None
        self.num = -1

    def __repr__(self) -> str:
        return self.__class__.__name__ + str(self.num)

    def __str__(self) -> str:
        return self.__repr__()

    def set_board(self, board: Board) -> None:
        self._board_ref = board

    def valid_moves(self) -> list[tuple[int, int]]:
        self._valid_moves = self._board_ref.valid_moves(self._position)
        return self._valid_moves

    def evaluate(self) -> int:
        return len(self._valid_moves)

    def update_position(self, postion: tuple[int, int]) -> None:
        self._position = postion

    def make_move(self) -> Move:
        valid_moves = self.valid_moves()
        if not valid_moves:
            return EMPTY_MOVE
        position = random.choice(self.valid_moves())

        move = Move(self._position, position)
        return move
