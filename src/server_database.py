# -*- coding: utf-8 -*-

import os
import sqlite3
import crypt
import pdb

from alpha_server_defines import DATABASE_FILE
from game_exceptions import InvalidCharacters, InvalidLogin, InvalidPassword, InvalidValue


class AlphaDatabase:
    def __init__(self):
        # create file if needed
        if not os.path.exists(DATABASE_FILE):
            if '/' in DATABASE_FILE:
                os.mkdir('/'.join(DATABASE_FILE.split('/')[:-1]))
            open(DATABASE_FILE, 'a').close()

        self.conn = sqlite3.connect(DATABASE_FILE)
        # check if tables are k
        self.conn.cursor().execute("CREATE TABLE IF NOT EXISTS users_login (account_id VARCHAR (16), password_hash VARCHAR (256), password_salt VARCHAR (256))")
        self.conn.cursor().execute("CREATE TABLE IF NOT EXISTS characters (account_id VARCHAR (32), character_name VARCHAR (16), posx Int, posy Int, plevel Int, max_hp Int, curr_hp Int, max_mp Int, curr_mp Int, helmet Int, shirt Int, trousers Int, shield Int, weapon Int)")
        self.conn.commit()

    def check_login(self, account_id, password_passed):
        if not account_id.isalnum():
            raise InvalidCharacters('Invalid characters at %s' % self.__class__.__name__)
        reply = self.conn.cursor().execute("SELECT * FROM users_login WHERE account_id == ? LIMIT 1", (account_id, )).fetchall()
        if not reply:
            raise InvalidLogin('Invalid login at %s' % self.__class__.__name__)
        reply = reply[0]
        salt = reply[2]
        login_try_password = crypt.crypt(password_passed, "$6$" + salt)
        if login_try_password == reply[1]:
            return True
        else:
            raise InvalidPassword('Invalid login at %s' % self.__class__.__name__)

    def create_login(self, account_id, password):
        if not account_id.isalnum():
            raise InvalidCharacters('Invalid characters at %s' % self.__class__.__name__)

        if len(self.conn.cursor().execute("SELECT * FROM users_login WHERE account_id == ?", (account_id, )).fetchall()) > 0:
            raise InvalidValue('Account already exists at %s' % self.__class__.__name__)
        salt = crypt.mksalt()
        password_hash = crypt.crypt(password, "$6$" + salt)
        self.conn.cursor().execute("INSERT INTO users_login VALUES (?, ?, ?)", (account_id, password_hash, salt))
        self.conn.commit()
        return True

    def __exit__(self):
        self.conn.close()


if __name__ == '__main__':
    ad = AlphaDatabase()
    pdb.set_trace()