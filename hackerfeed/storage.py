# -*- encoding: utf-8 -*-
#
# Copyright (C) 2013 Steve Frécinaux
#
# This module is part of hackerfeed and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import os.path
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models


class Store(object):
    def __init__(self, filename):
        self.__init_engine(filename)

    def __init_engine(self, filename):
        db_exists = os.path.exists(filename)
        self.engine = create_engine('sqlite:///' + filename, echo=True)
        self.session = sessionmaker(bind=self.engine)

        if not db_exists:
            models.Base.metadata.create_all(self.engine)
