# -*- coding: utf-8 -*-

import os
import pdb

import pygame
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE

from alpha_defines import ASSETS_DIR
from util.resource_loader import AlphaResourceLoader, AlphaSprite, SPRITE_LEN

black = (0, 0, 0)

TILE = 0
MASK = 1000
OBJECT = 2000

CHARACTER = 10000
CHARACTER_DETAIL = 15000


RAW_CHAR = 10000

HELMET = 2100
ARMOR = 2200
TROUSERS = 2300
BOOTS = 2350

SHIELD = 2400
WAND = 2500
CLUB = 2600
SWORD = 2700
BOW = 2800
# {('roguelikeChar_transparent.png', 42, 6): 2700, ('roguelikeChar_transparent.png', 28, 0): 2100, ('roguelikeChar_transparent.png', 23, 0): 2100, ('roguelikeChar_transparent.png', 42, 4): 2600, ('roguelikeChar_transparent.png', 0, 0): 10000, ('roguelikeChar_transparent.png', 47, 0): 2600, ('roguelikeChar_transparent.png', 31, 8): 2100, ('roguelikeChar_transparent.png', 17, 9): 2200, ('roguelikeChar_transparent.png', 33, 0): 2400, ('roguelikeChar_transparent.png', 46, 5): 2600, ('roguelikeChar_transparent.png', 52, 0): 2800, ('roguelikeChar_transparent.png', 6, 0): 2200, ('roguelikeChar_transparent.png', 0, 3): 10000, ('roguelikeChar_transparent.png', 22, 11): 2100, ('roguelikeChar_transparent.png', 53, 4): 2800, ('roguelikeChar_transparent.png', 51, 9): 2600, ('roguelikeChar_transparent.png', 26, 7): 2100, ('roguelikeChar_transparent.png', 42, 0): 2500, ('roguelikeChar_transparent.png', 4, 9): 2350, ('roguelikeChar_transparent.png', 40, 8): 2400, ('roguelikeChar_transparent.png', 46, 3): 2500, ('roguelikeChar_transparent.png', 46, 9): 2700, ('roguelikeChar_transparent.png', 19, 0): 2100, ('roguelikeChar_transparent.png', 3, 0): 2350}

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((160, 160), HWSURFACE|DOUBLEBUF|RESIZABLE)
    pygame.display.flip()

    c = pygame.time.Clock()

    FILES_LISTDIR = [i for i in os.listdir(ASSETS_DIR)]
    FILES = list()
    for i in FILES_LISTDIR:
        if 'Char' in i:
            FILES.append(i)
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
                    if event.key == pygame.K_h:
                        DATA[(i, x, y)] = HELMET
                    if event.key == pygame.K_a:
                        DATA[(i, x, y)] = ARMOR
                    if event.key == pygame.K_t:
                        DATA[(i, x, y)] = TROUSERS
                    if event.key == pygame.K_s:
                        DATA[(i, x, y)] = SHIELD
                    if event.key == pygame.K_w:
                        DATA[(i, x, y)] = WAND
                    if event.key == pygame.K_c:
                        DATA[(i, x, y)] = CLUB
                    if event.key == pygame.K_e:
                        DATA[(i, x, y)] = SWORD
                    if event.key == pygame.K_b:
                        DATA[(i, x, y)] = BOW
                    if event.key == pygame.K_r:
                        DATA[(i, x, y)] = RAW_CHAR
                    if event.key == pygame.K_y:
                        DATA[(i, x, y)] = BOOTS
                    # if event.key == pygame.K_t:
                    #     DATA[(i, x, y)] = TILE # (i, x, y)
                    #     x += 1
                    #     if x == MAX_X:
                    #         x = 0
                    #         y += 1
                    # if event.key == pygame.K_m:
                    #     DATA[(i, x, y)] = MASK # (i, x, y)
                    #     x += 1
                    #     if x == MAX_X:
                    #         x = 0
                    #         y += 1
                    # if event.key == pygame.K_o:
                    #     DATA[(i, x, y)] = OBJECT
                    #     x += 1
                    #     if x == MAX_X:
                    #         x = 0
                    #         y += 1
                    # if event.key == pygame.K_c:
                    #     DATA[(i, x, y)] = CHARACTER
                    #     x += 1
                    #     if x == MAX_X:
                    #         x = 0
                    #         y += 1
                    # if event.key == pygame.K_d:
                    #     DATA[(i, x, y)] = CHARACTER_DETAIL
                    #     x += 1
                    #     if x == MAX_X:
                    #         x = 0
                    #         y += 1
                    if event.key == pygame.K_ESCAPE:
                        pdb.set_trace()
                    # if event.key == pygame.K_p:
                    #     print("CURRENT FILE: " + i)
                    #     file -= 1
                    # if event.key == pygame.K_n:
                    #     print("CURRENT FILE: " + i)
                    #     file += 1
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