# -*- encoding: utf-8 -*-
#
# Copyright (C) 2013 Steve Frécinaux
#
# This module is part of hackerfeed and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Entry(Base):
    __tablename__ = 'entries'

    id = Column(String, primary_key=True)
    link = Column(String)
    title = Column(String)
    updated = Column(Integer)

    def __init__(self, id, link, title, updated):
        self.id = id
        self.link = link
        self.title = title
        self.updated = updated

    def __repr__(self):
        return '<Entry("%s", "%s")>' % (self.id, self.title)


Session = sessionmaker()


engine = None
session = None
def init_storage(filename):
    global engine, session

    if engine is None:
        db_exists = os.path.isfile(filename)
        engine = create_engine('sqlite:///' + filename, echo=True)

        if not db_exists:
            Base.metadata.create_all(engine)

    if session is None:
        Session.configure(bind=engine)
        session = Session()
