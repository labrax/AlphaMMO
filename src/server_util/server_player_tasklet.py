# -*- coding: utf-8 -*-

import os
import sys
import stackless

from util.alpha_exceptions import InvalidLogin, InvalidPassword, InvalidValue
from server_util.server_tasklet import AlphaServerTasklet
from util.alpha_socket_comm import send_receive
from util.alpha_protocol import AlphaProtocol, retrieve_with_types


class AlphaServerPlayerTasklet(AlphaServerTasklet):
    def __init__(self, server, client_socket, address):
        super(AlphaServerPlayerTasklet, self).__init__(server)
        self.client_socket = client_socket
        self.address = address
        self.socket_buffer = ''.encode()
        self.session_id = -1
        self.ping = 0.1  # todo: implement
        self.session_token = None  # todo: implement
        self.server = server
        self.messages_handlers = {AlphaProtocol.REGISTER: self.msg_register, AlphaProtocol.LOGIN: self.msg_login, AlphaProtocol.REQUEST_MOVE: self.msg_rqst_move}

    def iterate(self):
        super(AlphaServerPlayerTasklet, self).iterate()

    def run(self):
        while self.running:
            self.iterate()
            send_receive(self, True)
            stackless.schedule()

        def _disconnected():
            self.client_socket.close()
            if self.entity:
                # we will get the list of nearbies to notify upon logout:
                nearby = self.server.get_nearby_entities(self.entity.entity_id)
                self.server.server_map.remove_entity(self.entity)

                # notify nearbies
                for i in nearby:
                    if i.player_controlled:
                        goal = self.server.get_tasklet(i.entity_id)
                        if goal:
                            goal.channel.push(
                                [AlphaProtocol.REPLACE_ENTITIES, self.server.get_nearby_entities(i.entity_id)])
                # this way when we lose connection to the server the player gets disconnected
        _disconnected()
        stackless.schedule_remove()

    def msg_register(self, message):
        user = message[1]
        passwd = message[2]
        email = message[3]
        try:
            if self.server.server_database.create_account(user, passwd, email):
                self.channel.push([AlphaProtocol.STATUS, 1, self.session_id])
        except InvalidValue as e:
            self.channel.push([AlphaProtocol.STATUS, -1, self.session_id])
            self.channel.push([AlphaProtocol.SERVER_MESSAGE, e.args[0]])

    def msg_login(self, message):
        user = message[1]
        passwd = message[2]
        try:
            if self.server.server_database.login_account(user, passwd):
                self.entity = self.server.server_entities.create_random_player()
                player_x = self.entity.pos[0]
                player_y = self.entity.pos[1]
                self.entity.name = message[1]
                self.session_id = self.entity.entity_id
                self.server.set_tasklet(self.entity.entity_id, self)
                self.server.server_map.set_entity(self.entity)

                self.channel.push([AlphaProtocol.STATUS, 1, self.session_id])
                self.channel.push([AlphaProtocol.RECEIVE_PLAYER, self.server.get_entity(self.session_id)])
                self.channel.push([AlphaProtocol.TELEPORT, player_x, player_y])

                ret = self.server.server_map.prepare_map(player_x, player_y)
                self.channel.push([AlphaProtocol.RECEIVE_MAP, player_x, player_y, ret])

                self.channel.push(
                    [AlphaProtocol.SET_ENTITIES, self.server.get_nearby_entities(self.entity.entity_id)])

                for i in self.server.get_nearby_entities(self.entity.entity_id):
                    if i.player_controlled:
                        goal = self.server.get_tasklet(i.entity_id)
                        if goal:
                            goal.channel.push([AlphaProtocol.SET_ENTITIES, [self.entity]])
        except InvalidLogin:
            self.channel.push([AlphaProtocol.STATUS, -2, self.session_id])
        except InvalidPassword:
            self.channel.push([AlphaProtocol.STATUS, -2, self.session_id])

    def msg_rqst_move(self, message):
        player_x = int(message[1])
        player_y = int(message[2])
        if -1 <= player_x - self.entity.pos[0] <= 1 and -1 <= player_y - self.entity.pos[
            1] <= 1 and not self.entity.start_movement and self.server.server_map.is_valid_movement(
            (player_x, player_y)) \
                and (player_x - self.entity.pos[0] != 0 or player_y - self.entity.pos[1] != 0):
            # print('valid', self.entity.pos, (player_x, player_y))

            self.entity.set_movement(player_x - self.entity.pos[0], player_y - self.entity.pos[1])
            self.channel.push([AlphaProtocol.MOVING, player_x, player_y])
            self.channel.push([AlphaProtocol.SET_ENTITIES, self.server.get_nearby_entities(self.entity.entity_id)])
            for i in self.server.get_nearby_entities(self.entity.entity_id):
                if i.player_controlled:
                    goal = self.server.get_tasklet(i.entity_id)
                    if goal:
                        goal.channel.push([AlphaProtocol.SET_ENTITIES, [self.entity]])
        else:
            # print('invalid', self.entity.pos, (player_x, player_y))
            self.channel.push([AlphaProtocol.MOVING, self.entity.pos[0], self.entity.pos[1]])
            ret = self.server.server_map.prepare_map(self.entity.pos[0], self.entity.pos[1])
            self.channel.push([AlphaProtocol.RECEIVE_MAP, self.entity.pos[0], self.entity.pos[1], ret])

    def msg_rqst_action(self, message):
        self.channel.push([AlphaProtocol.ACTION, 1])
        effect = self.server.server_entities.create_effect((message[2], message[3]))

        self.channel.push([AlphaProtocol.EFFECT, effect, message[2], message[3]])
        for i in self.server.get_nearby_entities(self.entity.entity_id):
            if i.player_controlled:
                goal = self.server.get_tasklet(i.entity_id)
                if goal:
                    goal.channel.push([AlphaProtocol.EFFECT, effect, message[2], message[3]])

    def to_server(self, message):
        print(self.__class__.__name__, "SERVER RAW", self.session_id, message)
        try:
            message = retrieve_with_types(message, True)
            print('SERVER RECEIVED', message)
            if message[0] in self.messages_handlers:
                self.messages_handlers[message[0]](message)
            else:
                print("MESSAGE UNIDENTIFIED AT", self.__class__.__name__, message)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, e, fname, exc_tb.tb_lineno)
