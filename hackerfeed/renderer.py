# -*- encoding: utf-8 -*-
#
# Copyright (C) 2013 Steve Frécinaux
#
# This module is part of hackerfeed and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import heapq
import os
import sys

from itertools import islice

from . import views

class Renderer(object):
    N_PAGES = 10
    PAGE_SIZE = 30

    def __init__(self, opml, cache):
        self.opml = opml
        self.cache = cache
        self.env = views.Environment()

    def get_iterator(self, feed):
        for item in self.cache.get_entry_list(feed.url):
            yield (-item['updated'], dict(feed=feed, **item))

    def render_pages(self, dirname):
        template = self.env.get_template('page.html')

        iterables = [self.get_iterator(feed) for feed in self.opml.get_feeds()]
        all_entries = (item for (key, item) in heapq.merge(*iterables))

        for pageno in range(self.N_PAGES):
            variables = {
                'entries': list(islice(all_entries, self.PAGE_SIZE)),
                'pageno': pageno,
                'pagesize': self.PAGE_SIZE,
            }
            path = os.path.join(dirname, 'p%02d.html' % (pageno+1))
            template.stream(**variables).dump(path, 'utf-8')
            print("Generated '%s'" % path, file=sys.stderr)

    def render_css(self, dirname):
        path = os.path.join(dirname, 'style.css')
        self.env.get_template('style.css').stream().dump(path)
        print("Generated '%s'" % path, file=sys.stderr)

    def __call__(self, dirname):
        self.render_pages(dirname)
        self.render_css(dirname)
