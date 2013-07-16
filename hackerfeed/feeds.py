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
    def __init__(self, session):
        self.session = session

    def __get_entry_id(self, entry):
        if 'id' in entry:
            return entry.id
        return entry.link

    def __get_entry_date(self, entry):
        for field in ('published', 'updated', 'created'):
            if field in entry:
                return time.mktime(entry[field + '_parsed'])

    def __get_entry_author(self, entry):
        if 'author_detail' in entry:
            return entry.author_detail.name

    def parse(self, feed):
        p = feedparser.parse(feed.url)
        for entry in p.entries:
            yield models.Entry(self.__get_entry_id(entry), entry.link, entry.title,
                               self.__get_entry_date(entry), self.__get_entry_author(entry), feed)

    def import_feed(self, feed):
        for entry in self.parse(feed):
            self.session.add_or_ignore(entry)
