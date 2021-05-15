import pygame
import numpy as np

screen = None
BLACK = pygame.Color("black")
WHITE = pygame.Color("white")

def init(surface):
    global screen
    screen = surface


class Prism():
    def __init__(self, f1, f2):
        if not (len(f1.points) == len(f2.points)):
            raise IndexError
        self.face1 = f1
        self.face2 = f2

    def draw(self):
        self.face2.draw()
        self.face1.draw()
        for i in range(len(self.face1.points)):
            p1x,p1y = self.face1.points[i]
            p2x,p2y = self.face2.points[i]
            pygame.draw.line(screen, WHITE, (p1x,p1y), (p2x,p2y), width=2)

    def rotate(self, deg):
        self.face1.rotate(deg)
        self.face2.rotate(deg)
        

class Rect():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.centre = (x+w/2,y+h/2)
        self.points = [(x,y), (x+w,y), (x+w,y+h), (x,y+h)]
    
    def draw(self):
        pygame.draw.lines(screen, WHITE, True, self.points, width=2)
        for p in self.points:
            pygame.draw.circle(screen, WHITE, p, radius=min(self.w,self.h)//20)

    def rotate(self, deg):
        x0,y0 = self.centre
        for i in range(len(self.points)):
            x1,y1 = self.points[i]
            r = np.sqrt((x1-x0)**2 + (y1-y0)**2)
            phi = np.arctan2((y1-y0),(x1-x0)) + np.deg2rad(deg)
            self.points[i] = (x0 + r*np.cos(phi), y0 + r*np.sin(phi))