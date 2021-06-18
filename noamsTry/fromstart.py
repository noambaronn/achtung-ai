import pygame
# constants
#                   R G B
BACKGROUND_COLOR = (0,0,0)
(WIDTH, HEIGHT) = (900 , 640)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
RADIUS=4
FPS=60

pygame.display.set_caption('Achtung game')
x1= 150
y1= 150
j1= 400
j2= 350
def draw():
    global x1  
    global y1 
    global j1
    global j2
    pygame. draw. circle(screen, (50,250,90), (x1, y1), RADIUS, 0)
    x1= x1+1
    y1= y1+1
    pygame. draw. circle(screen, (255, 0, 255), (j1, j2), RADIUS, 0)
    j1+=1
    j2+=1
    pygame. draw. circle(screen, (255, 0, 255), (j1, j2), RADIUS, 0)
    pygame.display.update()

def main():
    clock= pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                 
                 
        draw()  

    pygame.display.flip()
    pygame.quit()

if __name__ ==  "__main__":
    main()

