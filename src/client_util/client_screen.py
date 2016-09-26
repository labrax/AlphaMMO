# -*- coding: utf-8 -*-

import time

import pygame
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE

from util.alpha_defines import START_RESOLUTION, gray, WINDOW_TITLE


class ClientScreen:
    """
    Holds information about the window
    ClientScreen.current_size is the window resolution
    ClientScreen.screen is the pygame window object
    """
    def __init__(self):
        # start screen
        self.current_size = START_RESOLUTION
        self.screen = pygame.display.set_mode(self.current_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
        pygame.display.set_caption(WINDOW_TITLE)
        pygame.display.flip()

    def render(self, client_states):
        """
        Render the game given the game states information
        :param client_states: the game state reference
        :return: nothing
        """
        # clear screen
        self.screen.fill(gray)

        # draw current state
        client_states.mode.render(self.screen)

        # flip buffer (display it)
        pygame.display.flip()

    def resize(self, event):
        """
        Pass information to resize the window
        :param event: the resize event
        :return: nothing
        """
        self.current_size = event.dict['size']
        self.screen = pygame.display.set_mode(self.current_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
