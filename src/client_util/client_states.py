# -*- coding: utf-8 -*-

# login imports
import stackless
import time

from util.alpha_communication import AlphaCommunicationMember
from util.alpha_defines import GRID_MEMORY_SIZE, SPRITE_LEN as TILE_SIZE, FONT_COLOR
from util.alpha_entities import Tile
from util.alpha_resource_loader import AlphaResourceLoader

# draw imports
import pygame
from client_util.client_ui import AlphaWindow, AlphaLabel, AlphaEditBox, AlphaButton
from util.alpha_defines import START_RESOLUTION, SPRITE_LEN, GRID_SIZE, GRID_MEMORY_SIZE, transparent, DRAW_PLAYERS_NAME


class ClientStates(AlphaCommunicationMember):
    def __init__(self):
        # server token
        self.session_id = None  # TODO: use later?
        self.running = True
        self.mode = AlphaLoginMode(START_RESOLUTION)

        self.channel = None
        self.logged = False

    def run(self):
        while self.running:
            self.mode.iterate()
            stackless.schedule()

    def notify(self, message):
        self.mode.notify(message, self)

    def resize(self, event):
        self.mode.resize(event)


class AlphaLoginMode:
    def __init__(self, screen_size):
        self.current_size = screen_size
        # screen objects
        self.aw = AlphaWindow((self.current_size[0] / 2 - 150, self.current_size[1] / 2 - 29 * 2), (300, 29 * 4), "LOGIN")
        al = AlphaLabel((3, 29), (120, 24), 'Account:')
        al2 = AlphaLabel((3, 29 * 2), (160, 24), 'Password:')
        ae = AlphaEditBox((3 + 150, 29), (145, 24), '')
        ae2 = AlphaEditBox((3 + 150, 29 * 2), (145, 24), '')

        ab = AlphaButton((0, 29 * 3), (150, 29), 'CANCEL', callback=print, callback_args=('cancel',))
        ab2 = AlphaButton((150, 29 * 3), (149, 29), 'OK', callback=print, callback_args=('ok',))
        self.aw.add_component([al, al2, ae, ae2, ab, ab2])
        self.selection = ae
        self.prepare()

    def resize(self, event):
        self.current_size = event.dict['size']
        self.prepare()

    def prepare(self):
        self.aw.pos = ((self.current_size[0] - self.aw.size[0]) / 2, (self.current_size[1] - self.aw.size[1]) / 2)
        self.aw.update()

    def render(self, dest):
        self.aw.render(dest)

    def iterate(self):
        pass

    def notify(self, message, caller):
        if type(message) is type(pygame.event):
            if self.selection:
                self.selection.notify(message)
        if message[0] == 'KEY' and message[1] == 'ENTER':
            caller.logged = True
            caller.mode = AlphaPlayMode(self.current_size)
            caller.channel.push([0, 'START'])


class AlphaPlayMode:
    def __init__(self, screen_size):
        self.current_size = screen_size
        # player and game information
        self.player_character = None
        self.tiled_memory = [[Tile() for __ in range(GRID_MEMORY_SIZE[0])] for _ in range(GRID_MEMORY_SIZE[1])]
        self.map_center = None
        self.entities = dict()

        # resource loader starter
        self.rl = AlphaResourceLoader()

        self.running = True
        self.ready_map = False
        self.ready_player = False

        self.ready = False

        self.texts_on_screen = list()

        # initializes grid memory
        self.tiled_area = pygame.Surface((GRID_SIZE[0] * SPRITE_LEN, GRID_SIZE[1] * SPRITE_LEN), pygame.SRCALPHA)
        self.players_and_texts = None # TODO
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
        # player position if in movement
        ref_movement_x = 0
        ref_movement_y = 0
        if self.player_character.start_movement:
            this_time = time.time()
            # check the direction it is moving
            diff = (self.player_character.movement[0] - self.player_character.pos[0],
                    self.player_character.movement[1] - self.player_character.pos[1])

            # space walked given speed and time
            space_walked = (-SPRITE_LEN + self.player_character.speed_pixels *
                            (this_time - self.player_character.start_movement))

            # if really walking, lets see how far we've got
            if diff[0]:
                ref_movement_x = -diff[0] * space_walked
            if diff[1]:
                ref_movement_y = -diff[1] * space_walked

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

    def notify(self, message, caller):
        # print("States received", message)
        if message[0] == 'KEY':
            if message[1] in ['LEFT', 'RIGHT', 'UP', 'DOWN'] and self.player_character.start_movement is None:
                if message[1] == 'LEFT':
                    caller.channel.push([0, 'MAP', self.player_character.pos[0] - 1, self.player_character.pos[1]])
                elif message[1] == 'RIGHT':
                    caller.channel.push([0, 'MAP', self.player_character.pos[0] + 1, self.player_character.pos[1]])
                elif message[1] == 'UP':
                    caller.channel.push([0, 'MAP', self.player_character.pos[0], self.player_character.pos[1] - 1])
                elif message[1] == 'DOWN':
                    caller.channel.push([0, 'MAP', self.player_character.pos[0], self.player_character.pos[1] + 1])
        elif message[0] == 'ADD_ENTITIES':
            for i in message[1]:
                self.add_entity(i)
        elif message[0] == 'REMOVE_ENTITIES':
            for i in message[1]:
                self.remove_entity(i)
        elif message[0] == 'CURR_ENTITIES':
            self.replace_entities(message[1])
        elif message[0] == 'MAP':
            self.map_center = (message[1], message[2])
            self.player_character.set_movement(message[1] - self.player_character.pos[0], message[2] - self.player_character.pos[1])
            ret = message[3]
            for j in range(GRID_MEMORY_SIZE[1]):
                for i in range(GRID_MEMORY_SIZE[0]):
                    self.tiled_memory[i][j] = ret[i][j]
                    self.tiled_memory[i][j].load(self.rl)
            self.ready_map = True
            if self.ready_player:
                self.ready = True
        elif message[0] == 'POS':
            self.player_character.pos = (message[1], message[2])
            self.player_character.set_movement(0, 0, immediate=True)
        elif message[0] == 'PLAYER':
            self.player_character = message[1]
            self.player_character.load(self.rl)
            font = self.rl.get_font()
            self.player_character.entity_name_surface = font.render(message[1].name, 1, FONT_COLOR)
            self.ready_player = True
            if self.ready_map:
                self.ready = True
        elif message[0] == 'SAY':
            font = self.rl.get_font()
            self.texts_on_screen.append((time.time(), font.render(message[2].name + ': ' + message[1], 1, FONT_COLOR), message[2]))
        else:
            print("MESSAGE UNIDENTIFIED AT", self.__class__.__name__, message)

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
