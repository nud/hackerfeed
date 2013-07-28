# -*- encoding: utf-8 -*-
#
# Copyright (C) 2013 Steve Frécinaux
#
# This module is part of hackerfeed and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


import os

import storage
import cli
import feeds
import models
import opml
import views


def hackerfeed(db_filename):
    store = storage.Store(db_filename)

    args = cli.parse_args()

    if args.opml:
        parser = opml.OpmlParser(store)
        parser.import_opml(args.opml)

    if args.poll:
        session = store.session()
        parser = feeds.FeedParser(session)
        parser.import_feeds(session.query(models.Feed).all())

    if args.generate:
        session = store.session()
        template = views.env.get_template('page.html')
        pagesize = 30

        for pageno in range(0, 10):
            entries = session.query(models.Entry).order_by('updated desc').offset(pageno*100).limit(100)
            variables = {
                'entries': entries.all(),
                'pageno': pageno,
                'pagesize': pagesize,
            }
            path = os.path.join(args.generate, 'p%02d.html' % (pageno+1))
            template.stream(**variables).dump(path, 'utf-8')

        views.env.get_template('style.css').stream().dump(os.path.join(args.generate, 'style.css'))
