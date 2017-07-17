# -*- encoding: utf-8 -*-
#
# Copyright (C) 2013 Steve Frécinaux
#
# This module is part of hackerfeed and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


import xml.etree.ElementTree as etree


class Feed(object):
    def __init__(self, el):
        self.__element = el

    @property
    def url(self):
        return self.__element.get('xmlUrl')

    @property
    def title(self):
        return self.__element.get('title')


class Opml(object):
    def __init__(self, filename):
        self.filename = filename
        self.__tree = etree.parse(filename)

    def get_feeds(self):
        return [Feed(el) for el in self.__tree.getroot().find('body').findall('outline')]
