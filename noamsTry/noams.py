from numpy.lib.utils import source
import pygame
from time import sleep
from math import radians, sin, cos, sqrt
import keyboard
import numpy as np
from numba import njit
from pygame.constants import BUTTON_X1

DARKGREY = np.array((59, 59, 64))
WINDOW_WIDTH: np.int16 = 700
WINDOW_HEIGHT: np.int16 = 500
RADIUS: np.int16 = 5
REFRESH_RATE: np.int16 = 60
HORIZONTAL_VELOCITY: np.int16 = 3
VERTICAL_VELOCITY: np.int16 = 5
BETA: np.float32 = np.deg2rad(10)
SPEED = 4.5
FPS = 60
AMOUNT_OF_STEPS = 5

pygame.init()
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
screen.fill(DARKGREY)
pygame.display.flip()
pygame.display.set_caption("AchtungGame")


grid = np.zeros(
    shape= (WINDOW_WIDTH, WINDOW_HEIGHT),

    # u for unsigned
    # int is the data type
    # 8 is the number of bits
    dtype= np.int8
)

@njit
def rotate(vel: np.ndarray, angle: np.float32):
    '''
    # Rotate a vector
    rotate the vector by `angle` degrees without changing its length
    ``` 
    x2 = cosβx1 − sinβy1
    y2 = sinβx1 + cosβy1
    ```
    '''
    vx = vel[0]
    vy = vel[1]
    vel[0] = cos(angle) * vx - sin(angle) * vy
    vel[1] = sin(angle) * vx + cos(angle) * vy


@njit
def normalize(vec: np.ndarray, newLength: np.float32):
    '''
    # Normalize a vector
    change its length to the `newLength`
    '''
    (x, y) = vec
    k = np.sqrt((x**2)+(y**2))
    l = newLength
    vec[0] = (l/k)*x
    vec[1] = (l/k)*y
    

@njit
def updateLastSteps(source: np.ndarray, pos: np.ndarray, n = AMOUNT_OF_STEPS):
    '''
    # update last steps
    delete the last step in 

    `source`: the steps array. its shape is `[n, 2]`.
    `n`: the amount of steps
    '''
    target = np.zeros((AMOUNT_OF_STEPS, 2), np.int16)
    for i in np.arange(n - 1):
        target[i + 1]= source[i]
    target[0,0] = pos[0]
    target[0,1] = pos[1]
    return target



class Snake():
    sid = -1
    isAlive = True
    angle = BETA
    pos = np.array((0.0,0.0), np.float32)
    vel = np.array((0.0,0.0), np.float32)
    lastSteps = np.ndarray((5, 2), np.int16)

    def __init__ (self, color, x, y, sid):
        self.color = color
        self.pos = np.array((x, y), np.float32)
        self.vel = np.array((3, 3), np.float32)
        for i in range(AMOUNT_OF_STEPS):
            self.lastSteps[i, 0] = x
            self.lastSteps[i, 1] = y
        self.sid = sid

    def update_velocity(self):
        self.rotate()
        self.normalize()
        
    def update_pos(self):
        # update last steps
        self.lastSteps = updateLastSteps(
            source= self.lastSteps,
            pos= self.pos
        )
        
        
        print(f'{self.lastSteps}\n')

        self.update_velocity()
        self.pos = self.pos + self.vel

        x, y = self.pos
        grid[x, y] = self.sid
    
    def rotate(self):
        rotate(self.vel, self.angle)
    
    def normalize(self):
        normalize(self.vel, SPEED)

    def draw(self):
        pygame.draw.circle(screen, (254, 5, 64),
                           self.pos, RADIUS, 0)

def dryRun():
    '''
    # Dry run
    simple function for running the `@njit`ed functions
    for the first time in order to make an executable code for the "real" run
    '''
    rotate(np.zeros((2), dtype= np.float32), 0)
    normalize(np.ones((2), np.float32), 1.0)
    updateLastSteps(
        source= np.zeros((AMOUNT_OF_STEPS, 2), dtype= np.int16),
        pos= np.array((0, 0), dtype= np.float32)
    )


dryRun()
clock= pygame.time.Clock()

snake1 = Snake((256, 0, 0), WINDOW_WIDTH / 8, WINDOW_HEIGHT / 8, 1)
finish = False
while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
         
    if keyboard.is_pressed('A'):
        snake1.angle = BETA
        
    elif keyboard.is_pressed('D'):
        snake1.angle = -BETA
        
    else:
        snake1.angle = 0
        
    snake1.update_pos()
    snake1.draw()

    
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()