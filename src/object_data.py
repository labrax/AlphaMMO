# -*- coding: utf-8 -*-

import pdb
import pygame
import os
from resource_loader import AlphaResourceLoader, AlphaSprite, SPRITE_LEN
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE

from alpha_defines import ASSETS_DIR

black = (0, 0, 0)

TILE = 0
MASK = 1000
OBJECT = 2000


CHARACTER = 10000
CHARACTER_DETAIL = 15000



if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((160, 160), HWSURFACE|DOUBLEBUF|RESIZABLE)
    pygame.display.flip()

    c = pygame.time.Clock()

    FILES = [i for i in os.listdir(ASSETS_DIR)]
    current_id = 1
    DATA = dict()

    rl = AlphaResourceLoader()
    x = 0
    y = 0
    try:
        file = 0

        running = True
        while running:
            i = FILES[file]
            curr = AlphaSprite(file=ASSETS_DIR + i)
            MAX_X, MAX_Y = int(curr.image.get_size()[0] / (SPRITE_LEN + 1)), int(
                curr.image.get_size()[1] / (SPRITE_LEN + 1))
            screen.fill(black)
            img = rl.get_sprite(i, x, y)
            screen.blit(pygame.transform.scale(img, (160, 160)), (0, 0))
            pygame.display.flip()

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x -= 1
                    if event.key == pygame.K_RIGHT:
                        x += 1
                    if event.key == pygame.K_UP:
                        y -= 1
                    if event.key == pygame.K_DOWN:
                        y += 1
                    if event.key == pygame.K_t:
                        DATA[(i, x, y)] = TILE # (i, x, y)
                        x += 1
                        if x == MAX_X:
                            x = 0
                            y += 1
                    if event.key == pygame.K_m:
                        DATA[(i, x, y)] = MASK # (i, x, y)
                        x += 1
                        if x == MAX_X:
                            x = 0
                            y += 1
                    if event.key == pygame.K_o:
                        DATA[(i, x, y)] = OBJECT
                        x += 1
                        if x == MAX_X:
                            x = 0
                            y += 1
                    if event.key == pygame.K_c:
                        DATA[(i, x, y)] = CHARACTER
                        x += 1
                        if x == MAX_X:
                            x = 0
                            y += 1
                    if event.key == pygame.K_d:
                        DATA[(i, x, y)] = CHARACTER_DETAIL
                        x += 1
                        if x == MAX_X:
                            x = 0
                            y += 1
                    if event.key == pygame.K_ESCAPE:
                        pdb.set_trace()
                    if event.key == pygame.K_p:
                        print("CURRENT FILE: " + i)
                        file -= 1
                    if event.key == pygame.K_n:
                        print("CURRENT FILE: " + i)
                        file += 1
                if event.type == pygame.QUIT:
                    running = False
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            if x > MAX_X:
                x = MAX_X
            if y > MAX_Y:
                y = MAX_Y
            if file >= len(FILES):
                file = len(FILES) - 1
            if file < 0:
                file = 0
    except Exception as e:
        print(e)
        print(DATA)
    print(DATA)