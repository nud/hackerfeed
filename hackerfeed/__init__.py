# -*- encoding: utf-8 -*-
#
# Copyright (C) 2013 Steve Frécinaux
#
# This module is part of hackerfeed and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import os
import sys

from . import cache
from . import feeds
from . import renderer
from . import opml


class HackerFeed(object):
    def __init__(self, opml_filename):
        assert(os.path.isfile(opml_filename))

        self.opml = opml.Opml(opml_filename)
        self.cache_dir = os.path.join(os.path.dirname(opml_filename), '.hf-cache')

    def _get_feedparser(self):
        return feeds.FeedParser(self.opml, self.cache_dir)

    def _get_cache(self):
        return cache.Cache(self.cache_dir)

    def update_feeds(self):
        self._get_feedparser().update_feeds()

    def generate(self, dirname):
        render = renderer.Renderer(self.opml, self._get_cache())
        render(dirname)

    def add(self, url, title=None):
        if self.opml.has(url):
            print("URL '%s' is already present in '%s'" % (url, self.opml.filename), file=sys.stderr)
            sys.exit(1)
        else:
            if title is None:
                self._get_feedparser().update_feed(url)
                title = self._get_cache().get_metadata(url)['title']

            print('Adding feed with url %s and title "%s"' % (url, title))
            self.opml.add(url, title)
            self.opml.save()
