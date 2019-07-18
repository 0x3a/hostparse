#!/usr/bin/env python3

#import re
import os
import sys
import difflib
import argparse
from itertools import tee

# py3 "compatible"
try:
    import urlparse
except:
    import urllib.parse as urlparse

import tldextract


"""
    The tool is very simple and just maps -known- arguments through an objector dict. 
    It might not be pretty but its surprisingly efficient.
"""

# Taken from: https://mail.python.org/pipermail/tutor/2003-November/026645.html
class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)


# Remove buffering, processing large datasets eats memory otherwise
sys.stdout = Unbuffered(sys.stdout)

# Taken from https://goodcode.io/articles/python-dict-object/
class ObjDict(dict):
    def from_dict(self, d):
        for key, value in d.items():
            self[key] = value
        return self

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)

def parse_url(url):
    o = ObjDict()
    p_url = urlparse.urlparse(url)
    t_url = tldextract.extract(url)

    o.filename = p_url.path.split("/")[-1]
    o.scheme = p_url.scheme
    o.username = p_url.username
    o.password = p_url.password
    o.subdomain = t_url.subdomain
    o.domain = t_url.domain
    o.tld = t_url.suffix
    o.hostname = p_url.hostname
    o.suffix = t_url.suffix
    o.port = p_url.port
    o.path = p_url.path
    o.params = p_url.params
    o.query = p_url.query
    o.fragment = p_url.fragment

    return o

KEYWORDS = [
    'username',
    'domain',
    'fragment',
    'query',
    'path',
    'password',
    'port',
    'subdomain',
    'hostname',
    'filename',
    'params',
    'tld',
    'scheme'
]

def process_args():
    parser = argparse.ArgumentParser(prog='hostparse')
    parser.add_argument('-d', '--delimiter', dest='delim', default='.', help="Output delimiter.")
    parser.add_argument('format', nargs=None,
                        help="Format keywords seperated by a comma. Keywords: scheme, username, password, subdomain, \
                        domain, hostname, tld, port, path, filename, params, query, fragment. It matches the shortest \
                        match (ho is hostname, t is tld, p is unknown, po is port).")
    args = parser.parse_args()

    format_str = []
    for format_keyword in args.format.split(','):
        km = [item for item in KEYWORDS if item.startswith(format_keyword)]
        if len(km) > 1:
            parser.error("Supplied format key '{k}' isn't specific enough, matches multiple keywords ({m}).".format(k=format_keyword, m=','.join(km)))

        if len(km) < 1:
            parser.error("Supplied format key '{k}' doesn't match any keyword.".format(k=format_keyword))

        format_str.append(km[0])

    return format_str, args.delim


def main():
    format_str, delim = process_args()
    for line in sys.stdin:
        line = line.rstrip()
        print(delim.join([getattr(parse_url(line), fk) for fk in format_str]))

