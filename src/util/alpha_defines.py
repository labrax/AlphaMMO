# -*- coding: utf-8 -*-

black = (0, 0, 0)
gray = (104, 104, 104)
white = (255, 255, 255)
transparent = (0, 0, 0, 0)

ASSETS_DIR = 'assets/'
SPRITE_LEN = 16
GRID_SIZE = (11, 11)
GRID_MEMORY_SIZE = (15, 15)
assert(int((GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) % 2) == 0)
assert(int((GRID_MEMORY_SIZE[1] - GRID_SIZE[1]) % 2) == 0)

START_RESOLUTION = (4 * SPRITE_LEN * GRID_SIZE[0], 4 * SPRITE_LEN * GRID_SIZE[1])

FPS = 60
version = 'almost 0.00001a'

FONT_FILE = '04B_03__.TTF'
FONT_SIZE = 32
FONT_COLOR = (0, 0, 0)

DRAW_PLAYERS_NAME = True

SERVER_IP = '127.0.0.1'
SERVER_PORT = 1337
SOCKET_BUFFER = 4096
SOCKET_TIMEOUT = 1
