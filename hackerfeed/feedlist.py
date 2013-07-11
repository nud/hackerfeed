# -*- encoding: utf-8 -*-
#
# Copyright (C) 2013 Steve Frécinaux
#
# This module is part of hackerfeed and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


import xml.sax


class Feed(object):
    def __init__(self, url, title):
        self.url = url
        self.title = title

    def __unicode__(self):
        return u"%s — %s" % (self.title, self.url)


class OpmlContentHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.feeds = []

    def startElement(self, name, attrs):
        if name == 'outline' and 'title' in attrs and 'xmlUrl' in attrs:
            self.feeds.append(Feed(attrs['xmlUrl'], attrs['title']))


class FeedList(object):
    def __init__(self, path):
        self.feeds = self.__parse_opml(path)

    def __parse_opml(self, path):
        handler = OpmlContentHandler()

        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(open(path, 'r'))

        return handler.feeds
