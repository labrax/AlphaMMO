# -*- coding: utf-8 -*-


import pygame

from client_util.client_states_modes.alpha_mode import AlphaMode
import client_util.client_states_modes.alpha_start
import client_util.client_states_modes.alpha_play

from client_util.client_ui import AlphaWindow, AlphaLabel, AlphaEditBox, AlphaButton
from client_util.client_internal_protocol import AlphaClientProtocol
from util.alpha_protocol import AlphaProtocol


class AlphaLoginMode(AlphaMode):
    """
    Class for the login screen
    AlphaLoginMode.aw is the login window
    """
    def __init__(self, screen_size, client_states):
        super(AlphaLoginMode, self).__init__(screen_size, client_states)
        # screen objects
        self.aw = AlphaWindow((self.current_size[0] / 2 - 150, self.current_size[1] / 2 - 29 * 2), (300, 29 * 4),
                              "LOGIN")
        al = AlphaLabel((3, 29), (120, 24), 'Account:')
        al2 = AlphaLabel((3, 29 * 2), (160, 24), 'Password:')
        ae = AlphaEditBox((3 + 150, 29), (145, 24), '')
        ae2 = AlphaEditBox((3 + 150, 29 * 2), (145, 24), '', password=True)

        ab = AlphaButton((0, 29 * 3), (150, 29), 'CANCEL', callback=self.cancel)
        ab2 = AlphaButton((150, 29 * 3), (149, 29), 'OK', callback=self.try_login, callback_args=(ae, ae2,))
        self.aw.escape = ab
        self.aw.enter = ab2
        self.aw.add_component([al, al2, ae, ae2, ab, ab2])
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
        else:
            if message[0] == AlphaProtocol.STATUS:
                if message[1] == 1:
                    self.client_states.session_id = message[2]
                    self.client_states.mode = client_util.client_states_modes.alpha_play.AlphaPlayMode(self.current_size, self.client_states)
                    self.client_states.logged = True
                elif message[1] == -2:
                    # todo: improve message
                    print('Invalid login/password.')
                elif message[1] == -3:
                    print("Server is overloaded.")
                else:
                    print("Status invalid at", self.__class__.__name__, message[1])
            else:
                print("Invalid message at", self.__class__.__name__, message)

    def try_login(self, user_ui, passwd_ui):
        """
        Try to login on the server
        :param user_ui: the UI for the account edit box
        :param passwd_ui: the UI for the password edit box
        :return: nothing
        """
        self.client_states.channel.push([AlphaClientProtocol.TRY_LOGIN, user_ui.text, passwd_ui.text])

    def cancel(self):
        """
        Cancel the login window, returns to start screen
        :return: nothing
        """
        self.client_states.mode = client_util.client_states_modes.alpha_start.AlphaStartMode(self.current_size, self.client_states)
