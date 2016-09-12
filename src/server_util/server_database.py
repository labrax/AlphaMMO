# -*- coding: utf-8 -*-

import crypt
import os
import pdb
import sqlite3
import time

from server_util.alpha_server_defines import DATABASE_FILE
from util.alpha_exceptions import InvalidCharacters, InvalidLogin, InvalidPassword, InvalidValue


class AlphaDatabase:
    def __init__(self):
        # create file if needed
        if not os.path.exists(DATABASE_FILE):
            if '/' in DATABASE_FILE:
                os.mkdir('/'.join(DATABASE_FILE.split('/')[:-1]))
            open(DATABASE_FILE, 'a').close()

        self.conn = sqlite3.connect(DATABASE_FILE)
        # check if tables are k
        self.conn.cursor().execute(
            "CREATE TABLE IF NOT EXISTS users_login (account_id VARCHAR (18), password_hash VARCHAR (256), password_salt VARCHAR (256))")
        self.conn.cursor().execute(
            "CREATE TABLE IF NOT EXISTS characters (account_id VARCHAR (34), last_login BIGINT, character_name VARCHAR (18), posx INT, posy INT, pexp BIGINT, max_hp INT, curr_hp INT, max_mp INT, curr_mp INT, skin INT, hair INT, helmet INT, shirt INT, trousers INT, boots INT, shield INT, weapon INT)")
        try:
            self.conn.cursor().execute(
                "CREATE INDEX users_login_idx on users_login (account_id)")
            self.conn.cursor().execute(
                "CREATE INDEX characters_idx on characters (account_id)")
        except:
            print('Indexes already created.')
        self.conn.commit()

    @staticmethod
    def reset_db(areyousure=False):
        if areyousure:
            import subprocess
            subprocess.Popen('rm ' + DATABASE_FILE, shell=True)
            time.sleep(2)

    def login_account(self, account_id, password_passed):
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

    def create_account(self, account_id, password):
        if not account_id.isalnum():
            raise InvalidCharacters('Invalid characters at %s' % self.__class__.__name__)
        if len(account_id) > 16:
            raise InvalidValue('Account too long at %s' % self.__class__.__name__)
        if len(self.conn.cursor().execute("SELECT * FROM users_login WHERE account_id == ?", (account_id, )).fetchall()) > 0:
            raise InvalidValue('Account already exists at %s' % self.__class__.__name__)
        salt = crypt.mksalt()
        password_hash = crypt.crypt(password, "$6$" + salt)
        self.conn.cursor().execute("INSERT INTO users_login VALUES (?, ?, ?)", (account_id, password_hash, salt))
        self.conn.commit()
        return True
    
    def create_character(self, account_id, character_name):
        """
        We are supposing that the account is right, there is a working account_id with an active session
        :param account_id:
        :param character_name:
        :return:
        """
        if not character_name.isalnum():
            raise InvalidCharacters('Invalid characters at %s' % self.__class__.__name__)
        if len(character_name) > 16:
            raise InvalidValue('Character name too long at %s' % self.__class__.__name__)
        self.conn.cursor().execute("INSERT INTO characters VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (account_id, 0, character_name, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.conn.commit()
        return True

    def login_character(self, account_id, character_name):
        character_data = self.conn.cursor().execute("SELECT * FROM characters WHERE account_id = ? AND character_name = ?", (account_id, character_name)).fetchall()
        self.conn.cursor().execute("UPDATE characters SET last_login = ? WHERE account_id = ? AND character_name = ?", (time.time(), account_id, character_name))
        self.conn.commit()
        return character_data

    def update_character(self, account_id, character_name, character_data):
        self.conn.cursor().execute("UPDATE characters SET posx = ?, posy = ?, pexp = ?, max_hp = ?, curr_hp = ?, max_mp = ?, curr_mp = ?, skin = ?, hair = ?, helmet = ?, shirt = ?, trousers = ?, boots = ?, shield = ?, weapon = ? WHERE account_id = ? AND character_name = ?",
                                   character_data + [account_id, character_name])
        self.conn.commit()
        return True

    def delete_character(self, account_id, character_name):
        self.conn.cursor().execute("DELETE FROM characters WHERE account_id = ? AND character_name = ?", (account_id, character_name))
        self.conn.commit()
        return True

    @staticmethod
    def entity_to_sql(entity):
        return [entity.pos[0], entity.pos[1], entity.exp, entity.hp[1], entity.hp[0], entity.mp[1], entity.mp[0],
                entity.sprite.skin, entity.sprite.hair, entity.sprite.helmet, entity.sprite.shirt,
                entity.sprite.trousers, entity.sprite.boots, entity.sprite.shield, entity.sprite.weapon]

    def __exit__(self):
        self.conn.close()


if __name__ == '__main__':
    ad = AlphaDatabase()
    pdb.set_trace()