import math,os
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

srcW = 800
srcH = 800
cenPos = Vec2d(srcW/2,srcH/2)-40


# set up the colors
BLACK = (  0,   0,   0)
GRAY  = (192, 192, 192)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
LTGREEN=(  0, 192,   0)
BLUE  = (  0,   0, 255)

MS_LEFT = 1
MS_RIGHT= 3
MS_DOWN = 4
MS_UP   = 5

curIndex = 0
oldIndex = -1
abcStr = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
numStr = '0123456789'
clkStr = ''
objStr = abcStr
pygame.init()
screen = pygame.display.set_mode((srcW, srcH), 0, 24)
pygame.display.set_caption('MouseWheelGame')
strFont = pygame.font.get_default_font();
curFont = pygame.font.SysFont(strFont,150)
bigFont = pygame.font.SysFont(strFont,256+128)

class CircleText:
    pos = Vec2d(0.0,0.0)
    rad = 10.0
    text= ''
    dAngle=0.0
    oldIndex=0
    font=pygame.font.SysFont('freemono',32)
    def __init__(self,txt,font):
        self.font = font
        self.setText(txt)
        
    def setText(self,txt):
        self.text = txt
        self.dAngle = 360.0/len(txt)
        print txt
        #print ('len=%d angle=%f')%(len(txt),self.dAngle)
    def getText(self):
        return self.text
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
        for abc in self.text:
            lbl = self.font.render(abc,2,GRAY)
            obj = pygame.transform.rotate(lbl,-rot)
            cur = vr+self.pos
            sur.blit(obj,(cur.x,cur.y))
            vr.rotate(self.dAngle)
            #print ('%s rot=%f')%(abc,rot)
            rot += self.dAngle
            
class charSprite(pygame.sprite.Sprite):
    def __init__(self,imf):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imf).convert_alpha()
        #self.rect = self.image.get_rect()
        
    def load(self,imf,width,height):
        imf=0    

def genIndex(button):
    global curIndex
    #print 'Btn=%d'%button
    if button==32 or button == MS_UP or button ==MS_LEFT or button==274 or button ==275:
       curIndex+=1
    elif button == MS_DOWN or button ==MS_RIGHT or button ==273 or button==276:
        curIndex-=1
def isNumKey(key):
    return (event.key>=48 and event.key <= 57) or (event.key>=256 and event.key <= 265) 
def isChrKey(key):
    return (event.key>=97 and event.key <= 122)

def showChar(surface,index):
    global bigFont,curFont,objStr
    index = index%len(objStr)
    print 'idx=%d'%index
    curString = objStr[index]
    textUpper = bigFont.render(curString,1,GREEN)    
    surface.blit(textUpper,(cenPos.x-55,150))
    if len(objStr)> 12:
        textLower = curFont.render(curString.lower(),1,LTGREEN)
        surface.blit(textLower,(cenPos.x+150,srcH/2-100))
    return curString

resMap={'1':'1'}

def ListFiles(dirPath):   
    fileList = []  
    for root, dirs, files in os.walk(dirPath):
        for fileObj in files:   
            fileList.append(os.path.join(root, fileObj))   
    return fileList 
resFiles = ListFiles('./res')

for f in resFiles:
    resMap[f[6]]=f


def showPict(surface,char):
    global resMap
    tarfile = resMap[char.lower()]
    print tarfile
    csp = charSprite(tarfile)
    surface.blit(csp.image,(cenPos.x-80,cenPos.y+50,150,150))

abcCir = CircleText(abcStr,curFont)
abcCir.setPos(cenPos)
abcCir.setRad(cenPos.y-24)
clock = pygame.time.Clock()

def chMode(string=None):
    global abcCir,objStr,numStr,oldIndex
    print string
    if string == objStr:
        return
    elif string != None:
        objStr = string
    else:
        print len(objStr)
        if len(objStr)>20:
            objStr = numStr
        else:
            objStr = abcStr
    abcCir.setText(objStr)
    oldIndex=-1

# run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            genIndex(event.button)            
        elif event.type == KEYDOWN:
            if isNumKey(event.key):
                chMode(numStr)
                curIndex =event.key - 48
                if curIndex>200:
                    curIndex -= 256-48
            elif isChrKey(event.key):
                chMode(abcStr)
                curIndex = event.key-97
            elif event.key == 304:
                chMode()
            else:
                genIndex(event.key)
    if(curIndex!=oldIndex):
        oldIndex = curIndex
        screen.fill(BLACK)
        abcCir.render(screen,curIndex)
        char = showChar(screen,curIndex)
        showPict(screen,char)
    pygame.display.flip()
    clock.tick(10)
