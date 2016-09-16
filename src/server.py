# -*- coding: utf-8 -*-

import sys
import os

import random
import stackless
import time

import socket
import select
import ssl
import pickle

from server_util.alpha_server_defines import HOST_BIND, PORT_BIND, MAX_SERVER_CONN, CERTIFICATE_FILE, KEY_FILE, SOCKET_BUFFER
from util.alpha_entities import Tile
from server_util.server_map import AlphaServerMap
from util.alpha_communication import AlphaCommunicationChannel
from util.alpha_defines import GRID_MEMORY_SIZE, GRID_MEMORY_SIZE as CLIENT_GRID_MEMORY_SIZE, SPRITE_LEN as TILE_SIZE

from util.alpha_exceptions import SingletonViolated

from server_util.server_entities import AlphaServerEntities


class AlphaServerTasklet(AlphaCommunicationChannel):
    def __init__(self):
        # the handler for each entity will be a channel itself, when running it will solve the destination to the
        # socket address
        super(AlphaServerTasklet, self).__init__(None)
        self.channel = self  # quick fix
        self.last_time = None
        self.entity = None
        self.tasklet = None
        self.running = True

    def iterate(self):
        pass

    def notify(self, message):
        pass


class AlphaServerPlayerTasklet(AlphaServerTasklet):
    def __init__(self, client_socket, address):
        super(AlphaServerPlayerTasklet, self).__init__()
        self.client_socket = client_socket
        self.address = address
        self.socket_buffer = ''.encode()
        self.session_id = -1

    def run(self):
        while self.running:
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
                while self.queue.qsize() > 0:
                    data = pickle.dumps(self.queue.get())
                    # print("Server sending", data)
                    self.client_socket.send(str(len(data)).encode() + b' ' + data)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, e, fname, exc_tb.tb_lineno)
                # something went wrong, player is now offline - needs to re-establish connection
                self.running = False
            stackless.schedule()
        self.client_socket.close()
        try:
            AlphaServer.__instance__.server_map.remove_entity(self.entity)
        except:
            pass
        # this way when we lose connection to the server the player gets disconnected
        stackless.schedule_remove()

    def to_server(self, message):
        print("server recv", self.session_id, message)
        try:
            if message[1] == 'MAP':
                player_x = int(message[2])
                player_y = int(message[3])

                ret = [[Tile() for _2 in range(CLIENT_GRID_MEMORY_SIZE[0])] for _ in range(CLIENT_GRID_MEMORY_SIZE[1])]
                for j in range(player_y - int(CLIENT_GRID_MEMORY_SIZE[1] / 2),
                               player_y + int(CLIENT_GRID_MEMORY_SIZE[1] / 2)):
                    for i in range(player_x - int(CLIENT_GRID_MEMORY_SIZE[0] / 2),
                                   player_x + int(CLIENT_GRID_MEMORY_SIZE[0] / 2)):
                        if i < 0 or j < 0 or i >= GRID_MEMORY_SIZE[0] or j >= GRID_MEMORY_SIZE[1]:
                            continue
                        ret[j - (player_y - int(CLIENT_GRID_MEMORY_SIZE[1] / 2))][
                            i - int(player_x - int(CLIENT_GRID_MEMORY_SIZE[0] / 2))] = \
                        AlphaServer.__instance__.server_map.tiled_memory[j][i]

                self.channel.push(['MAP', player_x, player_y, ret])
                self.channel.push(['CURR_ENTITIES', AlphaServer.__instance__.get_nearby_entities(self.session_id)])
            elif message[1] == 'START':
                self.entity = AlphaServer.__instance__.server_entities.create_random_player()
                self.entity.name = message[2]
                self.session_id = self.entity.entity_id
                AlphaServer.__instance__.set_tasklet(self.entity.entity_id, self)
                AlphaServer.__instance__.server_map.set_entity(self.entity)

                self.channel.push(['PLAYER', AlphaServer.__instance__.get_entity(self.session_id)])
                self.channel.push(['POS', 6, 6])
                self.to_server([self.session_id, 'MAP', 6, 6])
            elif message[1] == 'SAY':
                self.channel.push(['SAY', message[2], AlphaServer.__instance__.get_entity(self.session_id)])
            else:
                print("MESSAGE UNIDENTIFIED AT", self.__class__.__name__, message)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, e, fname, exc_tb.tb_lineno)


