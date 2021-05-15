from numpy.lib.function_base import average
import pygame
import numpy as np


screen = None
BLACK = pygame.Color("black")
WHITE = pygame.Color("white")
GREY = pygame.Color("grey")


def init(surface):
    global screen
    screen = surface


class Cube():
    def __init__(self, center_pos, s):
        self.s = s
        if len(center_pos) < 3:
            center_pos = center_pos + (0,)
        self.c = np.array(center_pos)
        self.diag = np.sqrt(3*s**2)
        self.points = np.array([
            (self.c + ( self.s/2,  self.s/2,  self.s/2)),
            (self.c + ( self.s/2,  self.s/2, -self.s/2)),
            (self.c + ( self.s/2, -self.s/2, -self.s/2)),
            (self.c + ( self.s/2, -self.s/2,  self.s/2)),
            (self.c + (-self.s/2,  self.s/2,  self.s/2)),
            (self.c + (-self.s/2,  self.s/2, -self.s/2)),
            (self.c + (-self.s/2, -self.s/2, -self.s/2)),
            (self.c + (-self.s/2, -self.s/2,  self.s/2)),
        ])

    def draw(self, draw_face=False):
        projected_points = [p[:2] for p in self.points]
        z_avg1 = np.average(self.points[:4][:,2])
        color1 = ((z_avg1+self.s/2)*225/self.s,)*3

        z_avg2 = np.average(self.points[4:][:,2])
        color2 = ((z_avg2+self.s/2)*225/self.s,)*3
        if z_avg1 < 0:
            if draw_face:
                pygame.draw.polygon(screen, color1, projected_points[:4])
            for p in projected_points[:4]:
                pygame.draw.circle(screen, GREY, p, self.s//20) 
        if z_avg2 < 0:
            if draw_face:
                pygame.draw.polygon(screen, color2, projected_points[4:])
            for p in projected_points[4:]:
                pygame.draw.circle(screen, GREY, p, self.s//20)       

        pygame.draw.lines(screen, GREY, True, projected_points[:4])
        pygame.draw.lines(screen, GREY, True, projected_points[4:])
        pygame.draw.lines(screen, GREY, True, projected_points[:4:3] + projected_points[4::3][::-1])
        pygame.draw.lines(screen, GREY, True, projected_points[1:3] + projected_points[5:7][::-1])

        if z_avg1 >= 0:
            if draw_face:
                pygame.draw.polygon(screen, color1, projected_points[:4])
            for p in projected_points[:4]:
                pygame.draw.circle(screen, GREY, p, self.s//20)
        if z_avg2 >= 0:
            if draw_face:
                pygame.draw.polygon(screen, color2, projected_points[4:])
            for p in projected_points[4:]:
                pygame.draw.circle(screen, GREY, p, self.s//20)
       

    
    def rotate(self, pitch=0, roll=0, yaw=0):
        if pitch:
            theta = np.deg2rad(-pitch)
            r_mat = np.array([
                [1, 0, 0], 
                [0, np.cos(theta), -np.sin(theta)],
                [0, np.sin(theta), np.cos(theta)]
            ])
            self.points = np.array([self.c - np.matmul(r_mat, (self.c - p).T) for p in self.points])
        if roll:
            theta = np.deg2rad(-roll)
            r_mat = np.array([
                [np.cos(theta), -np.sin(theta), 0], 
                [np.sin(theta), np.cos(theta), 0],
                [0, 0, 1]
            ])
            self.points = np.array([self.c - np.matmul(r_mat, (self.c - p).T) for p in self.points])
        if yaw:
            theta = np.deg2rad(-yaw)
            r_mat = np.array([
                [np.cos(theta), 0, np.sin(theta)], 
                [0, 1, 0],
                [-np.sin(theta), 0, np.cos(theta)]
            ])
            self.points = np.array([self.c - np.matmul(r_mat, (self.c - p).T) for p in self.points])


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