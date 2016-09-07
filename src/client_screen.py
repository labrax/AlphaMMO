# -*- coding: utf-8 -*-

import pdb

import pygame
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE

from alpha_defines import START_RESOLUTION, SPRITE_LEN, GRID_SIZE, GRID_MEMORY_SIZE, gray, transparent


class ClientScreen:
    def __init__(self):
        # start screen
        self.current_size = START_RESOLUTION
        self.screen = pygame.display.set_mode(self.current_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
        pygame.display.flip()

        # initializes grid memory
        self.tiled_area = pygame.Surface((GRID_SIZE[0] * SPRITE_LEN, GRID_SIZE[1] * SPRITE_LEN), pygame.SRCALPHA)

    def render(self, client_states):
        # prepare range to fit screen
        ## get the smallest side fitting
        tiles_at_x = self.current_size[0] / SPRITE_LEN
        tiles_at_y = self.current_size[1] / SPRITE_LEN
        tiles = tiles_at_x
        if tiles_at_y < tiles_at_x:
            tiles = tiles_at_y
        ## get the position
        size_x = tiles * SPRITE_LEN
        size_y = tiles * SPRITE_LEN
        pos_x = self.current_size[0] / 2 - size_x / 2
        pos_y = self.current_size[1] / 2 - size_y / 2

        # clear screen
        self.screen.fill(gray)

        # clear area for 'main game tiled area'
        self.tiled_area.fill(transparent)

        # draw into 'main game tiled area'
        for i in range(int((GRID_MEMORY_SIZE[1] - GRID_SIZE[1]) / 2),
                       int(GRID_MEMORY_SIZE[1] - (GRID_MEMORY_SIZE[1] - GRID_SIZE[1]) / 2)):
            for j in range(int((GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) / 2),
                           int(GRID_MEMORY_SIZE[0] - (GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) / 2)):
                for elem in client_states.tiled_memory[i][j]:
                    self.tiled_area.blit(elem, ((j - (GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) / 2) * SPRITE_LEN,
                                            (i - (GRID_MEMORY_SIZE[1] - GRID_SIZE[1]) / 2) * SPRITE_LEN))

        if client_states.player_character.sprite is not None:
            self.tiled_area.blit(client_states.player_character.sprite, ((int(GRID_SIZE[0] / 2) + 1 - (GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) / 2) * SPRITE_LEN,
                                            (int(GRID_SIZE[1] / 2) + 1 - (GRID_MEMORY_SIZE[1] - GRID_SIZE[1]) / 2) * SPRITE_LEN))

        # draw to screen
        self.screen.blit(pygame.transform.scale(self.tiled_area, (int(size_x), int(size_y))), (pos_x, pos_y))

        # flip buffer
        pygame.display.flip()

    def resize(self, event):
        self.current_size = event.dict['size']
        self.screen = pygame.display.set_mode(self.current_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
