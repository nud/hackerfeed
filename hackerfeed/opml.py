# -*- encoding: utf-8 -*-
#
# Copyright (C) 2013 Steve Frécinaux
#
# This module is part of hackerfeed and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


import xml.sax

import models


class OpmlContentHandler(xml.sax.ContentHandler):
    def __init__(self, session):
        self.session = session

    def startElement(self, name, attrs):
        if name == 'outline' and 'title' in attrs and 'xmlUrl' in attrs:
            self.session.add_or_ignore(models.Feed(attrs['xmlUrl'], attrs['title']))


class OpmlParser(object):
    def __init__(self, store):
        self.store = store

    def import_opml(self, filename):
        session = self.store.session()
        handler = OpmlContentHandler(session)

        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(open(filename, 'r'))
        session.commit()
