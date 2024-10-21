import logging
import sys
from collections import Counter

from impact_isolation.game import Agent, Isolation, IsolationConfig
from impact_isolation.render.render import InteractiveRender
from tqdm import tqdm

if __name__ == "__main__":
    root_logger = logging.getLogger()
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    log_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
    )
    stdout_handler.setFormatter(log_formatter)
    root_logger.addHandler(stdout_handler)
    root_logger.setLevel(logging.DEBUG)

    agents = [Agent((2, 2)), Agent((3, 3)), Agent((9, 9)), Agent((6, 6)), Agent((7, 7))]
    config = IsolationConfig(board_size=10, agents=agents)
    game = Isolation(config)

    InteractiveRender(game)

    # winner_counter = Counter()

    # wins = []

    # for i in tqdm(range(1000)):
    #     config = IsolationConfig(board_size=5, agents=[Agent((0, 0)), Agent((1, 1))])
    #     game = Isolation(config)
    #     game.run()
    #     win = game.get_winner()
    #     wins.append(win)

    # print(Counter(wins))
