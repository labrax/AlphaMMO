# -*- coding: utf-8 -*-

from util.alpha_communication import AlphaCommunicationChannel


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
