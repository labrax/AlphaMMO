# -*- coding: utf-8 -*-

import socket
import ssl

import stackless

from util.alpha_communication import AlphaCommunicationChannel
from util.alpha_defines import SERVER_IP, SERVER_PORT, SOCKET_BUFFER, SOCKET_TIMEOUT
from client_util.client_internal_protocol import AlphaClientProtocol, AlphaClientProtocolValues
from util.alpha_protocol import AlphaProtocol, check_valid
from util.alpha_socket_comm import send_receive


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
        print("To client", message)
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
                send_receive(self, False)
            stackless.schedule()
        stackless.schedule_remove()
