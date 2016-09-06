# -*- coding: utf-8 -*-


class Alpha_Exception(Exception):
    def __init__(self, content):
        super(Alpha_Exception, self).__init__('ERROR: ' + content)