class AlphaServerNPCTasklet(AlphaServerTasklet):
    def __init__(self, entity):
        super(AlphaServerNPCTasklet, self).__init__()
        self.entity = entity

    def run(self):
        self.last_time = time.time()
        while self.running:
            this_time = time.time()
            '''if time.time() - self.last_time > 8:
                # push to all nearby
                for i in AlphaServer.__instance__.get_nearby_entities(self.entity.entity_id):
                    goal = AlphaServer.__instance__.get_tasklet(i.entity_id)
                    if goal:
                        goal.channel.push(
                            ['SAY', 'Hello?', self.entity])
                self.last_time = time.time()'''

            if self.entity.start_movement:
                if (this_time - self.entity.start_movement) * self.entity.speed_pixels > TILE_SIZE:
                    AlphaServer.__instance__.server_map.tiled_memory[self.entity.pos[1]][self.entity.pos[0]].entities.remove(self.entity)
                    self.entity.pos = (self.entity.movement[0], self.entity.movement[1])
                    AlphaServer.__instance__.server_map.tiled_memory[self.entity.pos[1]][self.entity.pos[0]].entities.add(self.entity)
                    self.entity.start_movement = None
                    # push to all nearby
                    for i in AlphaServer.__instance__.get_nearby_entities(self.entity.entity_id):
                        if i.player_controlled:
                            goal = AlphaServer.__instance__.get_tasklet(i.entity_id)
                            if goal:
                                goal.channel.push(
                                    ['ADD_ENTITIES', [self.entity]])
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
                    for i in AlphaServer.__instance__.get_nearby_entities(self.entity.entity_id):
                        if i.player_controlled:
                            goal = AlphaServer.__instance__.get_tasklet(i.entity_id)
                            if goal:
                                goal.channel.push(
                                    ['ADD_ENTITIES', [self.entity]])
            stackless.schedule()


class AlphaServer:
    __instance__ = None

    def __init__(self):
        if AlphaServer.__instance__:
            raise SingletonViolated(self.__class__.__name__)
        else:
            AlphaServer.__instance__ = self
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((HOST_BIND, PORT_BIND))
        self.server_socket.listen(MAX_SERVER_CONN)

        self.server_map = AlphaServerMap()
        self.server_entities = AlphaServerEntities()

        self.running = False

        self.tasklets_objects = list()
        self.tasklets_entities = dict()

    def start(self):
        # server setup
        self.server_map.start()

        # start entities tasklet
        for _ in range(5):
            i = self.server_entities.create_random_npc()
            self.server_map.set_entity(i)
            tasklet_object = AlphaServerNPCTasklet(i)
            self.tasklets_objects.append(tasklet_object)
            tasklet_object.tasklet = stackless.tasklet(tasklet_object.run)()

        # server run
        self.running = True
        stackless.tasklet(self.run)()
        stackless.run()

    def run(self):
        ITERATION_TIME = 1/60
        while self.running:
            last_time = time.time()
            rr, rw, err = select.select([self.server_socket], list(), list(), 0)

            # we have a client connecting
            if len(rr) > 0:
                try:
                    client_socket, address = self.server_socket.accept()
                    print("Client connecting", address)
                    client_socket = ssl.wrap_socket(client_socket, server_side=True, ssl_version=ssl.PROTOCOL_TLSv1,
                                                    certfile=CERTIFICATE_FILE, keyfile=KEY_FILE)

                    tasklet_object = AlphaServerPlayerTasklet(client_socket, address)
                    self.tasklets_objects.append(tasklet_object)
                    tasklet_object.tasklet = stackless.tasklet(tasklet_object.run)()
                except:
                    print("Client failed.")

            stackless.schedule()
            elapsed = time.time() - last_time
            if elapsed < ITERATION_TIME:
                time.sleep(ITERATION_TIME - elapsed)

        self.server_socket.close()

    def get_nearby_entities(self, curr_entity):
        return self.server_map.get_nearby_entities(curr_entity)

    def get_entity(self, entity_id):
        return self.server_map.get_entity(entity_id)

    def set_entity(self, entity):
        self.server_map.set_entity(entity)

    def get_tasklet(self, entity_id):
        return self.tasklets_entities.get(entity_id, None)

    def set_tasklet(self, entity_id, tasklet):
        self.tasklets_entities[entity_id] = tasklet

if __name__ == '__main__':
    AlphaServer.__instance__ = AlphaServer()
    AlphaServer.__instance__.start()
