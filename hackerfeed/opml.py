# -*- encoding: utf-8 -*-
#
# Copyright (C) 2013 Steve Frécinaux
#
# This module is part of hackerfeed and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


import xml.sax
from sqlalchemy.exc import IntegrityError

import models


class OpmlContentHandler(xml.sax.ContentHandler):
    def __init__(self, session):
        self.session = session

    def startElement(self, name, attrs):
        if name == 'outline' and 'title' in attrs and 'xmlUrl' in attrs:
            try:
                self.session.add(models.Feed(attrs['xmlUrl'], attrs['title']))
                self.session.commit()
            except IntegrityError, e:
                self.session.rollback()

class OpmlParser(object):
    def __init__(self, store):
        self.store = store

    def import_opml(self, filename):
        handler = OpmlContentHandler(self.store.session())

        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(open(filename, 'r'))
