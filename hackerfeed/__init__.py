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
import cli
import models
import opml
import views


def hackerfeed(db_filename):
    models.init_storage(db_filename)

    args = cli.parse_args()

    if args.opml:
        opml.import_opml(args.opml)

    fc = cache.FeedCache()

    if args.poll:
        for feed in models.session.query(models.Feed).all():
            p = feedparser.parse(feed.url)
            for entry in p.entries:
                fc.add_entry(entry)

    if args.generate:
        template = views.env.get_template('page.html')
        pagesize = 100

        for pageno in range(0, 10):
            variables = {
                'entries': fc.get_entries(pageno, pagesize),
                'pageno': pageno,
                'pagesize': pagesize,
            }
            path = os.path.join(args.generate, 'p%02d.html' % (pageno+1))
            template.stream(**variables).dump(path, 'utf-8')
