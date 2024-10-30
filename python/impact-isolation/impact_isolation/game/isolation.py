import logging
from dataclasses import dataclass

from .agent import Agent
from .board import Board
from .exceptions import InvalidMoveException, NoMovesException

logger = logging.getLogger(__name__)


@dataclass
class IsolationConfig:
    board_size: int
    agents: list[Agent]


class Isolation:
    def __init__(self, config: IsolationConfig) -> None:
        self.board = Board(config.board_size)
        for agent in config.agents:
            self.board.add_agent(agent)

        self.num_players = len(self.board.agents)

        # State management
        self.has_moves = [
            True if len(agent.valid_moves()) > 0 else False
            for agent in self.board.agents
        ]
        self.game_finished = False
        self.current_turn = 0
        self.current_agent = self.board.agents[0]

    def run_turn(self) -> None:
        try:
            move = self.current_agent.make_move()
            self.board.make_move(self.current_agent, move)
        except NoMovesException:
            logger.info(f"{self.current_agent} has ran out of moves!")
            self.has_moves[self.current_turn] = False
        except InvalidMoveException:
            logger.info(
                f"{self.current_agent} has been disqualified for an invalid move!"
            )
            self.has_moves[self.current_turn] = False

        self.get_next_player()

    def undo_turn(self) -> None:
        if self.board.turn_number == 0:
            raise ValueError("Cannot undo game with no moves")
        agent, move = self.board.unmake_move()
        self.current_turn = agent.num
        self.current_agent = agent

    def get_next_player(self) -> None:
        new_turn = -1
        new_player = None
        for i in range(1, self.num_players):
            new_turn = (self.current_turn + i) % self.num_players
            if self.has_moves[new_turn]:
                new_player = self.board.agents[new_turn]
                break

        if not new_player:
            self.game_finished = True
            self.winner = self.current_turn
            return
        logger.debug(f"new player chosen {new_player}, {new_turn}")
        self.current_agent = new_player
        self.current_turn = new_turn

    def run(self):
        while not self.check_finished():
            self.run_turn()
        logger.info(f"Game has been completed!")

    def check_finished(self) -> bool:
        return self.game_finished

    def get_winner(self) -> int:
        if self.game_finished:
            return self.winner

        return -1
