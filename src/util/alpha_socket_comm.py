# -*- coding: utf-8 -*-

import os
import sys

import select
import pickle

from util.alpha_defines import SOCKET_BUFFER
from util.alpha_protocol import AlphaProtocol


def send_receive(self, isserver):
    """
    Exchange TCP messages
    :param self: the handler calling this method
    :param isserver: True if is the server handling, False if is the client
    They are different because of the asymmetry between the server and client, the server sends as a pickle string,
    the client decodes it but only it sends lists.
    :return: nothing
    """
    if isserver:
        socket = self.client_socket
    else:
        socket = self.server_socket

    # check if there are messages to read non-blocking the socket
    rr, rw, err = select.select([socket], list(), list(), 0)
    try:
        if len(rr) > 0:
            input = socket.recv(SOCKET_BUFFER)
            if input:
                self.socket_buffer += input
                # while the buffer has been filled and we are waiting for more we will try reading more
                read = True
                while read:
                    read = False
                    if b' ' in self.socket_buffer:
                        if isserver:
                            size = self.socket_buffer.split(b' ')[0]
                            len_size = len(size)

                            size = int(size)

                            if len_size + 1 + size >= len(self.socket_buffer):
                                read = True
                                current_read = self.socket_buffer[len_size + 1: len_size + 1 + size]
                                self.socket_buffer = self.socket_buffer[len_size + 1 + size:]
                                data = [i.decode() for i in current_read.split(b' ')]
                                data[0] = AlphaProtocol(int(data[0]))
                                # print("Server receiving from client", data)
                                self.notify(data)
                        else:
                            read = True
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
                                read = False
            # if there is no message it means the connection is broken
            else:
                if isserver:
                    self.running = False
                else:
                    self.on_error(self.__class__.__name__, 'Received no content', self.run, '', failed=True)
        send_buffer = b''
        while self.queue.qsize() > 0:
            if isserver:
                data = pickle.dumps(self.queue.get())
            else:
                qval = self.queue.get()
                data = str(qval[0].value).encode() + b' ' + b' '.join([str(i).encode() for i in qval[1:]])
            next_packet = str(len(data)).encode() + b' ' + data
            if len(send_buffer) > 0 and len(send_buffer) + len(next_packet) > SOCKET_BUFFER:
                socket.send(send_buffer)
                send_buffer = b''
            send_buffer += next_packet
        if len(send_buffer) > 0:
            socket.send(send_buffer)
    # if somehow failed the connection is broken
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        if isserver:
            self.running = False
        else:
            self.on_error(exc_type, e, fname, exc_tb.tb_lineno)
