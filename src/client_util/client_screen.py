# -*- coding: utf-8 -*-

import time

import pygame
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE

from util.alpha_defines import START_RESOLUTION, gray, version


class ClientScreen:
    def __init__(self):
        # start screen
        self.current_size = START_RESOLUTION
        self.screen = pygame.display.set_mode(self.current_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
        pygame.display.set_caption('AlphaMMO Client ' + str(version))
        pygame.display.flip()

    def prepare(self):
        pass

    def render(self, client_states):
        # clear screen
        self.screen.fill(gray)

        # draw current state
        client_states.mode.render(self.screen)

        # flip buffer (display it)
        pygame.display.flip()

    def resize(self, event):
        self.current_size = event.dict['size']
        self.screen = pygame.display.set_mode(self.current_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.prepare()
