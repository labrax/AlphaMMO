# -*- coding: utf-8 -*-

# login imports
import stackless

import client_util.client_states_modes.alpha_start as alpha_start

from util.alpha_communication_tasklet import AlphaCommunicationMember
from util.alpha_defines import START_RESOLUTION


class ClientStates(AlphaCommunicationMember):
    """
    Class to handle the different states in the game
    ClientStates.session_id is the information about the client session
    ClientStates.running holds information if the tasklet should stop running
    ClientStates.mode is the reference to the current state
    ClientStates.channel is the channel to send messages to the server
    ClientStates.logged if the player is logged
    """
    def __init__(self):
        # server token
        self.session_id = None  # TODO: use later?
        self.running = True
        self.mode = alpha_start.AlphaStartMode(START_RESOLUTION, self)
        self.channel = None

    def run(self):
        """
        Runs the handler. Ends when ClientStates.running = False
        This method uses the stackless scheduler
        :return: nothing
        """
        while self.running:
            self.mode.iterate()
            stackless.schedule()

    def notify(self, message):
        self.mode.notify(message)

    def resize(self, event):
        """
        Pass information to resize the state
        :param event: the resize event
        :return: nothing
        """
        self.mode.resize(event)
