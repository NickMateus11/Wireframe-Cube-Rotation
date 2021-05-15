import pygame
import numpy as np

import shapes
from shapes import Rect, Prism, Cube


w, h = 800, 600
pygame.init()
screen = pygame.display.set_mode((w, h))

clock = pygame.time.Clock()
framerate = 30

BLACK = pygame.Color("black")
WHITE = pygame.Color("white")


shapes.init(screen)


def main():

    # rect_width = rect_height = 200
    # rect1 = Rect(w/2-rect_width/2, h/2-rect_height/2, rect_width, rect_height)
    # rect2 = Rect(w/2-rect_width/4, h/2-6*rect_height/10, rect_width, rect_height)
    # box = Prism(rect1,rect2)

    s = 200
    cube = Cube((w/2,h/2,0), s)
    cube.rotate(0, 30, 30)

    p = r = y = 0
    max_rot = 15
    rot_step = 0.5
    damping = 0.95
    eps = 0.05

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        mouse_rel = pygame.mouse.get_rel()

        if pygame.mouse.get_pressed()[0]:
            if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                if (mouse_rel[0] + mouse_rel[1]) > 0:
                    r = rot_step * -max(abs(mouse_rel[0]), abs(mouse_rel[1])) * 0.5
                else:
                    r = rot_step * max(abs(mouse_rel[0]), abs(mouse_rel[1])) * 0.5
            else:
                y = rot_step * -mouse_rel[0] * 0.5
                p = rot_step * mouse_rel[1] * 0.5

        if keys[pygame.K_LEFT]:
            if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL] :
                r += -rot_step
            else:
                y += -rot_step
        if keys[pygame.K_RIGHT]:
            if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                r += rot_step
            else:
                y += rot_step
        if keys[pygame.K_UP]:
            p += rot_step
        if keys[pygame.K_DOWN]:
            p += -rot_step

        p *= damping
        r *= damping
        y *= damping

        if abs(p) < eps: p = 0
        if abs(r) < eps: r = 0
        if abs(y) < eps: y = 0

        if abs(p) > max_rot:
            p = max_rot if p>0 else -max_rot
        if abs(r) > max_rot:
            r = max_rot if r>0 else -max_rot
        if abs(y) > max_rot:
            y = max_rot if y>0 else -max_rot

        screen.fill(BLACK)

        cube.draw(draw_face=False)
        cube.rotate(p,r,y)

        pygame.display.flip()
        clock.tick(framerate)


if __name__ == "__main__":
    main()
