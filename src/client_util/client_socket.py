# -*- coding: utf-8 -*-

import sys
import os

import socket
import select
import ssl
import pickle

import stackless

from util.alpha_communication import AlphaCommunicationChannel
from util.alpha_defines import SERVER_IP, SERVER_PORT, SOCKET_BUFFER, SOCKET_TIMEOUT
from client_util.client_internal_protocol import AlphaClientProtocol, AlphaClientProtocolValues
from util.alpha_protocol import AlphaProtocol, check_valid


class AlphaClientSocket(AlphaCommunicationChannel):
    def __init__(self, client_states):
        super(AlphaClientSocket, self).__init__(None)
        self.server_socket = None
        self.socket_buffer = b''
        self.running = True

        self.state = AlphaClientProtocolValues.OFF
        self.client_states = client_states

    def start(self):
        print("STARTING CONNECTION")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.settimeout(SOCKET_TIMEOUT)
        try:
            self.server_socket.connect((SERVER_IP, SERVER_PORT))
            self.server_socket = ssl.wrap_socket(self.server_socket, ca_certs='server.crt', cert_reqs=ssl.CERT_REQUIRED)
        except:
            # this case we can't even establish a connection to the server, thus it is offline and we are gonna stay too
            self.to_client_internal([AlphaClientProtocol, AlphaClientProtocolValues.OFF])
            self.on_error(self.__class__, 'Error establishing connection', self.start, '', failed=True)
        if self.state == AlphaClientProtocolValues.RECONNECTING:
            self.push([AlphaProtocol.REQUEST_RECONNECT, self.client_states.session_id])
        self.state = AlphaClientProtocolValues.CONNECTED

    # message to client
    def to_client(self, message):
        #print("To client", message)
        if check_valid(message, False):
            self.client_states.notify(message)
        else:
            print('Client received from server invalid message', message)

    def to_client_internal(self, message):
        self.client_states.notify(message)

    # message to server
    def notify(self, message):
        #print("Socket received", message)
        if message[0] == AlphaClientProtocol.TRY_LOGIN:
            # todo: implement
            self.push([AlphaProtocol.LOGIN, message[1], message[2]])
            self.state = AlphaClientProtocolValues.TRYING_CONNECTION
        elif message[0] == AlphaClientProtocol.TRY_REGISTER:
            # todo: implement properly ;)
            self.push([AlphaProtocol.REGISTER, message[1], message[2], message[3]])
            self.state = AlphaClientProtocolValues.TRYING_CONNECTION
        elif message[0] == AlphaClientProtocol.INTERNAL_STATUS and message[1] == AlphaClientProtocolValues.FORCE_SHUTDOWN:
            self.state = AlphaClientProtocolValues.OFF
        else:
            if check_valid(message, True):
                self.push(message)
            else:
                print('Client to server invalid message', message)

    def on_error(self, exc, e, fnma, lineno, failed=False):
        # something went wrong, player is now offline - needs to re-establish connection
        print(exc, e, fnma, lineno)
        if failed:
            self.state = AlphaClientProtocolValues.OFF
        else:
            self.state = AlphaClientProtocolValues.RECONNECTING
        self.to_client_internal([AlphaClientProtocol.INTERNAL_STATUS, self.state])

    def run(self):
        while self.running:
            if not self.state == AlphaClientProtocolValues.OFF:
                if self.state == AlphaClientProtocolValues.TRYING_CONNECTION:
                    self.start()
                    continue
                rr, rw, err = select.select([self.server_socket], list(), list(), 0)
                if len(rr) > 0:
                    try:
                        input = self.server_socket.recv(SOCKET_BUFFER)
                        if input:
                            self.socket_buffer += input
                            # read message one by one
                            read = True
                            while read:
                                read = False
                                if b' ' in self.socket_buffer:
                                    # when we receive a package first we get the length of the message, and then we
                                    # calculate from what we have received if there is everything on the buffer
                                    size = self.socket_buffer.split(b' ')[0]
                                    len_size = len(size)

                                    size = int(size)

                                    if len_size + 1 + size <= len(self.socket_buffer):
                                        read = True
                                        current_read = self.socket_buffer[len_size + 1: len_size + 1 + size]
                                        self.socket_buffer = self.socket_buffer[len_size + 1 + size:]
                                        # print("Receiving...", current_read)
                                        self.to_client(pickle.loads(current_read))
                        else:
                            self.on_error(self.__class__, 'Received no content', self.run, '', failed=True)
                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        self.on_error(exc_type, e, fname, exc_tb.tb_lineno)
                try:
                    while self.queue.qsize() > 0:
                        qval = self.queue.get()
                        data = str(qval[0].value).encode() + b' ' + b' '.join([str(i).encode() for i in qval[1:]])
                        # data = b' '.join([str(i).encode() for i in self.queue.get()])
                        # print("Socket sending", data)
                        self.server_socket.send(str(len(data)).encode() + b' ' + data)
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    self.on_error(exc_type, e, fname, exc_tb.tb_lineno)
            stackless.schedule()
        stackless.schedule_remove()
