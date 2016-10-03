# -*- coding: utf-8 -*-


import pygame

from client_util.client_states_modes.alpha_mode import AlphaMode
import client_util.client_states_modes.alpha_register
import client_util.client_states_modes.alpha_login

from client_util.client_ui import AlphaWindow, AlphaButton
from util.alpha_defines import START_WINDOW_NAME


class AlphaStartMode(AlphaMode):
    """
    Class for the initial game screen
    AlphaStartMode.aw is the start window
    """
    def __init__(self, screen_size, client_states):
        super(AlphaStartMode, self).__init__(screen_size, client_states)
        # screen objects
        self.aw = AlphaWindow((self.current_size[0] / 2 - 150, self.current_size[1] / 2 - 29 * 2), (300, 29 * 2),
                              START_WINDOW_NAME)
        ab = AlphaButton((0, 29 * 1), (150, 29), 'REGISTER', callback=self.register_window)
        ab2 = AlphaButton((150, 29 * 1), (149, 29), 'LOGIN', callback=self.login_window)
        self.aw.add_component([ab, ab2])
        self.aw.enter = ab2
        self.prepare()

    def resize(self, event):
        self.current_size = event.dict['size']
        self.prepare()

    def prepare(self):
        self.aw.pos = ((self.current_size[0] - self.aw.size[0]) / 2, (self.current_size[1] - self.aw.size[1]) / 2)
        self.aw.update()

    def render(self, dest):
        self.aw.render(dest)

    def iterate(self):
        pass

    def notify(self, message):
        if isinstance(message, pygame.event.EventType):
            if self.aw.notify(message):
                self.aw.update()

    def register_window(self):
        """
        Loads the register window
        :return: nothing
        """
        self.client_states.mode = client_util.client_states_modes.alpha_register.AlphaRegisterMode(self.current_size, self.client_states)

    def login_window(self):
        """
        Loads the login window
        :return: nothing
        """
        self.client_states.mode = client_util.client_states_modes.alpha_login.AlphaLoginMode(self.current_size, self.client_states)
