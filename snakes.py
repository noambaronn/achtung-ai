from typing import List

from numpy import False_, true_divide

from player import *
from agent import *

snakes = List[Snake]
player1 = Player(COLORS_ARRAY[1], 1, 'A', 'D')
player2 = Player(COLORS_ARRAY[2], 2, 'left', 'right')
player3 = Player(COLORS_ARRAY[3], 3, 'N', 'M')
agent = Agent(COLORS_ARRAY[3], 3)
snakes = [player1, player2, player3, agent]

