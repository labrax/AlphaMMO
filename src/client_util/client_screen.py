# -*- coding: utf-8 -*-

import time

import pygame
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE

from util.alpha_defines import START_RESOLUTION, SPRITE_LEN, GRID_SIZE, GRID_MEMORY_SIZE, gray, transparent, version, \
    DRAW_PLAYERS_NAME


class ClientScreen:
    def __init__(self):
        # start screen
        self.current_size = START_RESOLUTION
        self.screen = pygame.display.set_mode(self.current_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
        pygame.display.set_caption('AlphaMMO Client ' + str(version))
        pygame.display.flip()

        # initializes grid memory
        self.tiled_area = pygame.Surface((GRID_SIZE[0] * SPRITE_LEN, GRID_SIZE[1] * SPRITE_LEN), pygame.SRCALPHA)
        self.players_and_texts = None # TODO

        self.size = None
        self.pos = None
        self.prepare()

    def prepare(self):
        # prepare range to fit screen
        ## get the smallest side fitting
        tiles_at = (self.current_size[0] / SPRITE_LEN, self.current_size[1] / SPRITE_LEN)
        tiles = tiles_at[0]
        if tiles_at[1] < tiles_at[0]:
            tiles = tiles_at[1]
        ## get the position
        self.size = (tiles * SPRITE_LEN, tiles * SPRITE_LEN)

        self.pos = (self.current_size[0] / 2 - self.size[0] / 2, self.current_size[1] / 2 - self.size[1] / 2)

        # surface updated when resizing
        self.players_and_texts = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)

    def render(self, client_states):
        # player position if in movement
        ref_movement_x = 0
        ref_movement_y = 0
        if client_states.player_character.start_movement:
            this_time = time.time()
            # check the direction it is moving
            diff = (client_states.player_character.movement[0] - client_states.player_character.pos[0],
                    client_states.player_character.movement[1] - client_states.player_character.pos[1])

            # space walked given speed and time
            space_walked = (-SPRITE_LEN + client_states.player_character.speed_pixels *
                            (this_time - client_states.player_character.start_movement))

            # if really walking, lets see how far we've got
            if diff[0]:
                ref_movement_x = -diff[0] * space_walked
            if diff[1]:
                ref_movement_y = -diff[1] * space_walked

        # clear screen
        self.screen.fill(gray)

        # clear temporary areas
        self.tiled_area.fill(transparent)
        self.players_and_texts.fill(transparent)

        # draw the tiles
        for i in range(int((GRID_MEMORY_SIZE[1] - GRID_SIZE[1]) / 2) - 2,
                       int((GRID_MEMORY_SIZE[1] + GRID_SIZE[1]) / 2) + 2):
            for j in range(int((GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) / 2) - 2,
                           int((GRID_MEMORY_SIZE[0] + GRID_SIZE[0]) / 2) + 2):
                for elem in client_states.tiled_memory[i][j]:
                    self.tiled_area.blit(elem,
                                         (ref_movement_x + (j - (GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) / 2) * SPRITE_LEN,
                                          ref_movement_y + (i - (GRID_MEMORY_SIZE[1] - GRID_SIZE[1]) / 2) * SPRITE_LEN))

        # draw the player character
        # this could be moved to render in the other area (but the sprite doesnt move, so its safe
        if client_states.player_character.sprite:
            self.tiled_area.blit(client_states.player_character.sprite,
                                 ((int(GRID_SIZE[0] / 2)) * SPRITE_LEN, (int(GRID_SIZE[1] / 2)) * SPRITE_LEN))

        # this factor is a space from the initial area to the scaled, without this factor we would have
        # the previous coordinate on the tiled area
        factor = self.size[0]/self.tiled_area.get_width()

        # draw entities and their names
        for i in client_states.entities.values():
            pos_to_draw = (i.pos[0] - (client_states.map_center[0] - int(GRID_SIZE[0] / 2) - 2),
                           i.pos[1] - (client_states.map_center[1] - int(GRID_SIZE[1] / 2) - 2))
            if int((GRID_MEMORY_SIZE[1] - GRID_SIZE[1]) / 2) - 2 <= pos_to_draw[1] < int((GRID_MEMORY_SIZE[1] + GRID_SIZE[1]) / 2) + 2:
                if int((GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) / 2) - 2 <= pos_to_draw[0] < int((GRID_MEMORY_SIZE[0] + GRID_SIZE[0]) / 2) + 2:
                    # check if it is moving and its fix
                    entity_ref_movement_x = 0
                    entity_ref_movement_y = 0

                    # calculate movement delta if moving
                    if i.start_movement:
                        this_time = time.time()
                        if (this_time - i.start_movement) * i.speed_pixels > SPRITE_LEN:
                            this_time = SPRITE_LEN / i.speed_pixels + i.start_movement

                        # is there a movement? lets get the difference
                        diff = (i.movement[0] - i.pos[0], i.movement[1] - i.pos[1])
                        # given a speed and time, we got the space travelled
                        space_walked = (i.speed_pixels * (this_time - i.start_movement))

                        if diff[0]:
                            entity_ref_movement_x = diff[0] * space_walked
                        if diff[1]:
                            entity_ref_movement_y = diff[1] * space_walked

                    self.players_and_texts.blit(pygame.transform.scale(i.sprite, (int(SPRITE_LEN * factor), int(SPRITE_LEN * factor))),
                                         (factor * (ref_movement_x + entity_ref_movement_x + (pos_to_draw[0] - (GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) / 2) * SPRITE_LEN),
                                         factor * (ref_movement_y + entity_ref_movement_y + (pos_to_draw[1] - (GRID_MEMORY_SIZE[1] - GRID_SIZE[1]) / 2) * SPRITE_LEN)))
                    if DRAW_PLAYERS_NAME:
                        self.players_and_texts.blit(i.entity_name_surface,
                                                (- i.entity_name_surface.get_width() / 2 + factor * (SPRITE_LEN / 2 + ref_movement_x + entity_ref_movement_x + (pos_to_draw[0] - (GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) / 2) * SPRITE_LEN),
                                                 - i.entity_name_surface.get_height() / 2 + factor * (-1 + ref_movement_y + entity_ref_movement_y + (pos_to_draw[1] - (GRID_MEMORY_SIZE[1] - GRID_SIZE[1]) / 2) * SPRITE_LEN)))

        # draw player name
        if client_states.player_character.entity_name_surface and DRAW_PLAYERS_NAME:
            self.players_and_texts.blit(client_states.player_character.entity_name_surface, (- client_states.player_character.entity_name_surface.get_width() / 2 + factor * (SPRITE_LEN / 2 + (int(GRID_SIZE[0] / 2)) * SPRITE_LEN), - client_states.player_character.entity_name_surface.get_height() / 2 + factor * (-1 + (int(GRID_SIZE[1] / 2)) * SPRITE_LEN)))

        # draw tiles to screen (from the tiled area to main screen)
        self.screen.blit(pygame.transform.scale(self.tiled_area, (int(self.size[0]), int(self.size[1]))), (self.pos[0], self.pos[1]))

        # draw the text, entites are saying
        # TODO: how should text be printed?
        for i in range(len(client_states.texts_on_screen)):
            message = client_states.texts_on_screen[i][1]
            entity = client_states.texts_on_screen[i][2]
            self.screen.blit(message, (0, message.get_height()*i))

        # draw players and texts to screen (from the temporary surface)
        self.screen.blit(self.players_and_texts, (self.pos[0], self.pos[1]))

        # flip buffer (display it)
        pygame.display.flip()

    def resize(self, event):
        self.current_size = event.dict['size']
        self.screen = pygame.display.set_mode(self.current_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.prepare()
