# -*- coding: utf-8 -*-


class AlphaMode(object):
    """
    Class for the different stages of the game
    AlphaMode.current_size is the size of the screen
    AlphaMode.client_states is the upper class calling the state
    """
    def __init__(self, screen_size, client_states):
        self.current_size = screen_size
        self.client_states = client_states

    def resize(self, event):
        """
        Passes a resize event to the current mode
        :param event: the resize event
        :return: nothing
        """
        pass

    def prepare(self):
        """
        Prepares the screen on startup and screen resize
        :return: nothing
        """
        pass

    def render(self, dest):
        """
        Render the screen on a destionation surface
        :param dest: the destination surface
        :return: nothing
        """
        pass

    def iterate(self):
        """
        Iterate some events on the modes
        :return:
        """
        pass

    def notify(self, message):
        """
        Notifies the mode for events
        :param message: the message
        :return: nothing
        """
        pass
