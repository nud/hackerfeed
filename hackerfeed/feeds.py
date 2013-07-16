# -*- encoding: utf-8 -*-
#
# Copyright (C) 2013 Steve Frécinaux
#
# This module is part of hackerfeed and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


import feedparser
import time

import models


class FeedParser(object):
    def __init__(self, store):
        self.store = store

    def __get_entry_id(self, entry):
        if 'id' in entry:
            return entry.id
        return entry.link

    def __get_entry_date(self, entry):
        for field in ('published', 'updated', 'created'):
            if field in entry:
                return time.mktime(entry[field + '_parsed'])

    def parse(self, feed):
        p = feedparser.parse(feed.url)
        for entry in p.entries:
            yield models.Entry(self.__get_entry_id(entry), entry.link, entry.title, self.__get_entry_date(entry))

    def import_feed(self, feed):
        session = self.store.session()

        for entry in self.parse(feed):
            session.add_or_ignore(entry)
        session.commit()
