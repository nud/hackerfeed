# -*- encoding: utf-8 -*-
#
# Copyright (C) 2013 Steve Frécinaux
#
# This module is part of hackerfeed and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import os.path
import sqlite3
import time

class FeedCache(object):
    def __init__(self, filename):
        self.__connect(filename)

    def __connect(self, filename):
        db_exists = os.path.isfile(filename)

        self.__conn = sqlite3.connect(filename)

        if not db_exists:
            c = self.__conn.cursor()

            c.execute("""CREATE TABLE entry (id TEXT PRIMARY KEY, link TEXT, title TEXT, updated INTEGER)""")
            self.__conn.commit()
    
    def __get_entry_id(self, entry):
        if 'id' in entry:
            return entry.id
        return entry.link

    def __get_entry_date(self, entry):
        for field in ('published', 'updated', 'created'):
            if field in entry:
                return time.mktime(entry[field + '_parsed'])

    def add_entry(self, entry):
        c = self.__conn.cursor()
        c.execute('INSERT OR REPLACE INTO entry (id, link, title, updated) VALUES (?, ?, ?, ?)',
                  (self.__get_entry_id(entry), entry.link, entry.title, self.__get_entry_date(entry)))
        self.__conn.commit()

    def get_entries(self, page=0, pagesize=100):
        c = self.__conn.cursor()
        c.execute('SELECT * FROM entry ORDER BY updated DESC LIMIT ?, ?', (page*pagesize, pagesize))
        return c.fetchall()
