# -*- coding: utf-8 -*-

import time
import random
import stackless

from server_util.server_tasklet import AlphaServerTasklet
from util.alpha_protocol import AlphaProtocol
from util.alpha_defines import GRID_MEMORY_SIZE, GRID_MEMORY_SIZE as CLIENT_GRID_MEMORY_SIZE, SPRITE_LEN as TILE_SIZE


class AlphaServerNPCTasklet(AlphaServerTasklet):
    def __init__(self, server, entity):
        super(AlphaServerNPCTasklet, self).__init__()
        self.entity = entity
        self.server = server

    def run(self):
        self.last_time = time.time()
        while self.running:
            this_time = time.time()
            '''if time.time() - self.last_time > 8:
                # push to all nearby
                for i in self.server.get_nearby_entities(self.entity.entity_id):
                    goal = self.server.get_tasklet(i.entity_id)
                    if goal:
                        goal.channel.push(
                            ['SAY', 'Hello?', self.entity])
                self.last_time = time.time()'''

            if self.entity.start_movement:
                if (this_time - self.entity.start_movement) * self.entity.speed_pixels > TILE_SIZE:
                    self.server.server_map.tiled_memory[self.entity.pos[1]][self.entity.pos[0]].entities.remove(self.entity)
                    self.entity.pos = (self.entity.movement[0], self.entity.movement[1])
                    self.server.server_map.tiled_memory[self.entity.pos[1]][self.entity.pos[0]].entities.add(self.entity)
                    self.entity.start_movement = None
                    # push to all nearby
                    for i in self.server.get_nearby_entities(self.entity.entity_id):
                        if i.player_controlled:
                            goal = self.server.get_tasklet(i.entity_id)
                            if goal:
                                goal.channel.push(
                                    [AlphaProtocol.SET_ENTITIES, [self.entity]])
            else:
                if True:
                    if random.choice([True, False]):
                        if random.choice([True, False]):
                            if 0 <= self.entity.pos[0] + 1 < GRID_MEMORY_SIZE[0] and 0 <= self.entity.pos[1] < GRID_MEMORY_SIZE[1]:
                                self.entity.set_movement(+1, 0)
                        else:
                            if 0 <= self.entity.pos[0] - 1 < GRID_MEMORY_SIZE[0] and 0 <= self.entity.pos[1] < GRID_MEMORY_SIZE[1]:
                                self.entity.set_movement(-1, 0)
                    else:
                        if random.choice([True, False]):
                            if 0 <= self.entity.pos[0] < GRID_MEMORY_SIZE[0] and 0 <= self.entity.pos[1] + 1 < GRID_MEMORY_SIZE[1]:
                                self.entity.set_movement(0, +1)
                        else:
                            if 0 <= self.entity.pos[0] < GRID_MEMORY_SIZE[0] and 0 <= self.entity.pos[1] - 1 < GRID_MEMORY_SIZE[1]:
                                self.entity.set_movement(0, -1)
                    # push to all nearby
                    for i in self.server.get_nearby_entities(self.entity.entity_id):
                        if i.player_controlled:
                            goal = self.server.get_tasklet(i.entity_id)
                            if goal:
                                goal.channel.push(
                                    [AlphaProtocol.SET_ENTITIES, [self.entity]])
            stackless.schedule()
