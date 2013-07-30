# -*- encoding: utf-8 -*-
#
# Copyright (C) 2013 Steve Frécinaux
#
# This module is part of hackerfeed and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


import feedparser
import time
import multiprocessing as mp
import sys

from . import models


class _FeedFetcher(object):
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

    def __get_entry_fields(self, entry):
        return (
            self.__get_entry_id(entry),
            entry.link,
            entry.title,
            self.__get_entry_date(entry),
            self.__get_entry_author(entry)
        )

    def parse_url(self, url):
        p = feedparser.parse(url)
        return [self.__get_entry_fields(entry) for entry in p.entries]


def _parse_url_cb(params):
    feed_idx, feed_url = params
    return (feed_idx, _FeedFetcher().parse_url(feed_url))


class FeedParser(object):
    def __init__(self, session):
        self.session = session

    def import_feeds(self, feed_list):
        n_feeds = len(feed_list)

        p = mp.Pool(4)

        for feed_idx, entries in p.imap_unordered(_parse_url_cb, [(i, feed_list[i].url) for i in range(n_feeds)]):
            print >>sys.stderr, "Updating %s" % feed_list[feed_idx].url
            for entry in entries:
                params = entry + (feed_list[feed_idx],)
                self.session.add_or_ignore(models.Entry(*params))
            self.session.commit()

        p.close()
        p.join()
