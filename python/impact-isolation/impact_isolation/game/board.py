from __future__ import annotations

import logging

from .models import EMPTY_MOVE, Cell, Move
from .exceptions import InvalidMoveException, NoMovesException
from .agent import Agent

logger = logging.getLogger(__name__)

EMPTY_AGENT = Agent((-1, -1))


class Board:
    def __init__(self, size: int) -> None:
        # Board information
        self._size = size
        self._board = [[Cell.EMPTY for _x in range(size)] for _y in range(size)]

        self.move_history = [(EMPTY_AGENT, EMPTY_MOVE) for _ in range(size**2)]
        self.turn_number = 0

        # Game playing agents
        self.agents: list[Agent] = []
        self.num_agents = 0

    def _fill_position(
        self, position: tuple[int, int], cell_value: Cell = Cell.FILLED
    ) -> None:
        y, x = position
        self._board[y][x] = cell_value

    def add_agent(self, agent: Agent) -> Agent:
        pos = agent._position

        if self.turn_number > 0:
            raise ValueError("Cannot add an agent after the game has already began!")

        if not self._in_bounds(pos):
            raise ValueError("Starting postion must be in bounds.")

        if self._is_filled(pos):
            raise ValueError("Starting postion must not be occupied or filled.")

        self._fill_position(pos, cell_value=Cell.PLAYER)
        agent.set_board(self)
        self.agents.append(agent)
        agent.num = self.num_agents
        self.num_agents += 1

        return agent

    def make_move(self, agent: Agent, move: Move) -> None:
        if agent._position != move.start_pos:
            raise InvalidMoveException(f"Agent {agent} gave a move that is not from their position.")
        
        valid_moves = self.valid_moves(move.start_pos)
        if len(valid_moves) == 0:
            raise NoMovesException(f"Agent {agent} has no valid moves!")

        if agent._position != move.start_pos:
            raise InvalidMoveException(f"Agent {agent} gave a move that is not from their position.")
        
        if move.end_pos not in valid_moves:
            raise InvalidMoveException(f"Agent {agent} played an invalid move! {move}")

        logger.debug(f"Agent {agent} makes the move {move}")

        agent.update_position(move.end_pos)
        self._fill_position(move.start_pos, Cell.FILLED)
        self._fill_position(move.end_pos, Cell.PLAYER)
        self.move_history[self.turn_number] = (agent, move)
        self.turn_number += 1

    def unmake_move(self) -> tuple[Agent, Move]:
        self.turn_number -= 1
        agent, move = self.move_history[self.turn_number]
        self._fill_position(move.end_pos, Cell.EMPTY)
        self._fill_position(move.start_pos, Cell.PLAYER)
        agent.update_position(move.start_pos)

        return agent, move

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
        return self._board[y][x] != Cell.EMPTY

    def _in_bounds(self, position: tuple[int, int]) -> bool:
        y, x = position

        # x not in bounds
        if x < 0 or x >= self._size:
            return False

        # y not in bounds
        if y < 0 or y >= self._size:
            return False

        return True
