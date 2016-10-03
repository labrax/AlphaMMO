# -*- coding: utf-8 -*-


import time
import pygame

from client_util.client_states_modes.alpha_mode import AlphaMode
import client_util.client_states_modes.alpha_login

from util.alpha_defines import GRID_MEMORY_SIZE, SPRITE_LEN, SPRITE_LEN as TILE_SIZE, FONT_COLOR, GRID_SIZE, DRAW_PLAYERS_NAME, transparent
from util.alpha_entities import Tile
from util.alpha_resource_loader import AlphaResourceLoader

# internal and external protocol
from util.alpha_protocol import AlphaProtocol
from client_util.client_internal_protocol import AlphaClientProtocol, AlphaClientProtocolValues


class AlphaPlayMode(AlphaMode):
    """
    Class for the playing screen
    AlphaPlayMode.player_character is the player character information
    AlphaPlayMode.tiled_memory is the game grid information
    AlphaPlayMode.map_center is the position of the center of the map
    AlphaPlayMode.entities is the dictionary of entities information
    AlphaPlayMode.effects is the dictionary of effects information
    AlphaPlayMode.key check which keys are pressed
    AlphaPlayMode.waiting_movement to check if it is waiting for a reply from the server related to movement
    AlphaPlayMode.waiting_action to check if it is waiting for a reply from the server related to action
    AlphaPlayMode.rl is the resource loader for the game sprites
    AlphaPlayMode.running if the play screen is executing
    AlphaPlayMode.ready_map if the map is ready to display
    AlphaPlayMode.ready_player if the player character is ready to display
    AlphaPlayMode.ready if the game is ready to display
    AlphaPlayMode.texts_on_screen is the list of texts on screen
    AlphaPlayMode.tiled_area is the draw information about the tiles on the game
    AlphaPlayMode.players_and_texts draws information about the players and texts
    AlphaPlayMode.size is the screen size
    AlphaPlayMode.pos is the position to draw the elements the box inside the screen
    """
    def __init__(self, screen_size, client_states):
        super(AlphaPlayMode, self).__init__(screen_size, client_states)
        # player and game information
        self.player_character = None
        self.tiled_memory = [[Tile() for __ in range(GRID_MEMORY_SIZE[0])] for _ in range(GRID_MEMORY_SIZE[1])]
        self.map_center = None
        self.entities = dict()
        self.effects = dict()
        self.key = {'up': False, 'down': False, 'right': False, 'left': False, 'space': False}
        self.waiting_movement = False
        self.waiting_action = False

        # resource loader starter
        self.rl = AlphaResourceLoader()

        self.running = True
        self.ready_map = False
        self.ready_player = False

        self.ready = False

        self.texts_on_screen = list()

        # initializes grid memory
        self.tiled_area = pygame.Surface((GRID_SIZE[0] * SPRITE_LEN, GRID_SIZE[1] * SPRITE_LEN), pygame.SRCALPHA)
        self.players_and_texts = None
        self.size = None
        self.pos = None
        self.prepare()

    def resize(self, event):
        self.current_size = event.dict['size']
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

    def render(self, dest):
        if not self.ready:
            return
        # get the map center position in relation to the current player movement (this will avoid a flicker)
        ref_movement_x = (self.map_center[0] - self.player_character.movement[0]) * SPRITE_LEN
        ref_movement_y = (self.map_center[1] - self.player_character.movement[1]) * SPRITE_LEN
        if self.player_character.start_movement:
            this_time = time.time()
            # check the direction it is moving
            diff = (self.player_character.movement[0] - self.player_character.pos[0],
                    self.player_character.movement[1] - self.player_character.pos[1])

            # space walked given speed and time
            space_walked = (-SPRITE_LEN + self.player_character.speed_pixels *
                            (this_time - self.player_character.start_movement))

            # if really walking, lets see how far we've got and add the to reference center
            if diff[0]:
                ref_movement_x += -diff[0] * space_walked
            if diff[1]:
                ref_movement_y += -diff[1] * space_walked

        # clear temporary areas
        self.tiled_area.fill(transparent)
        self.players_and_texts.fill(transparent)

        # draw the tiles
        for i in range(int((GRID_MEMORY_SIZE[1] - GRID_SIZE[1]) / 2) - 2,
                       int((GRID_MEMORY_SIZE[1] + GRID_SIZE[1]) / 2) + 2):
            for j in range(int((GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) / 2) - 2,
                           int((GRID_MEMORY_SIZE[0] + GRID_SIZE[0]) / 2) + 2):
                for elem in self.tiled_memory[i][j]:
                    self.tiled_area.blit(elem,
                                         (ref_movement_x + (
                                         j - (GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) / 2) * SPRITE_LEN,
                                          ref_movement_y + (
                                          i - (GRID_MEMORY_SIZE[1] - GRID_SIZE[1]) / 2) * SPRITE_LEN))

        # draw the player character
        # this could be moved to render in the other area (but the sprite doesnt move, so its safe
        if self.player_character.sprite:
            self.tiled_area.blit(self.player_character.sprite,
                                 ((int(GRID_SIZE[0] / 2)) * SPRITE_LEN, (int(GRID_SIZE[1] / 2)) * SPRITE_LEN))

        # this factor is a space from the initial area to the scaled, without this factor we would have
        # the previous coordinate on the tiled area
        factor = self.size[0] / self.tiled_area.get_width()

        # draw entities and their names
        for i in self.entities.values():
            pos_to_draw = (i.pos[0] - (self.map_center[0] - int(GRID_SIZE[0] / 2) - 2),
                           i.pos[1] - (self.map_center[1] - int(GRID_SIZE[1] / 2) - 2))
            if int((GRID_MEMORY_SIZE[1] - GRID_SIZE[1]) / 2) - 2 <= pos_to_draw[1] < int(
                            (GRID_MEMORY_SIZE[1] + GRID_SIZE[1]) / 2) + 2:
                if int((GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) / 2) - 2 <= pos_to_draw[0] < int(
                                (GRID_MEMORY_SIZE[0] + GRID_SIZE[0]) / 2) + 2:
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

                    self.players_and_texts.blit(
                        pygame.transform.scale(i.sprite, (int(SPRITE_LEN * factor), int(SPRITE_LEN * factor))),
                        (factor * (ref_movement_x + entity_ref_movement_x + (
                        pos_to_draw[0] - (GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) / 2) * SPRITE_LEN),
                         factor * (ref_movement_y + entity_ref_movement_y + (
                         pos_to_draw[1] - (GRID_MEMORY_SIZE[1] - GRID_SIZE[1]) / 2) * SPRITE_LEN)))

                    # TODO: draw hp & mp
                    '''if DRAW_HP:
                        pygame.draw.rect(self.players_and_texts, (255, 255, 255), pygame.Rect())
                        self.players_and_texts.blit(i.entity_name_surface,
                                                    (- i.entity_name_surface.get_width() / 2 + factor * (
                                                        SPRITE_LEN / 2 + ref_movement_x + entity_ref_movement_x + (
                                                            pos_to_draw[0] - (
                                                                GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) / 2) * SPRITE_LEN),
                                                     - i.entity_name_surface.get_height() / 2 + factor * (
                                                         -1 + ref_movement_y + entity_ref_movement_y + (
                                                             pos_to_draw[1] - (
                                                                 GRID_MEMORY_SIZE[1] - GRID_SIZE[
                                                                     1]) / 2) * SPRITE_LEN)))'''

                    if DRAW_PLAYERS_NAME:
                        self.players_and_texts.blit(i.entity_name_surface,
                                                    (- i.entity_name_surface.get_width() / 2 + factor * (
                                                    SPRITE_LEN / 2 + ref_movement_x + entity_ref_movement_x + (
                                                    pos_to_draw[0] - (
                                                    GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) / 2) * SPRITE_LEN),
                                                     - i.entity_name_surface.get_height() / 2 + factor * (
                                                     -1 + ref_movement_y + entity_ref_movement_y + (
                                                     pos_to_draw[1] - (
                                                     GRID_MEMORY_SIZE[1] - GRID_SIZE[1]) / 2) * SPRITE_LEN)))

        # draw player name
        if self.player_character.entity_name_surface and DRAW_PLAYERS_NAME:
            self.players_and_texts.blit(self.player_character.entity_name_surface, (
            - self.player_character.entity_name_surface.get_width() / 2 + factor * (
            SPRITE_LEN / 2 + (int(GRID_SIZE[0] / 2)) * SPRITE_LEN),
            - self.player_character.entity_name_surface.get_height() / 2 + factor * (
            -1 + (int(GRID_SIZE[1] / 2)) * SPRITE_LEN)))

        # draw tiles to screen (from the tiled area to main screen)
        dest.blit(pygame.transform.scale(self.tiled_area, (int(self.size[0]), int(self.size[1]))),
                         (self.pos[0], self.pos[1]))

        # draw the text, entites are saying
        # TODO: how should text be printed?
        for i in range(len(self.texts_on_screen)):
            message = self.texts_on_screen[i][1]
            entity = self.texts_on_screen[i][2]
            dest.blit(message, (0, message.get_height() * i))

        # draw effects:
        will_remove = list()
        for i, j in self.effects.items():
            sprite = j.get_sprite()
            if not sprite:
                will_remove.append(i)
                continue
            else:
                pos_to_draw = (j.pos[0] - (self.map_center[0] - int(GRID_SIZE[0] / 2) - 2),
                               j.pos[1] - (self.map_center[1] - int(GRID_SIZE[1] / 2) - 2))
                self.players_and_texts.blit(
                    pygame.transform.scale(sprite, (int(SPRITE_LEN * factor),
                                                    int(SPRITE_LEN * factor))),
                    (factor * (ref_movement_x + (pos_to_draw[0] - (GRID_MEMORY_SIZE[0] - GRID_SIZE[0]) / 2) * SPRITE_LEN),
                    factor * (ref_movement_y + (pos_to_draw[1] - (GRID_MEMORY_SIZE[1] - GRID_SIZE[1]) / 2) * SPRITE_LEN))
                )
        for i in will_remove:
            self.effects.pop(i)

        # draw players and texts to screen (from the temporary surface)
        dest.blit(self.players_and_texts, (self.pos[0], self.pos[1]))

    def iterate(self):
        if self.ready:
            # first check texts to be removed
            texts_on_screen_to_be_removed_index = 0
            for i in range(len(self.texts_on_screen)):
                time_elapsed = time.time() - self.texts_on_screen[i][0]
                if time_elapsed > 10:
                    texts_on_screen_to_be_removed_index = i
            self.texts_on_screen = self.texts_on_screen[texts_on_screen_to_be_removed_index:]

            if self.player_character.start_movement:
                this_time = time.time()
                # movement is over
                if self.player_character.speed_pixels * (
                    this_time - self.player_character.start_movement) > TILE_SIZE:
                    self.player_character.pos = (
                    self.player_character.movement[0], self.player_character.movement[1])
                    self.player_character.start_movement = None

            if not self.player_character.start_movement and not self.waiting_movement:
                def _request_movement(pos):
                    self.client_states.channel.push(
                        [AlphaProtocol.REQUEST_MOVE, pos[0], pos[1]])
                    self.waiting_movement = True
                if self.key['left']:
                    if self.tiled_memory[self.map_center[0] - self.player_character.pos[0] - 1][self.map_center[1] - self.player_character.pos[1]].can_walk:
                        _request_movement([self.player_character.pos[0] - 1, self.player_character.pos[1]])
                    else:
                        self.key['left'] = False
                elif self.key['right']:
                    if self.tiled_memory[self.map_center[0] - self.player_character.pos[0] + 1][self.map_center[1] - self.player_character.pos[1]].can_walk:
                        _request_movement([self.player_character.pos[0] + 1, self.player_character.pos[1]])
                    else:
                        self.key['right'] = False
                elif self.key['up']:
                    if self.tiled_memory[self.map_center[0] - self.player_character.pos[0]][self.map_center[1] - self.player_character.pos[1] - 1].can_walk:
                        _request_movement([self.player_character.pos[0], self.player_character.pos[1] - 1])
                    else:
                        self.key['up'] = False
                elif self.key['down']:
                    if self.tiled_memory[self.map_center[0] - self.player_character.pos[0]][self.map_center[1] - self.player_character.pos[1] + 1].can_walk:
                        _request_movement([self.player_character.pos[0], self.player_character.pos[1] + 1])
                    else:
                        self.key['down'] = False

            if not self.player_character.start_action and not self.waiting_action:
                if self.key['space']:
                    self.client_states.channel.push(
                        [AlphaProtocol.REQUEST_ACTION, 1, self.player_character.pos[0], self.player_character.pos[1], self.player_character.entity_id]
                    )
                    self.waiting_action = True

    def notify(self, message):
        if isinstance(message, pygame.event.EventType):
            event = message
            # only try to move when another movement is already finished
            if self.player_character:
                if event.type == pygame.locals.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.key['left'] = True
                        self.key['right'] = False
                    elif event.key == pygame.K_RIGHT:
                        self.key['left'] = False
                        self.key['right'] = True
                    elif event.key == pygame.K_UP:
                        self.key['up'] = True
                        self.key['down'] = False
                    elif event.key == pygame.K_DOWN:
                        self.key['up'] = False
                        self.key['down'] = True
                    elif event.key == pygame.K_SPACE:
                        self.key['space'] = True
                elif event.type == pygame.locals.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.key['left'] = False
                    elif event.key == pygame.K_RIGHT:
                        self.key['right'] = False
                    elif event.key == pygame.K_UP:
                        self.key['up'] = False
                    elif event.key == pygame.K_DOWN:
                        self.key['down'] = False
                    elif event.key == pygame.K_SPACE:
                        self.key['space'] = False
        else:
            print(self.__class__.__name__, "received", message)
            if message[0] == AlphaProtocol.SET_ENTITIES:
                for i in message[1]:
                    self.add_entity(i)
            elif message[0] == AlphaProtocol.REMOVE_ENTITIES:
                for i in message[1]:
                    self.remove_entity(i)
            elif message[0] == AlphaProtocol.REMOVE_ENTITY:
                self.remove_entity(message[1])
            elif message[0] == AlphaProtocol.REPLACE_ENTITIES:
                self.replace_entities(message[1])
            elif message[0] == AlphaProtocol.SET_ENTITY:
                self.add_entity(message[1])
            elif message[0] == AlphaProtocol.MOVING:
                self.player_character.set_movement(message[1] - self.player_character.pos[0], message[2] - self.player_character.pos[1])
                self.waiting_movement = False
            elif message[0] == AlphaProtocol.ACTION:
                self.waiting_action = False
            elif message[0] == AlphaProtocol.EFFECT:
                effect = message[1]
                effect.load(self.rl)
                self.effects[effect] = effect
            elif message[0] == AlphaProtocol.RECEIVE_MAP:
                self.map_center = (message[1], message[2])
                ret = message[3]
                for j in range(GRID_MEMORY_SIZE[1]):
                    for i in range(GRID_MEMORY_SIZE[0]):
                        self.tiled_memory[i][j] = ret[i][j]
                        self.tiled_memory[i][j].load(self.rl)
                self.ready_map = True
            elif message[0] == AlphaProtocol.TELEPORT:
                self.player_character.pos = (message[1], message[2])
                self.player_character.set_movement(0, 0, immediate=True)
            elif message[0] == AlphaProtocol.RECEIVE_PLAYER:
                self.player_character = message[1]
                self.player_character.load(self.rl)
                font = self.rl.get_font()
                self.player_character.entity_name_surface = font.render(message[1].name, 1, FONT_COLOR)
                self.ready_player = True
            elif message[0] == AlphaProtocol.SPEAKING:
                font = self.rl.get_font()
                self.texts_on_screen.append((time.time(), font.render(message[2].name + ': ' + message[1], 1, FONT_COLOR), message[2]))
            elif message[0] == AlphaClientProtocol.INTERNAL_STATUS and message[1] == AlphaClientProtocolValues.OFF:
                self.client_states.mode = client_util.client_states_modes.alpha_login.AlphaLoginMode(self.current_size, self.client_states)
                self.client_states.logged = False
            else:
                print("MESSAGE UNIDENTIFIED AT", self.__class__.__name__, message)

        if self.ready_map and self.ready_player:
            self.ready = True

    def replace_entities(self, entities):
        self.entities = dict()
        for i in entities:
            self.add_entity(i)

    def add_entity(self, entity):
        # TODO: move code?
        font = self.rl.get_font()
        entity.entity_name_surface = font.render(entity.name, 1, FONT_COLOR)
        entity.load(self.rl)
        self.entities[entity.entity_id] = entity

    def remove_entity(self, entity):
        self.entities.pop(entity.entity_id)
