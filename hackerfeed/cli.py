# -*- encoding: utf-8 -*-
#
# Copyright (C) 2013 Steve Frécinaux
#
# This module is part of hackerfeed and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import argparse

from . import HackerFeed


def parse_args():
    parser = argparse.ArgumentParser(description='Damn Simple RSS Client')
    parser.add_argument('--opml', dest='opml', default='hf.opml',
                        help='use the specified OPML file')

    subparsers = parser.add_subparsers(dest='command')

    subparser = subparsers.add_parser('generate', help='generate the HTML files')
    subparser.add_argument('--no-update', dest='update', action='store_false', default='true',
                           help='do not update the RSS feeds.')
    subparser.add_argument('dir', help='destination directory')

    subparser = subparsers.add_parser('add', help='add a new Atom/RSS feed')
    subparser.add_argument('--title', help='title of the feed')
    subparser.add_argument('url', help='url of the feed')

    return parser.parse_args()

def run():
    args = parse_args()

    hf = HackerFeed(args.opml)

    if args.command == 'generate':
        if args.update:
            hf.update_feeds()
        hf.generate(args.dir)

    elif args.command == 'add':
        hf.add(args.url, args.title)
