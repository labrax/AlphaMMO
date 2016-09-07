# -*- coding: utf-8 -*-

black = (0, 0, 0)
gray = (104, 104, 104)
white = (255, 255, 255)
transparent = (0, 0, 0, 0)

ASSETS_DIR = 'assets/'
SPRITE_LEN = 16
GRID_SIZE = (11, 11)
GRID_MEMORY_SIZE = (13, 13)
assert(int((GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) % 2 ) == 0)
assert(int((GRID_MEMORY_SIZE[1] - GRID_SIZE[1]) % 2 ) == 0)

START_RESOLUTION = (4 * SPRITE_LEN * GRID_SIZE[0], 4 * SPRITE_LEN * GRID_SIZE[1])

FPS = 60