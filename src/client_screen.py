# -*- coding: utf-8 -*-

import pdb
import time


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


        ref_movement_x = 0
        ref_movement_y = 0

        # player position if in movement
        if (client_states.player_character.start_movement):
            this_time = time.time()
            diff_x = client_states.player_character.movement[0] - client_states.player_character.pos[0]
            diff_y = client_states.player_character.movement[1] - client_states.player_character.pos[1]

            if diff_x:
                ref_movement_x = -diff_x * (-SPRITE_LEN + client_states.player_character.speed_pixels * (this_time - client_states.player_character.start_movement))
            if diff_y:
                ref_movement_y = -diff_y * (-SPRITE_LEN + client_states.player_character.speed_pixels * (this_time - client_states.player_character.start_movement))

        # clear screen
        self.screen.fill(gray)

        # clear area for 'main game tiled area'
        self.tiled_area.fill(transparent)

        # draw into 'main game tiled area'
        for i in range(int((GRID_MEMORY_SIZE[1] - GRID_SIZE[1]) / 2) - 2,
                       int((GRID_MEMORY_SIZE[1] + GRID_SIZE[1]) / 2) + 2):
            for j in range(int((GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) / 2) - 2,
                           int((GRID_MEMORY_SIZE[0] + GRID_SIZE[0]) / 2) + 2):
                for elem in client_states.tiled_memory[i][j]:
                    self.tiled_area.blit(elem, (ref_movement_x + (j - (GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) / 2) * SPRITE_LEN,
                                            ref_movement_y + (i - (GRID_MEMORY_SIZE[1] - GRID_SIZE[1]) / 2) * SPRITE_LEN))

        for i in client_states.entities.values():
            pos_to_draw = (i.pos[0] - (client_states.map_center[0] - int(GRID_SIZE[0] / 2) - 2),
                           i.pos[1] - (client_states.map_center[1] - int(GRID_SIZE[1] / 2) - 2))
            if int((GRID_MEMORY_SIZE[1] - GRID_SIZE[1]) / 2) - 2 <= pos_to_draw[1] < int((GRID_MEMORY_SIZE[1] + GRID_SIZE[1]) / 2) + 2:
                if int((GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) / 2) - 2 <= pos_to_draw[0] < int((GRID_MEMORY_SIZE[0] + GRID_SIZE[0]) / 2) + 2:
                    # check if it is moving and its fix
                    entity_ref_movement_x = 0
                    entity_ref_movement_y = 0

                    if i.start_movement:
                        this_time = time.time()
                        if (this_time - i.start_movement) * i.speed_pixels > SPRITE_LEN:
                            this_time = SPRITE_LEN / i.speed_pixels + i.start_movement

                        diff_x = i.movement[0] - i.pos[0]
                        diff_y = i.movement[1] - i.pos[1]

                        if diff_x:
                            entity_ref_movement_x = diff_x * (i.speed_pixels * (this_time - i.start_movement))
                        if diff_y:
                            entity_ref_movement_y = diff_y * (i.speed_pixels * (this_time - i.start_movement))

                    self.tiled_area.blit(i.sprite, (ref_movement_x + entity_ref_movement_x + (pos_to_draw[0] - (GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) / 2) * SPRITE_LEN, ref_movement_y + entity_ref_movement_y + (pos_to_draw[1] - (GRID_MEMORY_SIZE[1] - GRID_SIZE[1]) / 2) * SPRITE_LEN))


        if client_states.player_character.sprite is not None:
            self.tiled_area.blit(client_states.player_character.sprite,
                                 ((int(GRID_SIZE[0] / 2)) * SPRITE_LEN, (int(GRID_SIZE[1] / 2)) * SPRITE_LEN))

        # draw to screen
        self.screen.blit(pygame.transform.scale(self.tiled_area, (int(size_x), int(size_y))), (pos_x, pos_y))

        # flip buffer
        pygame.display.flip()

    def resize(self, event):
        self.current_size = event.dict['size']
        self.screen = pygame.display.set_mode(self.current_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
