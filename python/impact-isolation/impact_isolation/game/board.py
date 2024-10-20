from __future__ import annotations

from .agent import Agent


class Board:
    def __init__(self, size: int) -> None:
        # Board information
        self._size = size
        self._board = tuple([tuple([0 for _x in range(size)]) for _y in range(size)])

        # Game playing agents
        self._agents = []

    def _fill_position(self, position: tuple[int, int]):
        new_board = tuple(
            [
                tuple(
                    [1 if position == (j, i) else value for i, value in enumerate(row)]
                )
                for j, row in enumerate(self._board)
            ]
        )
        self._board = new_board

    def add_agent(self, agent: Agent):
        pos = agent._position

        if not self._in_bounds(pos):
            raise ValueError("Starting postion must be in bounds.")

        if self._is_filled(pos):
            raise ValueError("Starting postion must not be occupied or filled.")

        self._fill_position(pos)
        agent.set_board(self)

        self._agents.append(agent)

        return agent

    def valid_moves(self, position: tuple[int, int]) -> list[tuple[int, int]]:
        valid_moves = []
        y, x = position

        # check horizontal right
        if x < self._size - 1:
            for i in range(x + 1, self._size):
                if self._is_filled((y, i)):
                    break
                valid_moves.append((y, i))

        # check horizontal left
        if x > 0:
            for i in range(x - 1, -1, -1):
                if self._is_filled((y, i)):
                    break
                valid_moves.append((y, i))

        # check vertical up
        if y > 0:
            for j in range(y - 1, -1, -1):
                if self._is_filled((j, x)):
                    break
                valid_moves.append((j, x))

        # check vertical down
        if y < self._size - 1:
            for j in range(y + 1, self._size):
                if self._is_filled((j, x)):
                    break
                valid_moves.append((j, x))

        # check diagonal top-left
        max_top_left = min(x, y)
        for k in range(1, max_top_left + 1):
            if self._is_filled((y - k, x - k)):
                break
            valid_moves.append((y - k, x - k))

        # check diagonal bottom-right
        max_bottom_right = min(self._size - x - 1, self._size - y - 1)
        for k in range(1, max_bottom_right + 1):
            if self._is_filled((y + k, x + k)):
                break
            valid_moves.append((y + k, x + k))

        # check diagonal top-right
        max_top_right = min(self._size - x - 1, y)
        for k in range(1, max_top_right + 1):
            if self._is_filled((y - k, x + k)):
                break
            valid_moves.append((y - k, x + k))

        # check diagonal bottom-left
        max_bottom_left = min(x, self._size - y - 1)
        for k in range(1, max_bottom_left + 1):
            if self._is_filled((y + k, x - k)):
                break
            valid_moves.append((y + k, x - k))

        return valid_moves

    def _is_filled(self, position: tuple[int, int]) -> bool:
        y, x = position
        return self._board[y][x] > 0

    def _in_bounds(self, position: tuple[int, int]) -> bool:
        y, x = position

        # x not in bounds
        if x < 0 or x >= self._size:
            return False

        # y not in bounds
        if y < 0 or y >= self._size:
            return False

        return True
