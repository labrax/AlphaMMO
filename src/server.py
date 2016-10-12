#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import stackless
import time

import socket
import select
import ssl

from server_util.alpha_server_defines import HOST_BIND, PORT_BIND, MAX_SERVER_CONN, CERTIFICATE_FILE, KEY_FILE, SERVER_ITERATION_TIME
from server_util.server_map import AlphaServerMap

from util.alpha_exceptions import SingletonViolated

from server_util.server_npc_tasklet import AlphaServerNPCTasklet
from server_util.server_player_tasklet import AlphaServerPlayerTasklet
from server_util.server_database import AlphaDatabase

from server_util.server_entities_factory import AlphaServerEntitiesFactory


class AlphaServer:
    """
    The game server side for the game
    AlphaServer.server_socket is the listener socket
    AlphaServer.server_database is the database
    AlphaServer.server_map is the map
    AlphaServer.server_entities is the entities factory
    AlphaServer.running holds information if the tasklet should stop running
    AlphaServer.tasklets_objects is the relation of tasklets
    AlphaServer.tasklets_entities if the relation of entities to tasklets
    """
    __instance__ = None

    def __init__(self):
        if AlphaServer.__instance__:
            raise SingletonViolated(self.__class__.__name__)
        else:
            AlphaServer.__instance__ = self
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((HOST_BIND, PORT_BIND))

        self.server_database = AlphaDatabase()

        self.server_map = AlphaServerMap()
        self.server_entities = AlphaServerEntitiesFactory()

        self.running = False

        self.tasklets_objects = list()
        self.tasklets_entities = dict()

    def start(self):
        """
        Starts the server:
            - starts the map
            - start the npcs
            - put the socket to listen
            - start stackless
        :return: nothing
        """
        # server setup
        self.server_map.start()

        def start_npc():
            """
            Starts a random NPC
            :return: nothing
            """
            i = self.server_entities.create_random_npc()
            self.server_map.set_entity(i)
            tasklet_object = AlphaServerNPCTasklet(self, i)
            self.tasklets_objects.append(tasklet_object)
            tasklet_object.tasklet = stackless.tasklet(tasklet_object.run)()

        # start entities tasklet
        for _ in range(5):
            start_npc()

        # server run
        self.server_socket.listen(MAX_SERVER_CONN)
        self.running = True
        stackless.tasklet(self.run)()
        stackless.run()

    def run(self):
        """
        Runs the handler. Ends when AlphaServer.running = False
        This method uses the stackless scheduler
        :return: nothing
        """
        print("Server is running.")
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

                    tasklet_object = AlphaServerPlayerTasklet(self, client_socket, address)
                    self.tasklets_objects.append(tasklet_object)
                    tasklet_object.tasklet = stackless.tasklet(tasklet_object.run)()
                except Exception as e:
                    import sys
                    import os
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, e, fname, exc_tb.tb_lineno)
                    print("Client failed.")

            stackless.schedule()
            elapsed = time.time() - last_time
            #print("FPS", 1/elapsed)
            if elapsed < SERVER_ITERATION_TIME:
               time.sleep(SERVER_ITERATION_TIME - elapsed)

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
