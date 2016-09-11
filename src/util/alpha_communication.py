# -*- coding: utf-8 -*-

from queue import Queue
import stackless


class AlphaCommunicationMember:
    def notify(self, message):
        pass


class AlphaCommunicationChannel:
    def __init__(self, destination):
        self.destination = destination
        self.queue = Queue()

    def push(self, message):
        self.queue.put(message)


class AlphaCommunication:
    def __init__(self):
        self.channels = list()
        self.running = True

    def add(self, channel):
        self.channels.append(channel)

    def run(self):
        while self.running:
            for i in self.channels:
                while i.queue.qsize() > 0:
                    i.destination.notify(i.queue.get())
            stackless.schedule()