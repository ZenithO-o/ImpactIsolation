import logging
import pygame
from impact_isolation.game.agent import Agent
from impact_isolation.game.isolation import Isolation, IsolationConfig

colors = {
    "bg": pygame.Color(14, 17, 22),
    "filled": pygame.Color(37, 110, 255),
    "empty": pygame.Color(252, 252, 252),
    "agent": pygame.Color(61, 220, 151),
    "move": pygame.Color(255, 73, 92),
}

SCREEN_SIZE = (1280, 720)
SCREEN_CENTER = pygame.Vector2(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)
TILE_SIZE = 40
TILE_GAP = 4

logger = logging.getLogger(__name__)


class InteractiveRender:
    def __init__(self, game: Isolation) -> None:
        self.game = game
        self._auto_run = False
        self._run()

    def _render_board(self):
        board = self.game.board

        agent_positions = set([agent._position for agent in board.agents])
        active_agent = self.game.current_agent
        active_moves = set(active_agent.valid_moves())

        FULL_SIZE = (TILE_SIZE * board._size) + (TILE_GAP * (board._size - 1))
        TOP_LEFT = SCREEN_CENTER - pygame.Vector2(FULL_SIZE / 2, FULL_SIZE / 2)

        y_off = 0
        for y, row in enumerate(board._board):
            x_off = 0
            for x, value in enumerate(row):
                color = colors["empty"]
                if (y, x) in agent_positions:
                    color = colors["agent"]
                elif active_moves and (y, x) in active_moves:
                    color = colors["move"]
                elif value != 0:
                    color = colors["filled"]

                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(
                        TOP_LEFT.x + x_off, TOP_LEFT.y + y_off, TILE_SIZE, TILE_SIZE
                    ),
                )
                x_off += TILE_SIZE + TILE_GAP
            y_off += TILE_SIZE + TILE_GAP

    def _render_title(self): ...

    def _run(self):
        # Example file showing a circle moving on screen
        import pygame

        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            # pygame.KEYDOWN event means the first frame the user pressed a key
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        try:
                            self.game.undo_turn()
                        except ValueError as err:
                            logger.error(err)
                    if event.key == pygame.K_e:
                        self.game.run_turn()
                    if event.key == pygame.K_r:
                        self._auto_run = True

            if self._auto_run and self.game.get_winner() == -1:
                self.game.run_turn()

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill(colors["bg"])
            self._render_title()
            self._render_board()

            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 120
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            self.dt = self.clock.tick(120) / 1000

        pygame.quit()
