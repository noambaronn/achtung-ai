import pygame
from time import sleep
from math import radians, sin, cos, sqrt
import keyboard
import numpy as np
from numba import njit
import random

from constants import *
from screen_globals import *
from snake import *

class Player(Snake):
    
    def __init__(self, color, x, y, sid, left, right):
        super().__init__(color, x, y, sid)
        self.left = left
        self.right = right
        
    def update_velocity(self):
        if keyboard.is_pressed(self.left):
            self.goLeft()
        elif keyboard.is_pressed(self.right):
            self.goRight()
        else:
            self.angle = 0
        # rotate and normalize
        super().update_velocity()
        
