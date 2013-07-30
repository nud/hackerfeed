# -*- encoding: utf-8 -*-
#
# Copyright (C) 2013 Steve Frécinaux
#
# This module is part of hackerfeed and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import os.path
import time
from sqlalchemy import create_engine, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from . import models


class StoreSession(Session):
    def add_or_ignore(self, obj):
        self.begin(nested=True)
        try:
            self.add(obj)
            self.commit()
        except IntegrityError as e:
            self.rollback()


class Store(object):
    instance = None

    def __init__(self, filename):
        self.__init_engine(filename)
        Store.instance = self

    def __init_engine(self, filename):
        db_exists = os.path.exists(filename)

        # Here we do ugly workarounds for a pysqlite3 bug:
        # https://groups.google.com/forum/#!topic/sqlalchemy-devel/0lanNjxSpb0
        # https://groups.google.com/forum/#!topic/sqlalchemy/XTUf_Pe4cNA/discussion
        # It might break things!
        self.engine = create_engine('sqlite:///' + filename, connect_args={'isolation_level': None})
        self.session = sessionmaker(bind=self.engine, class_=StoreSession)

        @event.listens_for(self.engine, "begin")
        def do_begin(conn):
            conn.execute("BEGIN")

        if not db_exists:
            models.Base.metadata.create_all(self.engine)
