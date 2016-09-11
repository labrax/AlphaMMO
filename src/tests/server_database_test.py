# -*- coding: utf-8 -*-

import unittest

from server_util.server_database import AlphaDatabase
from util.game_exceptions import InvalidCharacters, InvalidLogin, InvalidPassword, InvalidValue


class TestDatabase(unittest.TestCase):
    def test_invalid(self):
        sd = AlphaDatabase()
        with self.assertRaises(InvalidCharacters):
            sd.login_account('huehue\tbr', '')

        with self.assertRaises(InvalidCharacters):
            sd.login_account('huehueb?r', 'asdfgh')

        with self.assertRaises(InvalidCharacters):
            sd.create_account('huehue\tbr', '')

        with self.assertRaises(InvalidCharacters):
            sd.create_account('huehueb?r', 'asdfgh')

    def test_creation_and_repeat(self):
        AlphaDatabase.reset_db(True)
        sd = AlphaDatabase()
        sd.create_account('aaa', 'bbb')

        with self.assertRaises(InvalidValue):
            sd.create_account('aaa', 'bbb')

    def test_login(self):
        AlphaDatabase.reset_db(True)
        sd = AlphaDatabase()
        with self.assertRaises(InvalidLogin):
            sd.login_account('aaa2', 'bbb')

        self.assertTrue(sd.create_account('aaa', 'bbb'))

        with self.assertRaises(InvalidPassword):
            sd.login_account('aaa', 'bbb2')

        self.assertTrue(sd.login_account('aaa', 'bbb'))

    def test_create_login_toolong(self):
        sd = AlphaDatabase()
        with self.assertRaises(InvalidValue):
            sd.create_account('A'*17, "passwd")

    def test_create_update_login_del(self):
        AlphaDatabase.reset_db(True)
        sd = AlphaDatabase()
        sd.create_account('AAAA', "BBBB")
        with self.assertRaises(InvalidValue):
            sd.create_character('AAAA', 'A'*18)
        self.assertTrue(sd.create_character('AAAA', "Character"))
        self.assertTrue(sd.login_character('AAAA', "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB") == list())
        self.assertTrue(sd.login_character('AAAA', 'Character') == [
            ('AAAA', 0, 'Character', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)])
        self.assertTrue(sd.update_character('AAAA', 'Character', [1]*15))
        reply = sd.login_character('AAAA', 'Character')
        self.assertTrue(reply[0][2:] == ('Character', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))
        self.assertTrue(sd.delete_character('AAAA', 'Character'))
        self.assertTrue(sd.login_character('AAAA', 'Character') == list())


if __name__ == '__main__':
    unittest.main()
