class NoMovesException(Exception):
    """Raised when a agent attempts to make a move, but has no moves"""


class InvalidMoveException(Exception):
    """Raised when an agent makes a move that is not part of its valid moveset"""
