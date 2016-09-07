# -*- coding: utf-8 -*-

from client_entities import *
from alpha_defines import GRID_MEMORY_SIZE, SPRITE_LEN as TILE_SIZE
from util.resource_loader import AlphaResourceLoader
from client_communication import AlphaCommunicationMember


class ClientStates(AlphaCommunicationMember):
    def __init__(self):
        self.session_token = None

        self.player_character = Entity()
        self.tiled_memory = [[Tile() for _2 in range(GRID_MEMORY_SIZE[0])] for _ in range(GRID_MEMORY_SIZE[1])]
        self.map_center = None

        self.channel = None

        # resource loader starter
        self.rl = AlphaResourceLoader()

        ''''# sample for testing
        for i in range(GRID_MEMORY_SIZE[1]):
            for j in range(GRID_MEMORY_SIZE[0]):
                self.tiled_memory[i][j].tile = self.rl.get_sprite('roguelikeDungeon_transparent.png', 16, 15)

        #self.tiled_memory[6][6].characters.append(self.rl.get_sprite('roguelikeChar_transparent.png', 0, 8))  # screen center
        self.tiled_memory[6][5].characters.append(self.rl.get_sprite('roguelikeChar_transparent.png', 1, 9))
        self.tiled_memory[2][2].characters.append(self.rl.get_sprite('roguelikeChar_transparent.png', 0, 7))

        self.tiled_memory[2][2].decor_objects.append(self.rl.get_sprite('roguelikeDungeon_transparent.png', 1, 4))
        self.tiled_memory[7][7].decor_objects.append(self.rl.get_sprite('roguelikeDungeon_transparent.png', 1, 4))
        self.tiled_memory[8][8].decor_objects.append(self.rl.get_sprite('roguelikeDungeon_transparent.png', 1, 4))'''

        self.player_character.sprite = self.rl.get_sprite('roguelikeChar_transparent.png', 0, 8) # player character

    def start(self):
        self.map_center = (self.player_character.pos[0], self.player_character.pos[1])
        self.channel.push(['START', self.player_character.pos[0], self.player_character.pos[1]])

    def run(self):
        # player position
        if (self.player_character.start_movement):
            this_time = time.time()

            # movement is over
            if self.player_character.speed_pixels * (
                this_time - self.player_character.start_movement) > TILE_SIZE:
                self.player_character.pos = (
                self.player_character.movement[0], self.player_character.movement[1])
                self.player_character.start_movement = None


    def notify(self, message):
        if message[0] == 'KEY':
            if message[1] in ['LEFT', 'RIGHT', 'UP', 'DOWN'] and self.player_character.start_movement is None:
                if message[1] == 'LEFT':
                    self.channel.push(['MAP', self.player_character.pos[0] - 1, self.player_character.pos[1]])
                elif message[1] == 'RIGHT':
                    self.channel.push(['MAP', self.player_character.pos[0] + 1, self.player_character.pos[1]])
                elif message[1] == 'UP':
                    self.channel.push(['MAP', self.player_character.pos[0], self.player_character.pos[1] - 1])
                elif message[1] == 'DOWN':
                    self.channel.push(['MAP', self.player_character.pos[0], self.player_character.pos[1] + 1])
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
