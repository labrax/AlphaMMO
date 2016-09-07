# -*- coding: utf-8 -*-

from client_communication import AlphaCommunicationMember
from util.resource_loader import AlphaResourceLoader
from client_entities import Tile
from alpha_defines import GRID_MEMORY_SIZE as CLIENT_GRID_MEMORY_SIZE
from alpha_defines import GRID_MEMORY_SIZE

#GRID_MEMORY_SIZE = (12, 20)


class ClientAsServer(AlphaCommunicationMember):
    def __init__(self):
        # to write back
        self.channel = None

        # to load some resources
        self.rl = AlphaResourceLoader()

        ######################COPIED
        # sample for testing
        """
        self.tiled_memory = [[Tile() for _2 in range(GRID_MEMORY_SIZE[0])] for _ in range(GRID_MEMORY_SIZE[1])]
        for i in range(GRID_MEMORY_SIZE[1]):
            for j in range(GRID_MEMORY_SIZE[0]):
                self.tiled_memory[i][j].tile = self.rl.get_sprite('roguelikeDungeon_transparent.png', 16, 15)

        self.tiled_memory[6][5].characters.append(self.rl.get_sprite('roguelikeChar_transparent.png', 1, 9))
        self.tiled_memory[2][2].characters.append(self.rl.get_sprite('roguelikeChar_transparent.png', 0, 7))

        self.tiled_memory[2][2].decor_objects.append(self.rl.get_sprite('roguelikeDungeon_transparent.png', 1, 4))
        self.tiled_memory[7][7].decor_objects.append(self.rl.get_sprite('roguelikeDungeon_transparent.png', 1, 4))
        self.tiled_memory[8][8].decor_objects.append(self.rl.get_sprite('roguelikeDungeon_transparent.png', 1, 4))
        """

        # dummy map
        self.tiled_memory = [[Tile() for _2 in range(GRID_MEMORY_SIZE[0])] for _ in range(GRID_MEMORY_SIZE[1])]
        for i in range(GRID_MEMORY_SIZE[1]):
            for j in range(GRID_MEMORY_SIZE[0]):
                if i % 3 == 0 and j % 5 == 0:
                    self.tiled_memory[i][j].tile = self.rl.get_sprite('roguelikeDungeon_transparent.png', 17, 15)
                elif i % 4 == 0 and j % 7 == 0:
                    self.tiled_memory[i][j].tile = self.rl.get_sprite('roguelikeDungeon_transparent.png', 20, 15)
                else:
                    self.tiled_memory[i][j].tile = self.rl.get_sprite('roguelikeDungeon_transparent.png', 16, 15)
                if i % 9 == 0 and j % 3 == 0:
                    self.tiled_memory[i][j].decor_objects.append(
                        self.rl.get_sprite('roguelikeDungeon_transparent.png', 2, 2))
                if i % 7 == 0 and j % 2 == 0:
                    self.tiled_memory[i][j].decor_objects.append(
                        self.rl.get_sprite('roguelikeDungeon_transparent.png', 0, 2))
        self.tiled_memory[6][6].decor_objects.append(self.rl.get_sprite('roguelikeDungeon_transparent.png', 0, 0))

    def notify(self, message):
        if message[0] == 'MAP':
            player_x = message[1]
            player_y = message[2]

            ret = [[Tile() for _2 in range(CLIENT_GRID_MEMORY_SIZE[0])] for _ in range(CLIENT_GRID_MEMORY_SIZE[1])]

            for j in range(player_y - int(CLIENT_GRID_MEMORY_SIZE[1] / 2), player_y + int(CLIENT_GRID_MEMORY_SIZE[1] / 2)):
                for i in range(player_x - int(CLIENT_GRID_MEMORY_SIZE[0] / 2), player_x + int(CLIENT_GRID_MEMORY_SIZE[0] / 2)):
                    if i < 0 or j < 0 or i >= GRID_MEMORY_SIZE[0] or j >= GRID_MEMORY_SIZE[1]:
                        continue
                    ret[j - (player_y - int(CLIENT_GRID_MEMORY_SIZE[1] / 2))][i - int(player_x - int(CLIENT_GRID_MEMORY_SIZE[0] / 2))] = self.tiled_memory[j][i]

            self.channel.push(['MAP', player_x, player_y, ret])
        if message[0] == 'START':
            self.notify(['MAP', 6, 6])
            self.channel.push(['POS', 6, 6])
