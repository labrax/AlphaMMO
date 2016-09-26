# -*- coding: utf-8 -*-

"""
Exceptions for the game
"""


class AlphaException(Exception):
    """
    Game initiated exception
    """
    def __init__(self, content):
        super(AlphaException, self).__init__('ERROR: ' + content)


class DatabaseException(AlphaException):
    """
    Database specific error
    """
    def __init__(self, content):
        super(DatabaseException, self).__init__(content)


class InvalidCharacters(DatabaseException):
    def __init__(self, content):
        super(InvalidCharacters, self).__init__(content)


class InvalidLogin(DatabaseException):
    def __init__(self, content):
        super(InvalidLogin, self).__init__(content)


class InvalidPassword(DatabaseException):
    def __init__(self, content):
        super(InvalidPassword, self).__init__(content)


class InvalidValue(DatabaseException):
    def __init__(self, content):
        super(InvalidValue, self).__init__(content)


class SingletonViolated(AlphaException):
    def __init__(self, content):
        super(SingletonViolated, self).__init__(content)
