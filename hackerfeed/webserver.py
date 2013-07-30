# -*- encoding: utf-8 -*-
#
# Copyright (C) 2013 Steve Frécinaux
#
# This module is part of hackerfeed and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


import os
from flask import Flask

from . import storage
from . import cli
from . import feeds
from . import models
from . import opml
from . import views

app = Flask(__name__)

@app.route('/')
def index():
    return page(1);

@app.route('/p<int:pageno>.html')
def page(pageno):
    pageno -= 1

    session = storage.Store.instance.session()
    pagesize = 30

    entries = session.query(models.Entry).order_by('updated desc').offset(pageno*100).limit(100)
    variables = {
        'entries': entries.all(),
        'pageno': pageno,
        'pagesize': pagesize,
    }
    return views.env.get_template('page.html').render(**variables).encode('UTF-8')

@app.route('/style.css')
def stylesheet():
    return (views.env.get_template('style.css').render().encode('UTF-8'),
            200,
            { 'Content-type': 'text/css; charset=utf-8' })
