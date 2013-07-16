# -*- encoding: utf-8 -*-
#
# Copyright (C) 2013 Steve Frécinaux
#
# This module is part of hackerfeed and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Feed(Base):
    __tablename__ = 'feed'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    title = Column(String)
    entries = relationship("Entry", backref='feed')

    def __init__(self, url, title):
        self.url = url
        self.title = title

    def __unicode__(self):
        return u"%s — %s" % (self.title, self.url)


class Entry(Base):
    __tablename__ = 'entry'

    id = Column(String, primary_key=True)
    link = Column(String)
    title = Column(String)
    updated = Column(Integer)
    feed_id = Column(Integer, ForeignKey('feed.id'))

    def __init__(self, id, link, title, updated, feed):
        self.id = id
        self.link = link
        self.title = title
        self.updated = updated
        self.feed_id = feed.id

    def __repr__(self):
        return '<Entry("%s", "%s")>' % (self.id, self.title)
