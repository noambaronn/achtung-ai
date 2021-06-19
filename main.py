import pygame
import numpy as np


from constants import *
from screen_globals import *
from snake import *
from player import *

from snakes import *


pygame.init()


def dryRun():
    '''
    # Dry run
    simple function for running the `@njit`ed functions
    for the first time in order to make an executable code for the "real" run
    '''
    rotate(np.zeros((2), dtype=np.float32), 0)
    normalize(np.ones((2), np.float32), 1.0)
    updateLastSteps(
        source=np.zeros((AMOUNT_OF_STEPS, 2), dtype=np.int16),
        pos=np.array((0, 0), dtype=np.float32)
    )


dryRun()
clock = pygame.time.Clock()


finish = False
while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True

    for s in snakes:
        if s.isAlive:
            s.update()
            s.draw()

    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
