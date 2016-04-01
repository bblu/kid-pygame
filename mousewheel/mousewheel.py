import math
import pygame, sys
from pygame.locals import *

class Vec2d(object):
    """2d vector class, supports vector and scalar operators"""
    __slots__ = ['x', 'y']
 
    def __init__(self, x_or_pair, y = None):
        if y == None:
            self.x = x_or_pair[0]
            self.y = x_or_pair[1]
        else:
            self.x = x_or_pair
            self.y = y
#Addition
    def __add__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x + other.x, self.y + other.y)
#Subtraction
    def __sub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x - other.x, self.y - other.y)
#rotate
    def rotate(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        self.x = x
        self.y = y

# set up the window
screen = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption('Drawing')

# set up the colors
BLACK = (  0,   0,   0)
GRAY  = (192, 192, 192)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

UP = 'up'
DOWN = 'down'

abcIndex=0
abcString = 'ABCDEFGHIGKLMNOPQRSTUVWXYXZ'
curString = '?'
curFont = pygame.font.SysFont('freemono',128)
    
class CircleText:
    pos = Vec2d(0,0)
    rad = 10
    text= ''
    font=pygame.font.SysFont('freemono',128)
    def __init__(self,text,font):
        self.text = text
        self.font = font
    def setPos(ref):
        pos = ref
    def render(sur,idx):
        
        

def showChar(surface,index):
    global curFont,abcString,curString
    index = index%25
    curString = abcString[index-3:index+2]
    textobj = curFont.render(curString,1,BLUE)
    objTest = pygame.transform.rotate(textobj,index)
    surface.blit(objTest,(0,0))
    
def rollWheel(button):
    global abcIndex
    if button == 4:
       abcIndex+=1
    elif button == 5 :
        abcIndex-=1

pygame.init()
# run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            rollWheel(event.button)
            screen.fill(GRAY)
            showChar(screen,abcIndex)
    pygame.display.update()
