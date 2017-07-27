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

from itertools import repeat

from . import cache

class _FeedFetcher(object):
    def __init__(self, cache_dir):
        self.__cache = cache.Cache(cache_dir)

    def __get_entry_id(self, entry):
        if 'id' in entry:
            return entry.id
        return entry.link

    def __get_entry_date(self, entry):
        for field in ('published', 'updated', 'created'):
            if field in entry:
                return time.mktime(entry[field + '_parsed'])

    def __get_entry_author(self, entry):
        if 'author_detail' in entry and hasattr(entry.author_detail, 'name'):
            return entry.author_detail.name

    def __get_entry_fields(self, entry):
        return {
            'id': self.__get_entry_id(entry),
            'link': entry.link,
            'title': entry.get('title', 'Untitled'),
            'updated': self.__get_entry_date(entry),
            'author': self.__get_entry_author(entry)
        }

    def __get_info_fields(self, parser):
        return {
            'title': parser.feed.title,
            'etag': parser.get('etag'),
            'modified': parser.get('modified'),
        }

    def parse_url(self, url):
        info = self.__cache.get_metadata(url)
        p = feedparser.parse(url, etag=info.get('etag'), modified=info.get('modified'))
        if p.status == 200:
            info = self.__get_info_fields(p)
            entries = [self.__get_entry_fields(entry) for entry in p.entries]
            self.__cache.set_entry_list(url, entries)
            self.__cache.set_metadata(url, info)
        return info


def _parse_url_cb(params):
    feed_url, cache_dir = params
    return (feed_url, _FeedFetcher(cache_dir).parse_url(feed_url))


class FeedParser(object):
    def __init__(self, opml, cache_dir):
        self.opml = opml
        self.cache_dir = cache_dir

    def fetch_feed_info(self, url):
        return _FeedFetcher(self.cache_dir).parse_url(url)[1]

    def update_feeds(self):
        feed_list = self.opml.get_feeds()

        p = mp.Pool(4)

        params = zip((feed.url for feed in feed_list), repeat(self.cache_dir))
        for feed_url, info in p.imap_unordered(_parse_url_cb, params):
            print("Updated %s" % feed_url, file=sys.stderr)

        p.close()
        p.join()
