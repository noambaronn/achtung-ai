import numpy as np
from numba import njit
import keyboard

import time

from constants import *
from screen_globals import *
from snake import *


def profile(func, *params):
    t1 = time.perf_counter()
    func(*params)
    t2 = time.perf_counter()
    print(f'time = {t2 - t1}')


@njit
def arotate(vel: np.ndarray, angle: np.float32):
    '''
    # Rotate a vector
    rotate the vector by `angle` degrees without changing its length
    # returns:
    the desired vector
    ```
    x2 = cosβx1 − sinβy1
    y2 = sinβx1 + cosβy1
    ```
    '''
    vec = np.zeros_like(vel)
    vx = vel[0]
    vy = vel[1]
    vec[0] = cos(angle) * vx - sin(angle) * vy
    vec[1] = sin(angle) * vx + cos(angle) * vy
    return vec


@njit
def findNextSteps(
    pos: np.ndarray,
    vel: np.ndarray):

    left = np.zeros_like(vel)
    right = np.zeros_like(vel)
    straight = np.zeros_like(vel)

    left = arotate(vel, BETA)
    normalize(left, SPEED)
    left[0] += pos[0]
    left[1] += pos[1]

    right = arotate(vel, -BETA)
    normalize(right, SPEED)
    right[0] += pos[0]
    right[1] += pos[1]
    
    straight = vel
    normalize(straight, SPEED)
    straight[0] += pos[0]
    straight[1] += pos[1]

    nextSteps = np.empty((3, 2), np.float32)
    nextSteps[0] = left
    nextSteps[1] = straight
    nextSteps[2] = right

    return nextSteps


@njit
def acollision(grid: np.ndarray, steps: np.ndarray, pos: np.ndarray, r = RADIUS):
    '''
    regular collision that can have a different radius
    and returns the amount of valid squares in the checked region
    '''
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
                if x == np.int0(steps[i, 0]) and y == np.int0(steps[i, 1]):
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
def findNextVelocities(vel: np.ndarray):
    left = np.zeros_like(vel)
    right = np.zeros_like(vel)
    straight = np.zeros_like(vel)

    left = arotate(vel, BETA)
    straight = vel   
    right = arotate(vel, -BETA)
    
    normalize(left, SPEED)
    normalize(right, SPEED)
    normalize(straight, SPEED)

    nextVelocites = np.empty((3, 2), np.float32)
    nextVelocites[0] = left
    nextVelocites[1] = straight
    nextVelocites[2] = right

    return nextVelocites

@njit
def calculateRoute(
    grid: np.ndarray,
    lastSteps: np.ndarray,
    pos: np.ndarray,
    vel: np.ndarray,
    depth = AGENT_DEPTH):
    #TODO add a vels matrix

    #TODO make the recursion

    #TODO add a recursion-break statement at the start when
    #TODO @depth == 0 or 1 the choice is yours
    
    #TODO remember to check cleaning
    '''
    a recursive function
    ### returns:
    an int score for the given path
    '''
    score: np.int16 = 0
    nextSteps = findNextSteps(pos, vel)
    nextVelocities = findNextVelocities(vel)

    steps = np.copy(lastSteps)
    steps = updateLastSteps(steps, pos)
    
    # think as if the agent took
    x = np.int16(pos[0])
    y = np.int16(pos[1])
    

    keep = grid[x, y]
    grid[x, y] = AGENT_CODE

    # check for each one
    for i in np.arange(3, dtype= np.int16):
        if acollision(grid, steps, nextSteps[i, :]) == 0:
            if depth == 1:
                score += 1
            else:
                score += 1 + calculateRoute(grid, steps, nextSteps[i, :], nextVelocities[i, :],  depth - 1)


    grid[x, y] = keep
    return score    
    
@njit
def bestChoice(grid: np.ndarray, lastSteps: np.ndarray, pos: np.ndarray, vel: np.ndarray, depth = AGENT_DEPTH):
    '''
    ### returns: 
    a 3 int array, with the corresponding scores for each route
    '''
    scores = np.zeros((3,), np.int16)
    nextSteps = findNextSteps(pos, vel)
    nextVelocities = findNextVelocities(vel)

    steps = np.copy(lastSteps)
    steps = updateLastSteps(steps, pos)
    
    # think as if the agent took
    x = np.int16(pos[0])
    y = np.int16(pos[1])
    

    keep = grid[x, y]
    grid[x, y] = AGENT_CODE

    # check for each one
    for i in np.arange(3, dtype= np.int16):
        if acollision(grid, steps, nextSteps[i, :]) == 0:
            scores[i] += 1 + calculateRoute(grid, steps, nextSteps[i, :], nextVelocities[i, :] * 2, depth)


    grid[x, y] = keep
    return scores

@njit
def findIndecies(scores:np.ndarray, val):
    indexes = np.zeros (2, np.int16)
    index=0
    for i in np.arange(len(scores)):
        if scores[i] == val:
            indexes[index] = i
            index+=1
    return indexes

@njit
def pickFromIndecies(indecies:np.ndarray):
    length = len(indecies) - 1
    x = random.randint(0, length)
    return indecies[x]

class Agent(Snake):
    lastChoice = STRAIGHT

    def __init__(self, color, sid, x = -1, y = -1):
        super().__init__(color, sid, x, y)


    def update_velocity(self):
        choices = bestChoice(grid, 
            np.copy(self.lastSteps), 
            np.copy(self.pos), 
            np.copy(self.vel)) 
        choice = np.argmax(choices)

        maxs = np.max(choices)
        
        x, y = self.pos

        if len(choices[choices == maxs]) == 3:
            if maxs == NUM_OF_NODES:
                choice = STRAIGHT
            else:
                choice = self.lastChoice

        elif len(choices[choices == maxs]) == 2:
            indecies = findIndecies(choices, maxs)
            choice = pickFromIndecies(indecies)
        
        self.lastChoice = choice
        
        # if the velocitie's y is positive
        # then pick the opposite from his choice, to fix a bug  
        if y > WINDOW_HEIGHT - WINDOW_BORDER or self.vel[1] > 0:
            choice = 3 - (choice + 1)
        
        print(choices, f'choice = {CHOICES[choice]}')
        
        if choice == LEFT:
            self.goLeft()
        elif choice == RIGHT:
            self.goRight()
        else: # if choice == STRAIGHT
            self.angle = 0
        # rotate and normalize
        super().update_velocity()

if __name__ == '__main__':
    pass

