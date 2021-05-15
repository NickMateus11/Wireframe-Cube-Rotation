import pygame

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
    cube.rotate(0, 30, 60)

    p = r = y = 0
    max_rot = 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if pygame.key.get_pressed()[pygame.K_RCTRL]:
                        r += -1
                    else:
                        y += -1
                if event.key == pygame.K_RIGHT:
                    if pygame.key.get_pressed()[pygame.K_RCTRL]:
                        r += 1
                    else:
                        y += 1
                if event.key == pygame.K_UP:
                    p += 1
                if event.key == pygame.K_DOWN:
                    p += -1

        if abs(p) > max_rot:
            p = max_rot if p>0 else -max_rot
        if abs(r) > max_rot:
            r = max_rot if r>0 else -max_rot
        if abs(y) > max_rot:
            y = max_rot if y>0 else -max_rot

        screen.fill(BLACK)

        cube.draw()
        cube.rotate(p,r,y)

        pygame.display.flip()
        clock.tick(framerate)


if __name__ == "__main__":
    main()
