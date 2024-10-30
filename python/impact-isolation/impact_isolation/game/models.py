from dataclasses import dataclass
from enum import IntEnum


class Cell(IntEnum):
    EMPTY = 0
    FILLED = 1
    PLAYER = 2


@dataclass
class Move:
    start_pos: tuple[int, int]
    end_pos: tuple[int, int]


EMPTY_MOVE = Move((-1, -1), (-1, -1))
