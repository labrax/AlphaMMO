# -*- coding: utf-8 -*-

import time
import random
import stackless

from server_util.server_tasklet import AlphaServerTasklet
from util.alpha_protocol import AlphaProtocol


class AlphaServerNPCTasklet(AlphaServerTasklet):
    """
    Handles the actions for a NPC
    AlphaServerNPCTasklet.entity is the entity data
    """
    def __init__(self, server, entity):
        super(AlphaServerNPCTasklet, self).__init__(server)
        self.entity = entity

    def iterate(self):
        super(AlphaServerNPCTasklet, self).iterate()

    def run(self):
        self.last_time = time.time()
        while self.running:
            '''if time.time() - self.last_time > 8:
                # push to all nearby
                for i in self.server.get_nearby_entities(self.entity.entity_id):
                    goal = self.server.get_tasklet(i.entity_id)
                    if goal:
                        goal.channel.push(
                            ['SAY', 'Hello?', self.entity])
                self.last_time = time.time()'''
            self.iterate()
            if not self.entity.start_movement:
                if True:
                    if random.choice([True, False]):
                        if random.choice([True, False]):
                            if self.server.server_map.is_valid_movement([self.entity.pos[0] + 1, self.entity.pos[1]]):
                                self.entity.set_movement(+1, 0)
                        else:
                            if self.server.server_map.is_valid_movement([self.entity.pos[0] - 1, self.entity.pos[1]]):
                                self.entity.set_movement(-1, 0)
                    else:
                        if random.choice([True, False]):
                            if self.server.server_map.is_valid_movement([self.entity.pos[0], self.entity.pos[1] + 1]):
                                self.entity.set_movement(0, +1)
                        else:
                            if self.server.server_map.is_valid_movement([self.entity.pos[0], self.entity.pos[1] - 1]):
                                self.entity.set_movement(0, -1)
                    # push to all nearby
                    for i in self.server.get_nearby_entities(self.entity.entity_id):
                        if i.player_controlled:
                            goal = self.server.get_tasklet(i.entity_id)
                            if goal:
                                goal.channel.push(
                                    [AlphaProtocol.SET_ENTITIES, [self.entity]])
            stackless.schedule()

    def notify(self, message):
        pass
