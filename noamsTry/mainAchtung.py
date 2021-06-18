import pygame
from pygame.math import Vector2
from math import radians, sin, cos, sqrt
import keyboard
import numpy as np


pygame.init()
WIDTH = 800
HEIGHT = 450
SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SIZE)
BETA = radians(0.1)


grid = np.ndarray(shape=(WIDTH, HEIGHT),
                  dtype=np.uint8)

class Point:
    isBumpped = False

    def __init__(self, currdirection, pos: Vector2):
        self.currdirection = currdirection
        self.pos = pos


class Snake:
    #defaults
    RADIUS = 4
    SPEED = 0.055
    angle = BETA
    isAlive = True
    pos: np.ndarray
    def __init__(self, color, velocity: Vector2, pos: Vector2, cleft: str, cright: str):
        self.color = color
        self.velocity = velocity
        self.pos = pos
        self.cleft = cleft
        self.cright = cright
        self.normalize()


    def update(self):
        # rotation:
        self.collision()
        self.rotate()
        self.pos += self.velocity.xy

    def draw(self, screen: pygame.Surface):
        if self.isAlive:
            pygame.draw.circle(screen, self.color, self.pos, self.RADIUS)

    def rotate(self):
        # x2 = cosβx1 − sinβy1
        # y2 = sinβx1 + cosβy1
        (x1, y1) = self.velocity
        x2 = cos(self.angle) * x1 - sin(self.angle) * y1
        y2 = sin(self.angle) * x1 + cos(self.angle) * y1
        self.velocity = Vector2(x2, y2)

    def normalize(self):
        # L = sqrt( (x1^2) + (y1^2) )
        (x1, y1) = self.velocity
        l = sqrt((x1 ** 2) + (y1 ** 2))
        for i in range(2):
            self.velocity[i] = (self.velocity[i]) * (self.SPEED / l)

    def collision(self):
        (x,y) = self.pos
        if  x + self.RADIUS >= WIDTH or\
            y + self.RADIUS >= HEIGHT or\
            x - self.RADIUS <= 0 or\
            y - self.RADIUS <= 0:
            self.isAlive = False

            pygame.quit()

# fill the screen with black
# ~~~~~~~~~~~R~~G~~B~~~
screen.fill((0, 0, 0))
players = []


if __name__ == '__main__':
    players.append(Snake(color= (247, 138, 3),
                     velocity= Vector2(0.01, 0.01),
                     pos=Vector2(WIDTH // 8, HEIGHT // 8),
                     cleft= 'A',
                     cright= 'D'))

    players.append(Snake(color= (163, 155, 237),
                     velocity= Vector2(0.01, 0.01),
                     pos=Vector2(WIDTH // 4, HEIGHT // 2),
                     cleft= 'left',
                     cright= 'right'))

    running = True
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



        for i in range(len(players)):
           (players[i].cleft):
                players[i].angle = BETA
            elif keyboard.is_pressed(players[i].cright):
                players[i].angle = -BETA
            else:
                players[i].angle = 0

            # Draw a solid blue circle in the center
            players[i].update()
            players[i].draw(screen)

        # Flip the display
        pygame.display.flip()
    # Done! Time to quit.
    pygame.quit()
