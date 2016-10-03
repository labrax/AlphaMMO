# -*- coding: utf-8 -*-


import pygame

from client_util.client_states_modes.alpha_mode import AlphaMode
import client_util.client_states_modes.alpha_start
import client_util.client_states_modes.alpha_login

from client_util.client_ui import AlphaWindow, AlphaLabel, AlphaEditBox, AlphaButton
from client_util.client_internal_protocol import AlphaClientProtocol
from util.alpha_protocol import AlphaProtocol


class AlphaRegisterMode(AlphaMode):
    """
    Class for the register screen
    AlphaRegisterMode.aw is the register window
    """
    def __init__(self, screen_size, client_states):
        super(AlphaRegisterMode, self).__init__(screen_size, client_states)
        # screen objects
        self.aw = AlphaWindow((self.current_size[0] / 2 - 150, self.current_size[1] / 2 - 29 * 2), (300, 29 * 6),
                              "REGISTER")
        al = AlphaLabel((3, 29), (120, 24), 'Account:')
        al2 = AlphaLabel((3, 29 * 2), (160, 24), 'Password:')
        al3 = AlphaLabel((3, 29 * 3), (160, 24), 'Repeat:')
        al4 = AlphaLabel((3, 29 * 4), (160, 24), 'Email:')

        ae = AlphaEditBox((3 + 150, 29), (145, 24), '')
        ae2 = AlphaEditBox((3 + 150, 29 * 2), (145, 24), '', password=True)
        ae3 = AlphaEditBox((3 + 150, 29 * 3), (145, 24), '', password=True)
        ae4 = AlphaEditBox((3 + 150, 29 * 4), (145, 24), '')

        ab = AlphaButton((0, 29 * 5), (150, 29), 'CANCEL', callback=self.cancel)
        ab2 = AlphaButton((150, 29 * 5), (149, 29), 'OK', callback=self.try_register, callback_args=(ae, ae2, ae3, ae4))
        self.aw.escape = ab
        self.aw.enter = ab2
        self.aw.add_component([al, al2, al3, al4, ae, ae2, ae3, ae4, ab, ab2])
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
                    self.client_states.mode = client_util.client_states_modes.alpha_login.AlphaLoginMode(self.current_size, self.client_states)
                else:
                    print("Status invalid at", self.__class__.__name__, message[1])
            else:
                print("Invalid message at", self.__class__.__name__, message)

    def try_register(self, user_ui, passwd_ui, verify_passwd, email):
        """
        Try to register on the server
        :param user_ui: the UI for the account
        :param passwd_ui: the UI for the password
        :param verify_passwd: the UI for the password verification
        :param email: the UI for the player's email
        :return: nothing
        """
        if passwd_ui.text == verify_passwd.text:
            self.client_states.channel.push([AlphaClientProtocol.TRY_REGISTER, user_ui.text, passwd_ui.text, email.text])
        else:
            # todo: better notify that dont match
            print("Password doesn't match")

    def cancel(self):
        self.client_states.mode = client_util.client_states_modes.alpha_start.AlphaStartMode(self.current_size, self.client_states)
