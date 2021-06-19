from typing import List

from player import *
from agent import *

snakes = List[Snake]
player = Player(COLORS_ARRAY[1], WINDOW_WIDTH / 8, WINDOW_HEIGHT / 8, 1, 'A', 'D')
agent = Agent(COLORS_ARRAY[3], WINDOW_WIDTH / 3, WINDOW_HEIGHT / 3, 3)
snakes = [agent]
