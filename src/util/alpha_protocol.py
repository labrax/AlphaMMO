# -*- coding: utf-8 -*-

from util.alpha_entities import Entity, Tile
from enum import Enum
import os
import sys


class AlphaProtocol(Enum):
    LOGIN = 0
    LOGOUT = -1
    STATUS = 1

    REQUEST_MOVE = 10
    REQUEST_SPEAK = 11

    TELEPORT = 200
    MOVING = 20
    MOVING_STATUS = 21
    SPEAKING = 22

    SET_ENTITIES = 3000
    REPLACE_ENTITIES = 3001
    ADD_ENTITIES = 3002
    REMOVE_ENTITIES = 3003

    SET_ENTITY = 3100
    ADD_ENTITY = 3102
    REMOVE_ENTITY = 3103

    RECEIVE_MAP = 5000
    RECEIVE_PLAYER = 5001

    PING = 100
    PONG = 101

    REQUEST_RECONNECT = 302

# list will have a list following with all the possible cases
protocol_format = dict(LOGIN=(str, str),  # user, passwd
                       LOGOUT=tuple(),
                       STATUS=(int, int),  # 0 denied/offline, 1 login granted, -2 wrong user/passwd, -3 server overload AND session_id

                       REQUEST_MOVE=(int, int),  # coordinates
                       REQUEST_SPEAK=(str,),  # text

                       TELEPORT=(int, int),  # coordinates
                       MOVING=(int, int),  # start the character movement
                       MOVING_STATUS=(int, int, int),  # status, coordinates if the player started the movement return if success or not (move back)
                       SPEAKING=(str, int, int, int),  # text, type, coordinates

                       SET_ENTITIES=(list, [Entity]),  #list of visible entities
                       REPLACE_ENTITIES=(list, [Entity]),
                       ADD_ENTITIES=(list, [Entity]),
                       REMOVE_ENTITIES=(list, [Entity]),

                       SET_ENTITY=(Entity,),  # set an entity state
                       ADD_ENTITY=(Entity,),
                       REMOVE_ENTITY=(Entity,),

                       RECEIVE_MAP=(int, int, list, [list]),  # coordinates, tiles  # TODO: fix vulnerability?
                       RECEIVE_PLAYER=(Entity,),

                       PING=(int,),
                       PONG=(int,),

                       REQUEST_RECONNECT=(int,)  # session id
                       )

# we will verify each message that arrives to see if it is to the right destination
server_accepts = dict(LOGIN=True,
                      LOGOUT=True,

                      REQUEST_MOVE=True,
                      REQUEST_SPEAK=True,

                      PING=True,
                      PONG=True,

                      REQUEST_RECONNECT=True
                      )

client_accepts = dict(STATUS=True,  # login mode

                      TELEPORT=True,  # play
                      MOVING=True,
                      MOVING_STATUS=True,
                      SPEAKING=True,

                      SET_ENTITIES=True,
                      REPLACE_ENTITIES=True,
                      ADD_ENTITIES=True,
                      REMOVE_ENTITIES=True,

                      SET_ENTITY=True,
                      ADD_ENTITY=True,
                      REMOVE_ENTITY=True,
                      RECEIVE_MAP=True,
                      RECEIVE_PLAYER=True,

                      PING=True,  # sockets
                      PONG=True,
                      )


def check_valid(message, isserver):
    def _wrap(message, isserver):
        try:
            ap = AlphaProtocol(message[0])
            if isserver and ap.name not in server_accepts:
                return False
            elif not isserver and ap.name not in client_accepts:
                return False
            this_format = protocol_format[ap.name]
            for i in range(len(this_format)):
                if this_format[i] == list:
                    for e in message[i+1]:
                        if type(e) not in this_format[i+1]:
                            return False
                    i += 1
                    continue
                elif not isinstance(message[i+1], this_format[i]):
                    return False
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, e, fname, exc_tb.tb_lineno)
            return False
        return True
    status = _wrap(message, isserver)
    print('CHECKING MESSAGE', status, message)
    return status
