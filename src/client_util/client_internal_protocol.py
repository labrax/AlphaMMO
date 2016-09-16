# -*- coding: utf-8 -*-

from enum import Enum


class AlphaClientProtocol(Enum):
    # both directions
    INTERNAL_STATUS = 10000

    # from the client_states
    TRY_LOGIN = 100


class AlphaClientProtocolValues(Enum):
    # shutting down
    FORCE_SHUTDOWN = -111

    # from the client_sockets
    OFF = 98
    TRYING_CONNECTION = 102
    RECONNECTING = 105
    CONNECTED = 110
    LOGGED = 150
