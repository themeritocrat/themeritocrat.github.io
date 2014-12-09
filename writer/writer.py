#!/usr/bin/env python

'''
Publishes the blog.
'''

from __future__ import print_function
from datetime import datetime
import sys, os

try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser


class cfg(object):
    out_d = '..'
    posts_d = 'posts'
    template = 'template.htm'
    css = 'style.css'
    date_fmt = '%Y %m %d %H %M'
    posts_per_page = 5


class metaparser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.done = False
        self.meta = {}

    def handle_comment(self, data):
        if not self.done:
            lines = data.split('\n')
            for l in lines:
                t = [x.strip() for x in l.split(':', 1)]
                if len(t) < 2:
                    continue
                key = t[0].lower()
                val = t[1]
                self.meta[key] = val
            self.done = True


class post(object):
    def __init__(self, html):
        p = metaparser()
        p.feed(html)
        p.close()
        self.date = datetime.strptime(p.meta['date'], cfg.date_fmt) if 'date' in p.meta else None
        self.title = p.meta['title'] if 'title' in p.meta else None
        self.tags = p.meta['tags'].split() if 'tags' in p.meta else None 
        self.content = html[html.find('-->') + 3:]

        print(self.date, self.title, self.tags)
        print(self.content)

if __name__ == '__main__':
    p = post(open('test.htm').read())
