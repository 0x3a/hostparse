#!/usr/bin/env python3

#import re
import os
import sys
import difflib
import argparse
from itertools import tee

# Py3 compatible
try:
    import urlparse
except:
    import urllib.parse as urlparse

import tldextract


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

"""
    The tool is very simple and just maps -known- arguments through mapper dicts. The dict maps to functions which
    return generators to retrieve global parsed data. It might not be pretty but its surprisingly efficient.
"""
DATA_MAPPER = dict(
    tldextract=None,
    urlparse=None
)

def fill_mappers(url):
    global DATA_MAPPER
    DATA_MAPPER['tldextract'] = tldextract.extract(url)
    DATA_MAPPER['urlparse'] = urlparse.urlparse(url)

def mapper_func(obj_val):
    return getattr(DATA_MAPPER[obj_val[0]], obj_val[1])

# People will scream at me for this, I like generators.
def yield_basename(obj_val):
    yield os.path.basename(mapper_func(obj_val))

KEYWORD_MAPPER = {
    "scheme": ('urlparse', 'scheme'),
    "username": ('urlparse', 'username'),
    "password": ('urlparse', 'password'),
    "subdomain": ('tldextract', 'subdomain'),
    "domain": ('tldextract', 'domain'),
    "hostname": ('urlparse', 'hostname'),
    "tld": ('tldextract', 'suffix'),
    "port": ('urlparse', 'port'),
    "path": ('urlparse', 'path'),
    #"filename": yield_basename(mapper_func(('urlparse', 'path'))),
    "params": ('urlparse', 'params'),
    "query": ('urlparse', 'query'),
    "fragment": ('urlparse', 'fragment'),
}


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
        km = [item for item in KEYWORD_MAPPER.keys() if item.startswith(format_keyword)]
        if len(km) > 1:
            parser.error("Supplied format key '{k}' isn't specific enough, matches multiple keywords ({m}).".format(k=format_keyword, m=','.join(km)))

        if len(km) < 1:
            parser.error("Supplied format key '{k}' doesn't match any keyword.".format(k=format_keyword))

        format_str.append(km[0])

    return format_str, args.delim


def main():
    args, delim = process_args()
    for line in sys.stdin.readlines():
        line = line.rstrip()
        fill_mappers(line)
        print(delim.join([mapper_func(KEYWORD_MAPPER[fk]) for fk in args]))

