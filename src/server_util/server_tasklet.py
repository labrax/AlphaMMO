# -*- coding: utf-8 -*-

import time

from util.alpha_communication import AlphaCommunicationChannel
from util.alpha_protocol import AlphaProtocol
from util.alpha_defines import SPRITE_LEN as TILE_SIZE


class AlphaServerTasklet(AlphaCommunicationChannel):
    def __init__(self, server):
        # the handler for each entity will be a channel itself, when running it will solve the destination to the
        # socket address
        super(AlphaServerTasklet, self).__init__(None)
        self.channel = self  # quick fix
        self.last_time = None
        self.entity = None
        self.tasklet = None
        self.running = True
        self.server = server

    def iterate(self):
        this_time = time.time()
        if self.entity and self.entity.start_movement:
            if (this_time - self.entity.start_movement) * self.entity.speed_pixels > TILE_SIZE:
                self.server.server_map.move_entity(self.entity, self.entity.pos, self.entity.movement)
                self.entity.pos = (self.entity.movement[0], self.entity.movement[1])

                self.entity.start_movement = None
                # push to all nearby
                for i in self.server.get_nearby_entities(self.entity.entity_id):
                    if i.player_controlled:
                        goal = self.server.get_tasklet(i.entity_id)
                        if goal:
                            goal.channel.push([AlphaProtocol.SET_ENTITIES, [self.entity]])

                if self.entity.player_controlled:
                    ret = self.server.server_map.prepare_map(self.entity.pos[0], self.entity.pos[1])
                    self.channel.push(
                        [AlphaProtocol.RECEIVE_MAP, self.entity.pos[0], self.entity.pos[1], ret])

    def notify(self, message):
        pass
