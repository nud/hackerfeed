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
        return {
          'id': self.__get_entry_id(entry),
          'link': entry.link,
          'title': entry.title,
          'updated': self.__get_entry_date(entry),
          'author': self.__get_entry_author(entry)
        }

    def parse_url(self, url):
        p = feedparser.parse(url)
        return [self.__get_entry_fields(entry) for entry in p.entries]


def _parse_url_cb(params):
    feed_idx, feed_url = params
    return (feed_idx, _FeedFetcher().parse_url(feed_url))


class FeedParser(object):
    def __init__(self, opml, cache):
        self.opml = opml
        self.cache = cache

    def update_feeds(self):
        feed_list = self.opml.get_feeds()

        p = mp.Pool(4)

        for idx, entries in p.imap_unordered(_parse_url_cb, enumerate(x.url for x in feed_list)):
            print("Updating %s" % feed_list[idx].url, file=sys.stderr)
            self.cache.set_entry_list(feed_list[idx].url, entries)

        p.close()
        p.join()
