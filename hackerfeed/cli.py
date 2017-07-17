# -*- encoding: utf-8 -*-
#
# Copyright (C) 2013 Steve Frécinaux
#
# This module is part of hackerfeed and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import argparse

from . import hf


def parse_args():
    parser = argparse.ArgumentParser(description='Damn Simple RSS Client')
    parser.add_argument('--opml', dest='opml', help='import an OPML file')
    parser.add_argument('--poll', dest='poll', action='store_true', help='poll the configured list of feeds.')
    parser.add_argument('--generate', dest='generate', help='generate the HTML files')

    return parser.parse_args()

def run():
    args = parse_args()

    if args.opml:
        hf.import_opml(args.opml)
    if args.poll:
        hf.update_feeds()
    if args.generate:
        hf.generate(args.generate)
