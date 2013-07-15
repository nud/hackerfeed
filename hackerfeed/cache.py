# -*- encoding: utf-8 -*-
#
# Copyright (C) 2013 Steve Frécinaux
#
# This module is part of hackerfeed and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import os.path
import time
from sqlalchemy.exc import IntegrityError

import models


class FeedCache(object):
    def __get_entry_id(self, entry):
        if 'id' in entry:
            return entry.id
        return entry.link

    def __get_entry_date(self, entry):
        for field in ('published', 'updated', 'created'):
            if field in entry:
                return time.mktime(entry[field + '_parsed'])

    def add_entry(self, entry):
        try:
            entry = models.Entry(self.__get_entry_id(entry), entry.link, entry.title, self.__get_entry_date(entry))
            models.session.add(entry)
            models.session.commit()
        except IntegrityError, e:
            models.session.rollback()

    def get_entries(self, page=0, pagesize=100):
        return models.session.query(models.Entry).order_by('updated desc').offset(page*pagesize).limit(pagesize).all()
