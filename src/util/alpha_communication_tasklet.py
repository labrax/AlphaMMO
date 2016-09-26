# -*- coding: utf-8 -*-

from queue import Queue
import stackless


class AlphaCommunicationMember:
    """
    This is a member of the communication
    It will get notified of messages
    """
    def notify(self, message):
        """
        Receives a message
        :param message: the message
        :return: True if processed (or nothing)
        """
        pass


class AlphaCommunicationChannel:
    """
    This is a communication channel to a destination (AlphaCommunicationMember)
    """
    def __init__(self, destination):
        """
        Initiates a communication channel with a destination.
        :param destination: an AlphaCommunicationMember destination
        """
        self.destination = destination
        self.queue = Queue()

    def push(self, message):
        """
        Inserts a message in the queue
        :param message: the message
        :return: nothing
        """
        self.queue.put(message)

    def clean(self):
        """
        Resets the queue
        :return: nothing
        """
        self.queue = Queue()


class AlphaCommunication:
    """
    This is the communication handler.
    It will hold all channels and pass messages when required
    """
    def __init__(self):
        """
        Initiates with an empty relation of channels
        """
        self.channels = list()
        self.running = False

    def add(self, channel):
        """
        Add channels to the handler
        :param channel: the channel
        :return: nothing
        """
        self.channels.append(channel)

    def run(self):
        """
        Runs the handler. Ends when AlphaCommunication.running = False
        This method uses the stackless scheduler
        :return: nothing
        """
        self.running = True
        while self.running:
            for i in self.channels:
                while i.queue.qsize() > 0:
                    i.destination.notify(i.queue.get())
            stackless.schedule()
