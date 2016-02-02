#!/usr/bin/python
# -*- coding:utf-8 -*-
import sqlite3

class KVDatabase(object):
    __table_name = 'KV'

    def __init__(self, db_path):
        self.__db_path = db_path
        self.__connect()
        self.__create_database_if_not_exist()

    def __connect(self):
        self.__conn = sqlite3.connect(self.__db_path)

    def __create_database_if_not_exist(self):
        sql = """
        CREATE TABLE IF NOT EXISTS %s
        (
            `id`    integer primary key autoincrement,
            `key`   text    unique,
            `value` text
        )
        """ % (self.__table_name,)
        self.__conn.execute(sql)

    def set(self, key, value):
        sql = """
        SELECT *
        FROM %s
        WHERE `key` = ?
        """ % (self.__table_name)
        cursor = self.__conn.execute(sql, (str(key),))
        if cursor.fetchone() is None:
            sql = """
            INSERT INTO %s
            (`key`, `value`)
            VALUES
            (?, ?)
            """ % (self.__table_name,)
            self.__conn.execute(sql, (str(key), str(value)))
        else:
            sql = """
            UPDATE %s
            SET `value` = ?
            WHERE `key` = ?
            """ % (self.__table_name, str(value), str(key))
            self.__conn.execute(sql, (str(value), str(key)))


    def get(self, key, default=None):
        sql = """
        SELECT `key`, `value`
        FROM %s
        WHERE `key` = '%s'
        """ % (self.__table_name, str(key))
        cursor = self.__conn.execute(sql)
        kv = cursor.fetchone()
        if kv is not None:
            return kv[1]
        else:
            return default

    def unset(self, key):
        sql = """
        DELETE
        FROM %s
        WHERE `key` = '%s'
        """ % (self.__table_name, str(key))
        self.__conn.execute(sql)

    def clear(self):
        sql = """
        DELETE
        FROM %s
        WHERE 1
        """ % (self.__table_name,)
        self.__conn.execute(sql)
