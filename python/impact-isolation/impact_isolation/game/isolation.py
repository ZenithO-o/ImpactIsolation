import logging
from dataclasses import dataclass

from .agent import Agent
from .board import Board

logger = logging.getLogger("Isolation")


@dataclass
class IsolationConfig:
    board_size: int
    agents: list[Agent]


class Isolation:
    def __init__(self, config: IsolationConfig) -> None:
        self.board = Board(config.board_size)
        self.agents = [self.board.add_agent(agent) for agent in config.agents]

        # State management
        self.has_moves = [
            True if len(agent.valid_moves()) > 0 else False for agent in self.agents
        ]
        self.current_turn = 0
        self.game_finished = False
        self.num_players = len(self.agents)

    def _make_turn(self) -> None:
        curr_agent = self.agents[self.current_turn]
        old_pos = curr_agent._position

        if len(self.board.valid_moves(old_pos)) == 0:
            logger.info(
                f"Agent {self.current_turn} has no valid moves and is out of the game!"
            )
            self.has_moves[self.current_turn] = False
            if sum(self.has_moves) == 1:
                self.game_finished = True
            
            self.current_turn = (self.current_turn + 1) % self.num_players
            return

        move = curr_agent.make_move()
        logger.debug(f"Agent {self.current_turn} makes the move {move}")

        if move not in self.board.valid_moves(old_pos):
            raise RuntimeError(f"Agent {self.current_turn} returned invalid move!")

        self.board._fill_position(curr_agent._position)
        self.current_turn = (self.current_turn + 1) % self.num_players

    def run(self):
        while True:
            for i in range(self.num_players):
                self.current_turn = i
                logger.info(f"It is Agent {self.current_turn}'s turn!")
                try:
                    self._make_turn()
                except Exception as e:
                    logger.error(e)

    def get_winner(self) -> int:
        if self.game_finished:
            return self.has_moves.index(True)
        
        return -1
