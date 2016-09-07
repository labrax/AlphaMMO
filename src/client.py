#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE
from pygame.locals import QUIT, VIDEORESIZE
import time

from resource_loader import AlphaResourceLoader
from alpha_defines import START_RESOLUTION, FPS, SPRITE_LEN, GRID_SIZE, GRID_MEMORY_SIZE, black, white, gray, transparent

from data_structures import Tile


class AlphaGameClient:
    def __init__(self):
        # resource loader starter
        self.rl = AlphaResourceLoader()

        # initializes display
        self.current_size = START_RESOLUTION
        self.screen = pygame.display.set_mode(self.current_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
        pygame.display.flip()

        # initializes grid memory
        self.tiled_area = pygame.Surface((GRID_SIZE[0] * SPRITE_LEN, GRID_SIZE[1] * SPRITE_LEN), pygame.SRCALPHA)
        self.tiled_memory = [[Tile() for j in range(GRID_MEMORY_SIZE[0])] for i in range(GRID_MEMORY_SIZE[1])]

        # sample for testing
        for i in range(GRID_MEMORY_SIZE[1]):
            for j in range(GRID_MEMORY_SIZE[0]):
                self.tiled_memory[i][j].tile = self.rl.get_sprite('roguelikeDungeon_transparent.png', 16, 15)

        self.tiled_memory[6][6].characters.append(self.rl.get_sprite('roguelikeChar_transparent.png', 0, 8))  # screen center
        self.tiled_memory[6][5].characters.append(self.rl.get_sprite('roguelikeChar_transparent.png', 1, 9))
        self.tiled_memory[2][2].characters.append(self.rl.get_sprite('roguelikeChar_transparent.png', 0, 7))

        self.tiled_memory[2][2].decor_objects.append(self.rl.get_sprite('roguelikeDungeon_transparent.png', 1, 4))
        self.tiled_memory[7][7].decor_objects.append(self.rl.get_sprite('roguelikeDungeon_transparent.png', 1, 4))
        self.tiled_memory[8][8].decor_objects.append(self.rl.get_sprite('roguelikeDungeon_transparent.png', 1, 4))

    def render(self):
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
        for i in range(int((GRID_MEMORY_SIZE[1] - GRID_SIZE[1]) / 2), int(GRID_MEMORY_SIZE[1] - (GRID_MEMORY_SIZE[1] - GRID_SIZE[1]) / 2)):
            for j in range(int((GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) / 2), int(GRID_MEMORY_SIZE[0] - (GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) / 2)):
                for elem in self.tiled_memory[i][j]:
                    self.tiled_area.blit(elem, ((j - (GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) / 2) * SPRITE_LEN, (i - (GRID_MEMORY_SIZE[1] - GRID_SIZE[1]) / 2) * SPRITE_LEN))

        # draw to screen
        self.screen.blit(pygame.transform.scale(self.tiled_area, (int(size_x), int(size_y))), (pos_x, pos_y))

        # flip buffer
        pygame.display.flip()

    def run(self):
        running = True

        old_time = pygame.time.get_ticks()
        while running:
            new_time = pygame.time.get_ticks()
            waited = new_time - old_time
            old_time = new_time
            if waited < 60:
                time.sleep(1.0 / (FPS - waited))

            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    running = False
                if event.type == VIDEORESIZE:
                    self.current_size = event.dict['size']
                    self.screen = pygame.display.set_mode(self.current_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
            self.render()

        pygame.quit()


if __name__ == '__main__':
    gs = AlphaGameClient()
    gs.run()


