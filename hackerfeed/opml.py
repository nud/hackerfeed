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

    def __body(self):
        return self.__tree.getroot().find('body')

    def get_feeds(self):
        return [Feed(el) for el in self.__body().findall('outline')]

    def has(self, url):
        return any(f.url == url for f in self.get_feeds())

    def add(self, url, title):
        child = etree.Element('outline')
        self.__body().append(child)
        child.set('xmlUrl', url)
        child.set('title', title)

    def save(self):
        self.__tree.write(self.filename)
