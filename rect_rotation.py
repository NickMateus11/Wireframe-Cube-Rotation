import pygame

import polygon
from polygon import Rect, Prism


w, h = 800, 600
pygame.init()
screen = pygame.display.set_mode((w, h))

clock = pygame.time.Clock()
framerate = 30

BLACK = pygame.Color("black")
WHITE = pygame.Color("white")


polygon.init(screen)


def main():

    rect_width = rect_height = 200
    rect1 = Rect(w/2-rect_width/2, h/2-rect_height/2, rect_width, rect_height)
    rect2 = Rect(w/2-rect_width/4, h/2-6*rect_height/10, rect_width, rect_height)
    box = Prism(rect1,rect2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        box.draw()
        box.rotate(2)

        pygame.display.flip()
        clock.tick(framerate)


if __name__ == "__main__":
    main()
