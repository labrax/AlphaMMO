# -*- coding: utf-8 -*-

from util.alpha_communication import AlphaCommunicationMember


class AlphaServerPlayerHandler(AlphaCommunicationMember):
    def __init__(self, channel_to_player):
        self.channel = channel_to_player

    def notify(self, message):
        pass
