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
        else:
            return Vec2d(self.x - other, self.y - other)
#rotate
    def rotate(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        #print ('org %d=(%d,%d)')%(angle_degrees,x,y)
        self.x = x
        self.y = y

# set up the window

srcW = 640
srcH = 480
cenPos = Vec2d(srcW/2,srcH/2)
screen = pygame.display.set_mode((640, 480), 0, 32)
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
abcStr = 'ABCDEFGHIGKLMNOPQRSTUVWXYXZ'
pygame.init()
strFont = pygame.font.get_default_font();
curFont = pygame.font.SysFont(strFont,128)
    
class CircleText:
    pos = Vec2d(0.0,0.0)
    rad = 10.0
    text= ''
    dAngle=0.0
    font=pygame.font.SysFont('freemono',32)
    def __init__(self,text,font):
        self.text = text
        self.font = font
        self.dAngle = 360.0/len(text)
        print ('%f')%self.dAngle
        
    def setPos(self, p):
        self.pos = p
    def setRad(self, r):
        self.rad = r
    def render(self, sur, idx):
        start = -1*(self.dAngle*idx)
        vr = Vec2d(0,-self.rad)
        #print ('index=%d a=%f start = %d')%(idx,self.dAngle,start)
        vr.rotate(start)
        rot = start
        for abc in abcStr:
            lbl = self.font.render(abc,1,BLUE)
            obj = pygame.transform.rotate(lbl,rot)
            cur = vr+self.pos
            sur.blit(obj,(cur.x,cur.y))
            vr.rotate(self.dAngle)
            rot -= self.dAngle

def showChar(surface,index):
    global curFont,abcString,curString
    index = index%25
    curString = abcStr[index]
    textobj = curFont.render(curString,1,BLUE)
    surface.blit(textobj,(cenPos.x,cenPos.y))
    
def rollWheel(button):
    global abcIndex
    if button == 4:
       abcIndex+=1
    elif button == 5 :
        abcIndex-=1

abcCir = CircleText(abcStr,curFont)
abcCir.setPos(cenPos-20)
abcCir.setRad(cenPos.y)
# run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            rollWheel(event.button)
            screen.fill(GRAY)
            abcCir.render(screen,abcIndex)
            showChar(screen,abcIndex)
    pygame.display.update()
