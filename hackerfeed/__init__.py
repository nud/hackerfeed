# -*- encoding: utf-8 -*-
#
# Copyright (C) 2013 Steve Frécinaux
#
# This module is part of hackerfeed and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


import os

from . import storage
from . import feeds
from . import models
from . import opml
from . import views


DB_FILENAME = 'cache.db'


class HackerFeed(object):
    def __init__(self):
        self.store = storage.Store(DB_FILENAME)
        self.env = views.Environment()

    def import_opml(self, filename):
        opml.OpmlParser(self.store).import_opml(filename)

    def update_feeds(self):
        session = self.store.session()
        parser = feeds.FeedParser(session)
        parser.import_feeds(session.query(models.Feed).all())

    def generate(self, dirname):
        session = self.store.session()
        template = self.env.get_template('page.html')
        pagesize = 30

        for pageno in range(0, 10):
            entries = session.query(models.Entry).order_by('updated desc').offset(pageno*100).limit(100)
            variables = {
                'entries': entries.all(),
                'pageno': pageno,
                'pagesize': pagesize,
            }
            path = os.path.join(dirname, 'p%02d.html' % (pageno+1))
            template.stream(**variables).dump(path, 'utf-8')

        self.env.get_template('style.css').stream().dump(os.path.join(dirname, 'style.css'))
