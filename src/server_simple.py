# -*- coding: utf-8 -*-

import random
import stackless
import time

from server_util.server_entities import ServerTile as Tile
from util.alpha_communication import AlphaCommunicationMember
from util.alpha_defines import GRID_MEMORY_SIZE, GRID_MEMORY_SIZE as CLIENT_GRID_MEMORY_SIZE, SPRITE_LEN as TILE_SIZE
from util.alpha_entities import Entity as ServerEntity
from util.resource_loader import AlphaResourceLoader


class ClientAsServer(AlphaCommunicationMember):
    def __init__(self):
        # to write back
        self.channel = None

        # to load some resources
        self.rl = AlphaResourceLoader()

        self.tiled_memory = None
        self.all_entities = None
        self.p0 = None

        self.running = True

        self.start()

    def start(self):
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

        self.all_entities = dict()
        p0 = ServerEntity()
        p0.pos = (6, 6)
        p0.sprite = self.rl.get_sprite('roguelikeChar_transparent.png', 0, 8)
        p0.entity_id = 1
        p0.speed_pixels = 16 * 5
        p0.player_controlled = True
        p0.name = "It's me"

        self.p0 = p0

        p1 = ServerEntity()
        p1.pos = (5, 6)
        p1.sprite = self.rl.get_sprite('roguelikeChar_transparent.png', 1, 9)
        p1.entity_id = 2
        p1.speed_pixels = 8
        p1.movement = (4, 6)
        p1.start_movement = time.time()
        p1.name = 'AaaN'
        self.tiled_memory[6][5].entities.append(p1)

        p2 = ServerEntity()
        p2.pos = (2, 2)
        p2.sprite = self.rl.get_sprite('roguelikeChar_transparent.png', 0, 7)
        p2.entity_id = 3
        p2.speed_pixels = 4
        p2.movement = (1, 1)
        p2.start_movement = time.time()
        p2.name = 'Bbbhashashahsa'
        self.tiled_memory[2][2].entities.append(p2)

        for i in [p0, p1, p2]:
            self.all_entities[i.entity_id] = i

    def get_entities(self, curr_entity):
        curr_entity = self.all_entities[curr_entity]
        ret_entities = list()
        for j in range(curr_entity.pos[1] - int(GRID_MEMORY_SIZE[1] / 2), curr_entity.pos[1] + int(GRID_MEMORY_SIZE[1] / 2)):
            for i in range(curr_entity.pos[0] - int(GRID_MEMORY_SIZE[0] / 2), curr_entity.pos[0] + int(GRID_MEMORY_SIZE[0] / 2)):
                if 0 <= i < GRID_MEMORY_SIZE[0] and 0 <= j < GRID_MEMORY_SIZE[1]:
                    for elem in self.tiled_memory[j][i].entities:
                        if elem is not curr_entity:
                            ret_entities.append(elem)
        return ret_entities

    def get_player(self, session_id):
        return self.all_entities[session_id]

    def run(self):
        last_time = time.time()
        while self.running:
            this_time = time.time()
            for i in self.all_entities.values():
                if i.player_controlled:
                    continue

                if time.time() - last_time > 8:
                    # TODO: push to all nearby
                    self.channel.push(['SAY', 'Hello?' + str(random.random()), i])
                    last_time = time.time()
                if i.start_movement:
                    if (this_time - i.start_movement) * i.speed_pixels > TILE_SIZE:
                        self.tiled_memory[i.pos[1]][i.pos[0]].entities.remove(i)
                        i.pos = (i.movement[0], i.movement[1])
                        self.tiled_memory[i.pos[1]][i.pos[0]].entities.append(i)
                        i.start_movement = None
                        #TODO: push to all nearby
                        self.channel.push(['CURR_ENTITIES', self.get_entities(self.p0.entity_id)])
                else:
                    if random.choice([True, False, False, False]):
                        #TODO: push to all nearby
                        if random.choice([True, False]):
                            if random.choice([True, False]):
                                if 0 <= i.pos[0] + 1 < GRID_MEMORY_SIZE[0] and 0 <= i.pos[1] < GRID_MEMORY_SIZE[1]:
                                    i.set_movement(+1, 0)
                            else:
                                if 0 <= i.pos[0] - 1 < GRID_MEMORY_SIZE[0] and 0 <= i.pos[1] < GRID_MEMORY_SIZE[1]:
                                    i.set_movement(-1, 0)
                        else:
                            if random.choice([True, False]):
                                if 0 <= i.pos[0] < GRID_MEMORY_SIZE[0] and 0 <= i.pos[1] + 1 < GRID_MEMORY_SIZE[1]:
                                    i.set_movement(0, +1)
                            else:
                                if 0 <= i.pos[0] < GRID_MEMORY_SIZE[0] and 0 <= i.pos[1] - 1 < GRID_MEMORY_SIZE[1]:
                                    i.set_movement(0, -1)
                        self.channel.push(['CURR_ENTITIES', self.get_entities(self.p0.entity_id)])
            stackless.schedule()

    def notify(self, message):
        session_id = message[0]
        if message[1] == 'MAP':
            player_x = message[2]
            player_y = message[3]

            ret = [[Tile() for _2 in range(CLIENT_GRID_MEMORY_SIZE[0])] for _ in range(CLIENT_GRID_MEMORY_SIZE[1])]

            for j in range(player_y - int(CLIENT_GRID_MEMORY_SIZE[1] / 2), player_y + int(CLIENT_GRID_MEMORY_SIZE[1] / 2)):
                for i in range(player_x - int(CLIENT_GRID_MEMORY_SIZE[0] / 2), player_x + int(CLIENT_GRID_MEMORY_SIZE[0] / 2)):
                    if i < 0 or j < 0 or i >= GRID_MEMORY_SIZE[0] or j >= GRID_MEMORY_SIZE[1]:
                        continue
                    ret[j - (player_y - int(CLIENT_GRID_MEMORY_SIZE[1] / 2))][i - int(player_x - int(CLIENT_GRID_MEMORY_SIZE[0] / 2))] = self.tiled_memory[j][i]

            self.channel.push(['MAP', player_x, player_y, ret])
            self.channel.push(['CURR_ENTITIES', self.get_entities(session_id)])
        elif message[1] == 'START':
            self.channel.push(['PLAYER', self.get_player(session_id)])
            self.channel.push(['POS', 6, 6])
            self.channel.push(['CURR_ENTITIES', self.get_entities(session_id)])
            self.notify([session_id, 'MAP', 6, 6])
        elif message[1] == 'SAY':
            self.channel.push(['SAY', message[2], self.get_player(session_id)])
        else:
            print("MESSAGE UNIDENTIFIED AT", self.__class__.__name__, message)
