# -*- encoding: utf-8 -*-
#
# Copyright (C) 2013 Steve Frécinaux
#
# This module is part of hackerfeed and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


import datetime
import jinja2


def dateformat(value, format='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.fromtimestamp(value).strftime(format)


class Environment(jinja2.Environment):
    def __init__(self):
        loader = jinja2.PackageLoader('hackerfeed', 'templates')
        super(Environment, self).__init__(loader=loader)
        self.__init_custom_filters()

    def __init_custom_filters(self):
        self.filters['dateformat'] = dateformat


env = Environment()
