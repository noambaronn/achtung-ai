import numpy as np
from numba import njit

from constants import *
from screen_globals import *
from snake import *

def bestChoice(grid: np.ndarray, steps: np.ndarray, pos: np.ndarray, scores = np.zeros((3,), np.int16)):
    '''
    ### returns: 
    a 3 int array, with the corresponding scores for each route
    '''
    x, y = pos
    
# agent code is temporary
AGENT_CODE = 6

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
    left[0] += pos[0]
    left[1] += pos[1]

    right = arotate(vel, -BETA)
    right[0] += pos[0]
    right[1] += pos[1]
    
    straight = vel
    straight[0] += pos[0]
    straight[1] += pos[1]

    nextSteps = np.empty((3, 2), np.float32)
    nextSteps[0] = left
    nextSteps[1] = straight
    nextSteps[2] = right

    return nextSteps


@njit
def findNextVelocities(vel: np.mdarray):
    left = np.zeros_like(vel)
    right = np.zeros_like(vel)
    straight = np.zeros_like(vel)

    left = arotate(vel, BETA)
    straight = vel   
    right = arotate(vel, -BETA)
    
    nextVelocites = np.empty((3, 2), np.float32)
    nextVelocites[0] = left
    nextVelocites[1] = straight
    nextVelocites[2] = right

    return nextVelocites

def calculateRoute(
    grid: np.ndarray,
    lastSteps: np.ndarray,
    pos: np.ndarray,
    vel: np.ndarray,
    depth = 4):
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
    score = 0
    nextSteps = findNextSteps(pos, vel)
    nextVelocities = findNextVelocities(vel)


    steps = np.copy(lastSteps)
    steps = updateLastSteps(steps, pos)
    
    # think as if the agent took
    x, y = pos

    keep = grid[x, y]
    grid[x, y] = AGENT_CODE

    # check for each one
    for i in np.arange(3, dtype= np.int16):
        if collision(grid, steps, nextSteps[i]) == 0:
        
            score += calculateRoute(grid, steps, nextSteps[i], nextVelocities[i],  depth - 1)


    grid[x, y] = keep
        
    
    



class Agent(Snake):
    def __init__(self, color, x, y, sid):
        super().__init__(color, x, y, sid)

if __name__ == '__main__':
    print(findNextSteps(np.array([50, 50], np.float32), np.array([1, 1], np.float32)))