# -*- coding: utf-8 -*-

import socket
import ssl

import stackless

from util.alpha_communication_tasklet import AlphaCommunicationChannel
from util.alpha_defines import SERVER_IP, SERVER_PORT, SOCKET_BUFFER, SOCKET_TIMEOUT
from client_util.client_internal_protocol import AlphaClientProtocol, AlphaClientProtocolValues
from util.alpha_protocol import AlphaProtocol, check_valid
from util.alpha_socket_comm import send_receive


class AlphaClientSocket(AlphaCommunicationChannel):
    """
    Class to handle the different states in the game
    AlphaClientSocket.server_socket is the socket to the server
    AlphaClientSocket.socket_buffer is the buffer for the communication
    AlphaClientSocket.running holds information if the tasklet should stop running
    AlphaClientSocket.state is the state of the communication
    AlphaClientSocket.client_states is the reference to the client states object
    """
    def __init__(self, client_states):
        super(AlphaClientSocket, self).__init__(None)
        self.server_socket = None
        self.socket_buffer = b''
        self.running = True

        self.state = AlphaClientProtocolValues.OFF
        self.client_states = client_states

    def start(self):
        """
        Starts the communication:
            - create the socket
            - encapsulate with SSL
            - if on error notify and cancel
        :return: nothing
        """
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

    def to_client(self, message):
        """
        Receiving a message from the server send it to the client states object if it is valid
        :param message: the message
        :return: nothing
        """
        print("To client", message)
        if check_valid(message, False):
            self.client_states.notify(message)
        else:
            print('Client received from server invalid message', message)

    def to_client_internal(self, message):
        """
        Send an internal message to the client states object
        :param message: the message
        :return: nothing
        """
        self.client_states.notify(message)

    def notify(self, message):
        """
        Receiving a message from the client states object and send it to the server if it is valid
        :param message: the message
        :return: nothing
        """
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

    def on_error(self, exc, e, fnma, lineno, failed=False):  # TODO: put somewhere else?
        """
        If an error occurred print the information and update state
        :param exc: the object on error
        :param e: the error
        :param fnma: the function
        :param lineno: the line number
        :param failed: if the socket failed and the connection is over
        :return: nothing
        """
        # something went wrong, player is now offline - needs to re-establish connection
        print(exc, e, fnma, lineno)
        if failed:
            self.state = AlphaClientProtocolValues.OFF
        else:
            self.state = AlphaClientProtocolValues.RECONNECTING
        self.to_client_internal([AlphaClientProtocol.INTERNAL_STATUS, self.state])

    def run(self):
        """
        Runs the handler. Ends when AlphaClientSocket.running = False
        This method uses the stackless scheduler
        :return: nothing
        """
        while self.running:
            if not self.state == AlphaClientProtocolValues.OFF:
                if self.state == AlphaClientProtocolValues.TRYING_CONNECTION:
                    self.start()
                    continue
                send_receive(self, False)
            stackless.schedule()
        stackless.schedule_remove()
