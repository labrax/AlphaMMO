# -*- coding: utf-8 -*-

import stackless

from client_entities import *
from alpha_defines import GRID_MEMORY_SIZE, SPRITE_LEN as TILE_SIZE
from util.resource_loader import AlphaResourceLoader
from alpha_communication import AlphaCommunicationMember


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

    def replace_entities(self, entities):
        self.entities = dict()
        for i in entities:
            self.add_entity(i)

    def add_entity(self, entity):
        self.entities[entity.entity_id] = entity

    def remove_entity(self, entity):
        self.entities.pop(entity.entity_id)

    def start(self):
        self.channel.push([self.session_token, 'START'])

    def run(self):
        # player position
        while self.running:
            if (self.player_character.start_movement):
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
            self.ready = True
        else:
            print("MESSAGE UNIDENTIFIED AT", self.__class__.__name__, message)
