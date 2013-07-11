# -*- encoding: utf-8 -*-
#
# Copyright (C) 2013 Steve Frécinaux
#
# This module is part of hackerfeed and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


import collections
import feedparser
import os

import cache
import feedlist
import views


def hackerfeed(opml_filename, db_filename, base_path):
    Entry = collections.namedtuple('Entry', ['id', 'link', 'title', 'updated'])

    fl = feedlist.FeedList(opml_filename)
    fc = cache.FeedCache(db_filename)

    for feed in fl.feeds:
        p = feedparser.parse(feed.url)
        for entry in p.entries:
            fc.add_entry(entry)

    template = views.env.get_template('page.html')

    pagesize = 100

    for pageno in range(0, 10):
        variables = {
            'entries': [Entry(*x) for x in fc.get_entries(pageno, pagesize)],
            'pageno': pageno,
            'pagesize': pagesize,
        }
        path = os.path.join(base_path, 'p%02d.html' % (pageno+1))

        template.stream(**variables).dump(path, 'utf-8')
