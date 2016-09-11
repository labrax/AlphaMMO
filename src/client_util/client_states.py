# -*- coding: utf-8 -*-

import stackless
import time

from util.alpha_communication import AlphaCommunicationMember
from util.alpha_defines import GRID_MEMORY_SIZE, SPRITE_LEN as TILE_SIZE, FONT_COLOR
from util.alpha_entities import Tile
from util.resource_loader import AlphaResourceLoader


class ClientStates(AlphaCommunicationMember):
    def __init__(self):
        # server token
        self.session_token = 1

        # player and game information
        self.player_character = None
        self.tiled_memory = [[Tile() for _2 in range(GRID_MEMORY_SIZE[0])] for _ in range(GRID_MEMORY_SIZE[1])]
        self.map_center = None
        self.entities = dict()

        self.channel = None

        # resource loader starter
        self.rl = AlphaResourceLoader()

        self.running = True
        self.ready = False

        self.texts_on_screen = list()

    def replace_entities(self, entities):
        self.entities = dict()
        for i in entities:
            self.add_entity(i)

    def add_entity(self, entity):
        font = self.rl.get_font()
        entity.entity_name_surface = font.render(entity.name, 1, FONT_COLOR)
        self.entities[entity.entity_id] = entity

    def remove_entity(self, entity):
        self.entities.pop(entity.entity_id)

    def start(self):
        self.channel.push([self.session_token, 'START'])

    def run(self):
        # player position
        while self.running:
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
            stackless.schedule()

    def notify(self, message):
        if message[0] == 'KEY':
            if message[1] in ['LEFT', 'RIGHT', 'UP', 'DOWN'] and self.player_character.start_movement is None:
                if message[1] == 'LEFT':
                    self.channel.push([self.session_token, 'MAP', self.player_character.pos[0] - 1, self.player_character.pos[1]])
                elif message[1] == 'RIGHT':
                    self.channel.push([self.session_token, 'MAP', self.player_character.pos[0] + 1, self.player_character.pos[1]])
                elif message[1] == 'UP':
                    self.channel.push([self.session_token, 'MAP', self.player_character.pos[0], self.player_character.pos[1] - 1])
                elif message[1] == 'DOWN':
                    self.channel.push([self.session_token, 'MAP', self.player_character.pos[0], self.player_character.pos[1] + 1])
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
        elif message[0] == 'POS':
            self.player_character.pos = (message[1], message[2])
            self.player_character.set_movement(0, 0, immediate=True)
        elif message[0] == 'PLAYER':
            self.player_character = message[1]
            font = self.rl.get_font()
            self.player_character.entity_name_surface = font.render(message[1].name, 1, FONT_COLOR)
            self.ready = True
        elif message[0] == 'SAY':
            font = self.rl.get_font()
            self.texts_on_screen.append((time.time(), font.render(message[2].name + ': ' + message[1], 1, FONT_COLOR), message[2]))
        else:
            print("MESSAGE UNIDENTIFIED AT", self.__class__.__name__, message)
