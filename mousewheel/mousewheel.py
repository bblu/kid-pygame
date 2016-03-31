import pygame, sys
from pygame.locals import *

pygame.init()

# set up the window
DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption('Drawing')

# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

UP = 'up'
DOWN = 'down'

abcIndex=0
abcString = '?'
def showChar(index):
    global abcString
    abcString = 'A'
    
def rollWheel(direction):
    global abcIndex
    if direction == UP:
       abcIndex+=1
    else :
        abcIndex-=1


# run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            print ('butn=%d')%event.button
            pressed_array = pygame.mouse.get_pressed()
            for index in range(len(pressed_array)):
                if pressed_array[index]:
                    print ('%d')%index
            rollWheel(UP)
            
    pygame.display.update()
