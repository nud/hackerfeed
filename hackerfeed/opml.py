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
    def startElement(self, name, attrs):
        if name == 'outline' and 'title' in attrs and 'xmlUrl' in attrs:
            try:
                models.session.add(models.Feed(attrs['xmlUrl'], attrs['title']))
                models.session.commit()
            except IntegrityError, e:
                models.session.rollback()


def import_opml(path):
    handler = OpmlContentHandler()

    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    parser.parse(open(path, 'r'))
