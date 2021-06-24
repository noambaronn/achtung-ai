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

    n = (len(snakes))
    givenPoints = np.ones(n)
    isAlive = np.ones(n)
    scores = np.zeros(n)
    game_over = False
    playersActive = (len(snakes))
    for s in range (len(snakes)):
        if snakes[s].isAlive:
            snakes[s].update()
            snakes[s].draw()
        else:
            isAlive[s] = 0 
            m=0
            for k in range (len(isAlive)):
                if isAlive[k] == 0:
                    m+=1
            if m == n:
                font = pygame.font.Font('freesansbold.ttf', 100)
                text = font.render('GAME OVER !!', True, (0, 255 ,0), (0, 0, 255))
                textRect = text.get_rect()
                textRect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
                screen.blit(text, textRect)
            if isAlive[s] == 0 and givenPoints[s] == 1:
                print (isAlive)
                givenPoints[s] = 0
                for i in range (len(scores)):
                    if i != s:
                        if isAlive[i] == 1:
                            scores[i] += 1
                           
        for i in range (len(snakes)):
            snakes[i].score = scores[i]

        p = 0
        for i in range (len(snakes)):
            x = int(snakes[i].score) 
            score = str(x)
            Xpos = WINDOW_WIDTH + (ADDED_WALL //2)
            Ypos = (ADDED_WALL //2) + p
            p += 100
            font = pygame.font.Font('freesansbold.ttf', 25)
            text = font.render( score , True, (255, 255 ,0), (0, 0, 255))
            textRect = text.get_rect()
            textRect.center = (Xpos, Ypos)
            screen.blit(text, textRect)

    
        

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()



