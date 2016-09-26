# -*- coding: utf-8 -*-

import time
import bisect
import stackless


class AlphaServerScheduler:
    """
    Stores information about the next event and executes them at the time
    AlphaServerScheduler.sorted_list contains the events time of execution and callback method
    AlphaServerScheduler.running holds information if the tasklet should stop running
    """
    def __init__(self):
        self.sorted_list = list()
        self.running = True

    def add_event(self, callback, at_time=None, waiting_time=None):
        """
        Add an event to the queue
        :param callback: the function to be called after the wait
        :param at_time: the time for the function to be executed
        :param waiting_time: the time to wait before calling the function
        :return: nothing
        """
        if at_time:
            bisect.insort_left(self.sorted_list, (at_time, callback))
        elif waiting_time:
            bisect.insort_left(self.sorted_list, (time.time() + waiting_time, callback))
        else:
            bisect.insort_left(self.sorted_list, (0, callback))

    def run(self):
        """
        Runs the handler. Ends when AlphaServerScheduler.running = False
        This method uses the stackless scheduler
        :return: nothing
        """
        while self.running:
            curr_time = time.time()
            if len(self.sorted_list) > 0:
                index = 0
                for index in range(len(self.sorted_list)):
                    if curr_time > i[0]:
                        i[1]()
                    else:
                        break
                self.sorted_list = self.sorted_list[index:]
            stackless.schedule()
