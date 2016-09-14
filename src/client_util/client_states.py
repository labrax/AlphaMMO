# -*- coding: utf-8 -*-

import stackless
import time

from util.alpha_communication import AlphaCommunicationMember
from util.alpha_defines import GRID_MEMORY_SIZE, SPRITE_LEN as TILE_SIZE, FONT_COLOR
from util.alpha_entities import Tile
from util.alpha_resource_loader import AlphaResourceLoader


class ClientStates(AlphaCommunicationMember):
    def __init__(self):
        # server token
        self.session_id = None  # TODO: use later?
        self.running = True
        self.mode = AlphaLoginMode()

        self.channel = None
        self.logged = False

    def run(self):
        while self.running:
            self.mode.iterate()
            stackless.schedule()

    def notify(self, message):
        self.mode.notify(message, self)


class AlphaLoginMode:
    def __init__(self):
        pass

    def notify(self, message, caller):
        if message[0] == 'KEY' and message[1] == 'ENTER':
            caller.logged = True
            caller.mode = AlphaPlayMode()
            caller.channel.push([0, 'START'])

    def iterate(self):
        pass

    def ok(self):
        print('ok')

    def cancel(self):
        print('cancel')


class AlphaPlayMode:
    def __init__(self):
        # player and game information
        self.player_character = None
        self.tiled_memory = [[Tile() for _2 in range(GRID_MEMORY_SIZE[0])] for _ in range(GRID_MEMORY_SIZE[1])]
        self.map_center = None
        self.entities = dict()

        # resource loader starter
        self.rl = AlphaResourceLoader()

        self.running = True
        self.ready_map = False
        self.ready_player = False

        self.ready = False

        self.texts_on_screen = list()

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
