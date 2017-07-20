# -*- encoding: utf-8 -*-
#
# Copyright (C) 2013 Steve Frécinaux
#
# This module is part of hackerfeed and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import heapq
import itertools
import os
import sys

from . import cache
from . import feeds
from . import opml
from . import views


class HackerFeed(object):
    def __init__(self, opml_filename):
        assert(os.path.isfile(opml_filename))

        self.opml = opml.Opml(opml_filename)
        self.cache = cache.Cache(os.path.join(os.path.dirname(opml_filename), '.hf-cache'))
        self.env = views.Environment()

    def _get_feedparser(self):
        return feeds.FeedParser(self.opml, self.cache)

    def update_feeds(self):
        self._get_feedparser().update_feeds()

    def generate(self, dirname):
        template = self.env.get_template('page.html')
        pagesize = 30

        def generator(feed):
            for item in self.cache.get_entry_list(feed.url):
                yield (-item['updated'], dict(feed=feed, **item))

        iterables = []
        for feed in self.opml.get_feeds():
            iterables.append(generator(feed))
        all_entries = (item for (key, item) in heapq.merge(*iterables))

        for pageno in range(0, 10):
            entries = list(itertools.islice(all_entries, pagesize))
            variables = {
                'entries': entries,
                'pageno': pageno,
                'pagesize': pagesize,
            }
            path = os.path.join(dirname, 'p%02d.html' % (pageno+1))
            template.stream(**variables).dump(path, 'utf-8')

        self.env.get_template('style.css').stream().dump(os.path.join(dirname, 'style.css'))

    def add(self, url, title=None):
        if self.opml.has(url):
            print("URL '%s' is already present in '%s'" % (url, self.opml.filename), file=sys.stderr)
            sys.exit(1)
        else:
            if title is None:
                info = self._get_feedparser().fetch_feed_info(url)
                title = info['title']

            print('Adding feed with url %s and title "%s"' % (url, title))
            self.opml.add(url, title)
            self.opml.save()
