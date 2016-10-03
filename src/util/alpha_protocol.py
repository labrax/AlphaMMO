# -*- coding: utf-8 -*-

"""
This file holds the information for the communication between the client and the server
"""


from util.alpha_entities import Entity, Tile, AlphaEffect
from enum import Enum
import os
import sys


class AlphaProtocol(Enum):
    """
    The codes for the messages
    """
    LOGIN = 0
    LOGOUT = -1
    STATUS = 1
    SERVER_MESSAGE = 3
    REGISTER = 2

    REQUEST_MOVE = 10
    REQUEST_SPEAK = 11
    REQUEST_ACTION = 12

    TELEPORT = 200
    MOVING = 20
    MOVING_STATUS = 21
    SPEAKING = 22
    ACTION = 29
    EFFECT = 30

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
                       SERVER_MESSAGE=(str,),  # server message for multiple information
                       REGISTER=(str, str, str),  # account, password, email

                       REQUEST_MOVE=(int, int),  # coordinates
                       REQUEST_SPEAK=(str,),  # text
                       REQUEST_ACTION=(int, int, int, int),  # action id, position, entity id

                       TELEPORT=(int, int),  # coordinates
                       MOVING=(int, int),  # start the character movement
                       MOVING_STATUS=(int, int, int),  # status, coordinates if the player started the movement return if success or not (move back)
                       SPEAKING=(str, int, int, int),  # text, type, coordinates
                       ACTION=(int,),  # status 0: denied, 1: doing/success
                       EFFECT=(AlphaEffect, int, int),  # position

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

                       REQUEST_RECONNECT=(int,)  # session token
                       )

# we will verify each message that arrives to see if it is to the right destination
server_accepts = dict(LOGIN=True,
                      LOGOUT=True,
                      REGISTER=True,

                      REQUEST_MOVE=True,
                      REQUEST_SPEAK=True,
                      REQUEST_ACTION=True,

                      PING=True,
                      PONG=True,

                      REQUEST_RECONNECT=True
                      )

client_accepts = dict(STATUS=True,  # login mode
                      SERVER_MESSAGE=True,

                      TELEPORT=True,  # play
                      MOVING=True,
                      MOVING_STATUS=True,
                      SPEAKING=True,
                      ACTION=True,
                      EFFECT=True,

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


def check_valid(message, is_server):
    """
    Check if a message is valid for a given receptor
    :param message: the message
    :param is_server: True if the message targets the server, False if the message targets the client
    :return: True or False
    """
    def _wrap(message, is_server):
        try:
            ap = AlphaProtocol(message[0])
            message = message[1:]
            if is_server and ap.name not in server_accepts:
                return False
            elif not is_server and ap.name not in client_accepts:
                return False
            this_format = protocol_format[ap.name]
            i = -1
            for f in range(len(this_format)):
                i += 1
                if len(this_format) - this_format.count(list) == i:
                    break
                if this_format[f] == list:
                    for e in message[i]:
                        for element in this_format[f+1]:
                            if not isinstance(e, element):
                                return False
                    f += 1
                    continue
                elif not isinstance(message[i], this_format[f]):
                    return False
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, e, fname, exc_tb.tb_lineno)
            return False
        return True
    status = _wrap(message, is_server)
    # print('CHECKING MESSAGE', status, message)
    return status


def retrieve_with_types(message, is_server):
    """
    Returns a message with excepted formating if valid
    :param message: the message
    :param is_server: True if the message targets the server, False if the message targets the client
    :return: a list with the information of raises exception if invalid
    """
    assert is_server  # this function is not ready to handle lists at the client!

    def _wrap(message):
        try:
            ap = message[0]
            message = message[1:]
            this_format = protocol_format[ap.name]
            i = -1
            for f in range(len(this_format)):
                i += 1
                if this_format[f] == list:
                    for e in message[i+1]:
                        if type(e) not in this_format[f+1]:
                            raise Exception("Invalid message format")
                    f += 1
                    continue
                else:
                    try:
                        message[i] = this_format[f](message[i])
                    except:
                        raise Exception("Invalid message format")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, e, fname, exc_tb.tb_lineno)
        return message
    new_message = [message[0]] + _wrap(message)
    # print('OBTAINED', new_message)
    return new_message
