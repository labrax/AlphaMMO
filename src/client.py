#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import time

import pygame
from pygame.locals import QUIT, VIDEORESIZE, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION

import stackless

from alpha_defines import FPS
from client_states import ClientStates
from client_screen import ClientScreen
from client_input_handler import ClientInput
from alpha_communication import AlphaCommunication, AlphaCommunicationChannel


from server_simple import ClientAsServer


class AlphaGameClient:
    def __init__(self):
        # initializes game components
        # screen
        self.client_screen = ClientScreen()
        # client states - will hold everything we got
        self.client_states = ClientStates()
        # input
        self.client_input = ClientInput()
        # dummy server
        self.client_server = ClientAsServer()
        # communication
        self.client_communication = AlphaCommunication()
        channel_to_server = AlphaCommunicationChannel(self.client_server)
        self.client_communication.add(channel_to_server)
        channel_to_states = AlphaCommunicationChannel(self.client_states)
        self.client_communication.add(channel_to_states)

        self.client_input.channel = channel_to_states
        self.client_states.channel = channel_to_server
        self.client_server.channel = channel_to_states

        self.client_states.start()

    def start(self):
        """
        starts all the tasklets for the game client
        - communication
        - main loop
        :return:
        """
        self.tasklets = [stackless.tasklet(self.run)(), stackless.tasklet(self.client_server.run)(),
                         stackless.tasklet(self.client_communication.run)(), stackless.tasklet(self.client_states.run)()]
        stackless.run()

    def run(self):
        running = True

        old_time = pygame.time.get_ticks()
        while running:
            stackless.schedule()

            events = pygame.event.get()
            for event in events:
                if event.type in [KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION]:
                    self.client_input.handle(event)
                if event.type == VIDEORESIZE:
                    self.client_screen.resize(event)
                if event.type == QUIT:
                    running = False

            if self.client_states.ready:
                self.client_screen.render(self.client_states)

            new_time = pygame.time.get_ticks()
            waited = new_time - old_time
            old_time = new_time
            if waited < 60:
                time.sleep(1.0 / (FPS - waited))

        self.client_states.running = False
        self.client_communication.running = False
        self.client_server.running = False
        pygame.quit()


if __name__ == '__main__':
    gs = AlphaGameClient()
    gs.start()
