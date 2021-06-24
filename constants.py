import numpy as np



# colors
DARKGREY = (59, 59, 64)
HEAD_COLOR = (254, 255, 1)

# color array for the snakes:
COLORS_ARRAY = np.array([
    DARKGREY,
    [255, 0, 0],
    [0, 255, 0],
    [128, 0, 128]
])

WINDOW_WIDTH: np.int16 = 750
WINDOW_HEIGHT: np.int16 = 600
ADDED_WALL : np.int16 = 150
# used by the generate function, designed to limit the start position of a snake 
WINDOW_BORDER: np.int16 = int((WINDOW_HEIGHT/ WINDOW_WIDTH) * 300)
WINDOW_SIZE = (WINDOW_WIDTH + ADDED_WALL, WINDOW_HEIGHT)

RADIUS: np.int16 = 5

HORIZONTAL_VELOCITY: np.int16 = 3
VERTICAL_VELOCITY: np.int16 = 100
BETA: np.float32 = np.deg2rad(10)
SPEED = 4.5
DRAW_SAFETY_CONST = 2


FPS = 60
AMOUNT_OF_STEPS = 5

# agent code is temporary
AGENT_CODE = 6
AGENT_DEPTH = 3
NUM_OF_NODES = sum([3 ** i for i in range(AGENT_DEPTH + 1)])

# agent choices index
LEFT = 0
STRAIGHT = 1
RIGHT = 2
CHOICES = ['left', 'straight', 'right']