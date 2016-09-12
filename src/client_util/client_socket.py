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


class AlphaClientSocket(AlphaCommunicationChannel):
    def __init__(self, client_states):
        super(AlphaClientSocket, self).__init__(None)
        self.server_socket = None
        self.socket_buffer = b''
        self.running = True
        self.started = False
        self.client_states = client_states

    def start(self):
        print("STARTING CONNECTION")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.settimeout(SOCKET_TIMEOUT)
        try:
            self.server_socket.connect((SERVER_IP, SERVER_PORT))
        except:
            self.running = False
        self.server_socket = ssl.wrap_socket(self.server_socket, ca_certs='server.crt', cert_reqs=ssl.CERT_REQUIRED)
        self.started = True

    def to_client(self, message):
        print("To client", message)
        self.client_states.notify(message)

    # message to server
    def notify(self, message):
        print("Socket received", message)
        self.push(message)

    def run(self):
        while self.running:
            if not self.started:
                self.start()
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
                                size = self.socket_buffer.split(b' ')[0]
                                len_size = len(size)

                                size = int(size)

                                if len_size + 1 + size <= len(self.socket_buffer):
                                    read = True
                                    current_read = self.socket_buffer[len_size + 1: len_size + 1 + size]
                                    self.socket_buffer = self.socket_buffer[len_size + 1 + size:]
                                    #print("Receiving...", current_read)
                                    self.to_client(pickle.loads(current_read))
                    else:
                        self.running = False
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, e, fname, exc_tb.tb_lineno)
                    exit(-1)
                    # something went wrong, player is now offline - needs to re-establish connection
                    self.started = False
            try:
                while self.queue.qsize() > 0:
                    data = pickle.dumps(self.queue.get())
                    # print("Socket sending", data)
                    self.server_socket.send(str(len(data)).encode() + b' ' + data)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, e, fname, exc_tb.tb_lineno)
                exit(-1)
                # something went wrong, player is now offline - needs to re-establish connection
                self.running = False
            stackless.schedule()
        exit(-1)
        stackless.schedule_remove()
