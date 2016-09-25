# -*- coding: utf-8 -*-

import time
import bisect
import stackless


class AlphaServerScheduler:
    def __init__(self):
        self.sorted_list = list()
        self.running = True

    def add_event(self, callback, at_time=None, waiting_time=None):
        if at_time:
            bisect.insort_left(self.sorted_list, (at_time, callback))
        elif waiting_time:
            bisect.insort_left(self.sorted_list, (time.time() + waiting_time, callback))
        else:
            bisect.insort_left(self.sorted_list, (0, callback))

    def run(self):
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
