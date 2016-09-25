# -*- coding: utf-8 -*-

# login imports
import stackless

import client_util.client_states_modes.alpha_start as alpha_start

from util.alpha_communication import AlphaCommunicationMember
from util.alpha_defines import START_RESOLUTION


class ClientStates(AlphaCommunicationMember):
    def __init__(self):
        # server token
        self.session_id = None  # TODO: use later?
        self.running = True
        self.mode = alpha_start.AlphaStartMode(START_RESOLUTION, self)

        self.channel = None
        self.logged = False

    def run(self):
        while self.running:
            self.mode.iterate()
            stackless.schedule()

    def notify(self, message):
        self.mode.notify(message)

    def resize(self, event):
        self.mode.resize(event)
