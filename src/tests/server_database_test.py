# -*- coding: utf-8 -*-

import unittest
from game_exceptions import InvalidCharacters, InvalidLogin, InvalidPassword, InvalidValue
from server_database import AlphaDatabase


class TestDatabase(unittest.TestCase):
    def test_invalid(self):
        sd = AlphaDatabase()
        with self.assertRaises(InvalidCharacters):
            sd.create_login('huehue\tbr', '')

        with self.assertRaises(InvalidCharacters):
            sd.create_login('huehueb?r', 'asdfgh')

    def test_creation_and_repeat(self):
        sd = AlphaDatabase()
        sd.create_login('aaa', 'bbb')

        with self.assertRaises(InvalidValue):
            sd.create_login('aaa', 'bbb')

    def test_login(self):
        sd = AlphaDatabase()
        with self.assertRaises(InvalidLogin):
            sd.check_login('aaa2', 'bbb')

        with self.assertRaises(InvalidPassword):
            sd.check_login('aaa', 'bbb2')

        self.assertTrue(sd.check_login('aaa', 'bbb'))

if __name__ == '__main__':
    unittest.main()
