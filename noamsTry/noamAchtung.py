
import pygame
from time import sleep
from math import radians, sin, cos, sqrt
import keyboard
import numpy as np
from numba import njit
import random

# colors
DARKGREY = np.array((59, 59, 64))
HEAD_COLOR = np.array((254, 255, 1))

WINDOW_WIDTH: np.int16 = 700
WINDOW_HEIGHT: np.int16 = 500

RADIUS: np.int16 = 5

HORIZONTAL_VELOCITY: np.int16 = 3
VERTICAL_VELOCITY: np.int16 = 100
BETA: np.float32 = np.deg2rad(10)
SPEED = 2


FPS = 60
AMOUNT_OF_STEPS = 5

pygame.init()
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
screen.fill(DARKGREY)
pygame.display.flip()
pygame.display.set_caption("AchtungGame")


grid = np.zeros(
    shape=(WINDOW_WIDTH, WINDOW_HEIGHT),

    # u for unsigned
    # int is the data type
    # 8 is the number of bits
    dtype=np.int8
)


@njit
def distance(pos1: np.ndarray, pos2: np.ndarray):
    '''
    # Distance between 2 points
    '''

    x1, y1 = pos1
    x2, y2 = pos2
    return sqrt(((x1-x2)**2)+((y1-y2)**2))


@njit
def collision(grid: np.ndarray, steps: np.ndarray, pos: np.ndarray):
    '''
    # Check snake collision
    the function will check:
    1. if the given snake collided with walls
    2. if the given snake collided with another snake
    3. if the given snake collided with him self

    # returns:
    `True` if one of the conditions was met
    `False` if else

    # Alogorithm
    The function reduces the boundaries of the square according
    to the boundaries of the grid.

    There are four Extreme situations:
    for `(x1,y1) = pos ~the center of the square~`
    1. if the part of the square between `x1-2r` and `x1` is off the grid's boundaries
    (`x1-2r < 0`) then the square boundaries will be between `0` and `x1+2r`.

    2. if the part of the square between `x1+2r` and the `~WINDOW_WIDTH~` is off the grid's boundaries
    (`1x1+2r > ~WINDOW_WIDTH~1`) then the square boundaries will be between `x1-2r` and `~WINDOW_WIDTH~`.

    3. if the part of the square between `y1-2r` and `y1` is off the grid's boundaries
    (`y1-2r < 0`) then the square boundaries will be between `0` and `y1+2r`.

    4. if the part of the square between `y1+2r` and the `~WINDOW_HEIGHT~` is off the grid's boundaries
    (`y1+2r > ~WINDOW_HEIGHT~`) then the square boundaries will be between `y1-2r` and `~WINDOW_HEIGHT~`.

    Therefore:
    '''
    r = RADIUS
    w = WINDOW_WIDTH
    h = WINDOW_HEIGHT

    x1 = np.int16(pos[0])
    y1 = np.int16(pos[1])

    # check collision with walls
    if x1 + r > w or x1 - r < 0:
        return 1
    if y1 + r > h or y1 - r < 0:
        return 1

    # check collision with the snake itself or another snake
    for x in np.arange(max(x1 - 2*r, 0), min(x1 + 2*r, w)):
        for y in np.arange(max(y1 - 2*r, 0), min(y1 + 2*r, h)):

            isValid = 1
            for i in np.arange(len(steps)):
                if x == steps[i, 0] and y == steps[i, 1]:
                    isValid = 0
                    break

            if not isValid:
                continue

            if distance(pos, (x, y)) > 2 * r:
                continue

            if grid[x, y] != 0:
                return 1

    return 0


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
def updateLastSteps(source: np.ndarray, pos: np.ndarray, n=AMOUNT_OF_STEPS):
    '''
    # update last steps
    delete the last step in

    `source`: the steps array. its shape is `[n, 2]`.
    `n`: the amount of steps
    '''
    target = np.zeros((AMOUNT_OF_STEPS, 2), np.int16)
    for i in np.arange(n - 1):
        target[i + 1] = source[i]
    target[0, 0] = pos[0]
    target[0, 1] = pos[1]
    return target


class Snake():
    sid = -1
    isAlive = True
    angle = BETA
    pos = np.array((0.0, 0.0), np.float32)
    vel = np.array((0.0, 0.0), np.float32)
    lastSteps = np.ndarray((5, 2), np.int16)
    holeTimer = 0

    def __init__(self, color, x, y, sid):
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
        self.update_velocity()
        self.pos = self.pos + self.vel

    def setHole(self):
        x = random.randint(1, 20)
        if x == 8:
            self.holeTimer = random.randint(3, 20)

    def update(self):
        global grid

        self.setHole()

        # update last steps
        self.lastSteps = updateLastSteps(
            source= self.lastSteps,
            pos= self.pos
        )

        self.update_pos()

        # check collision
        if (collision(grid, self.lastSteps, self.pos)):
            self.isAlive = False

        # update grid
        x = np.int16(self.pos[0])
        y = np.int16(self.pos[1])

        if self.holeTimer != 0:
            self.holeTimer -= 1
            grid[x, y] = 0
            
        else:
            grid[x, y] = self.sid

    def rotate(self):
        rotate(self.vel, self.angle)

    def normalize(self):
        normalize(self.vel, SPEED)

    def draw(self):
        # draw last step, then draw the head.
        if self.holeTimer != 0:
            pygame.draw.circle(screen, DARKGREY,
                               self.lastSteps[0], RADIUS, 0)
        else:
            pygame.draw.circle(screen, self.color,
                               self.lastSteps[0], RADIUS, 0)

        pygame.draw.circle(screen, HEAD_COLOR,
                           self.pos, RADIUS, 0)


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

snake1 = Snake((255, 0, 0), WINDOW_WIDTH / 8, WINDOW_HEIGHT / 8, 1)
snake2 = Snake ((140, 188, 255), WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, 2)
snakes = []
snakes.append(snake1)
snakes.append(snake2)

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

    if keyboard.is_pressed('M'):
        snake2.angle = BETA

    elif keyboard.is_pressed('N'):
        snake2.angle = -BETA

    else:
        snake2.angle = 0

    for i in range(len(snakes)):
        if snakes[i].isAlive:
            snakes[i].update()
            snakes[i].draw()

    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
