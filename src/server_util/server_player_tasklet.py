# -*- coding: utf-8 -*-

import time
import os
import sys
import select
import stackless
import pickle

from util.alpha_exceptions import InvalidLogin, InvalidPassword
from server_util.server_tasklet import AlphaServerTasklet
from server_util.alpha_server_defines import SOCKET_BUFFER
from util.alpha_protocol import AlphaProtocol, retrieve_with_types
from util.alpha_defines import SPRITE_LEN as TILE_SIZE


class AlphaServerPlayerTasklet(AlphaServerTasklet):
    def __init__(self, server, client_socket, address):
        super(AlphaServerPlayerTasklet, self).__init__()
        self.client_socket = client_socket
        self.address = address
        self.socket_buffer = ''.encode()
        self.session_id = -1
        self.ping = 0.1  # todo: implement
        self.session_token = None  # todo: implement
        self.server = server

    def comm(self):
        rr, rw, err = select.select([self.client_socket], list(), list(), 0)
        if len(rr) > 0:
            try:
                input = self.client_socket.recv(SOCKET_BUFFER)
                if input:
                    self.socket_buffer += input
                    # read message one by one
                    read = True
                    while read:
                        read = False
                        if b' ' in self.socket_buffer:
                            size = self.socket_buffer.split(b' ')[0]
                            len_size = len(size)

                            size = int(size)

                            if len_size + 1 + size >= len(self.socket_buffer):
                                read = True
                                current_read = self.socket_buffer[len_size + 1: len_size + 1 + size]
                                self.socket_buffer = self.socket_buffer[len_size + 1 + size:]
                                data = [i.decode() for i in current_read.split(b' ')]
                                data[0] = AlphaProtocol(int(data[0]))
                                # print("Server receiving from client", data)
                                self.to_server(data)
                else:
                    self.running = False
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, e, fname, exc_tb.tb_lineno)
                # something went wrong, player is now offline - needs to re-establish connection
                self.running = False
        try:
            # sending each packet is heavy (I/O is heavy)
            # so we will put everything in a single packet: < time with ssl
            send_buffer = b''
            while self.queue.qsize() > 0:
                data = pickle.dumps(self.queue.get())
                # print("Server sending", data)
                next_packet = str(len(data)).encode() + b' ' + data
                if len(send_buffer) > 0 and len(send_buffer) + len(next_packet) > SOCKET_BUFFER:
                    self.client_socket.send(send_buffer)
                    send_buffer = b''
                send_buffer += next_packet
            if len(send_buffer) > 0:
                self.client_socket.send(send_buffer)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, e, fname, exc_tb.tb_lineno)
            # something went wrong, player is now offline - needs to re-establish connection
            self.running = False

    def iterate(self):
        this_time = time.time()
        if self.entity:
            if self.entity.start_movement:
                if (this_time - self.entity.start_movement) * self.entity.speed_pixels > TILE_SIZE:
                    self.server.server_map.tiled_memory[self.entity.pos[1]][
                        self.entity.pos[0]].entities.remove(self.entity)
                    self.entity.pos = (self.entity.movement[0], self.entity.movement[1])
                    self.server.server_map.tiled_memory[self.entity.pos[1]][self.entity.pos[0]].entities.add(
                        self.entity)
                    self.entity.start_movement = None

                    ret = self.server.server_map.prepare_map(self.entity.pos[0], self.entity.pos[1])
                    self.channel.push(
                        [AlphaProtocol.RECEIVE_MAP, self.entity.pos[0], self.entity.pos[1], ret])

                    # push to all nearby
                    for i in self.server.get_nearby_entities(self.entity.entity_id):
                        if i.player_controlled:
                            goal = self.server.get_tasklet(i.entity_id)
                            if goal:
                                goal.channel.push(
                                    [AlphaProtocol.SET_ENTITIES, self.server.get_nearby_entities(i.entity_id)])

    def run(self):
        while self.running:
            self.iterate()
            self.comm()
            stackless.schedule()
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
        stackless.schedule_remove()

    def to_server(self, message):
        print(self.__class__.__name__, "SERVER RAW", self.session_id, message)
        try:
            message = retrieve_with_types(message, True)
            print('SERVER RECEIVED', message)
            if message[0] == AlphaProtocol.REGISTER:
                user = message[1]
                passwd = message[2]
                email = message[3]

                try:
                    if self.server.server_database.create_account(user, passwd, email):
                        self.channel.push([AlphaProtocol.STATUS, 1, self.session_id])
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, e, fname, exc_tb.tb_lineno)
                    self.channel.push([AlphaProtocol.STATUS, -1, self.session_id])
            elif message[0] == AlphaProtocol.LOGIN:
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

                        self.channel.push([AlphaProtocol.SET_ENTITIES, self.server.get_nearby_entities(self.entity.entity_id)])

                        for i in self.server.get_nearby_entities(self.entity.entity_id):
                            if i.player_controlled:
                                goal = self.server.get_tasklet(i.entity_id)
                                if goal:
                                    goal.channel.push([AlphaProtocol.SET_ENTITIES, [self.entity]])
                except InvalidLogin:
                    self.channel.push([AlphaProtocol.STATUS, -2, self.session_id])
                except InvalidPassword:
                    self.channel.push([AlphaProtocol.STATUS, -2, self.session_id])
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, e, fname, exc_tb.tb_lineno)
            elif message[0] == AlphaProtocol.REQUEST_MOVE:
                player_x = int(message[1])
                player_y = int(message[2])
                if -1 <= player_x - self.entity.pos[0] <= 1 and -1 <= player_y - self.entity.pos[1] <= 1 and not self.entity.start_movement and self.server.server_map.is_valid_movement((player_x, player_y))\
                        and (player_x - self.entity.pos[0] != 0 or player_y - self.entity.pos[1] != 0):
                    #print('valid', self.entity.pos, (player_x, player_y))

                    self.entity.set_movement(player_x - self.entity.pos[0], player_y - self.entity.pos[1])
                    self.channel.push([AlphaProtocol.MOVING, player_x, player_y])
                    self.channel.push([AlphaProtocol.SET_ENTITIES, self.server.get_nearby_entities(self.entity.entity_id)])
                    for i in self.server.get_nearby_entities(self.entity.entity_id):
                        if i.player_controlled:
                            goal = self.server.get_tasklet(i.entity_id)
                            if goal:
                                goal.channel.push([AlphaProtocol.SET_ENTITIES, [self.entity]])
                else:
                    #print('invalid', self.entity.pos, (player_x, player_y))
                    self.channel.push([AlphaProtocol.MOVING, self.entity.pos[0], self.entity.pos[1]])
                    ret = self.server.server_map.prepare_map(self.entity.pos[0], self.entity.pos[1])
                    self.channel.push([AlphaProtocol.RECEIVE_MAP, self.entity.pos[0], self.entity.pos[1], ret])
            elif message[0] == AlphaProtocol.REQUEST_ACTION:
                self.channel.push([AlphaProtocol.ACTION, 1])
                effect = self.server.server_entities.create_effect((message[2], message[3]))

                self.channel.push([AlphaProtocol.EFFECT, effect, message[2], message[3]])
                for i in self.server.get_nearby_entities(self.entity.entity_id):
                    if i.player_controlled:
                        goal = self.server.get_tasklet(i.entity_id)
                        if goal:
                            goal.channel.push([AlphaProtocol.EFFECT, effect, message[2], message[3]])
            else:
                print("MESSAGE UNIDENTIFIED AT", self.__class__.__name__, message)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, e, fname, exc_tb.tb_lineno)
