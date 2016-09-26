# -*- coding: utf-8 -*-

"""
This file holds the information for the internal communication between the client states and socket
"""

from enum import Enum


class AlphaClientProtocol(Enum):
    """
    The codes for the messages
    """
    # both directions
    INTERNAL_STATUS = 10000

    # from the client_states
    TRY_LOGIN = 100
    TRY_REGISTER = 200


class AlphaClientProtocolValues(Enum):
    """
    The codes for the values
    """
    # shutting down
    FORCE_SHUTDOWN = -111

    # from the client_sockets
    OFF = 98
    TRYING_CONNECTION = 102
    RECONNECTING = 105
    CONNECTED = 110
    LOGGED = 150
