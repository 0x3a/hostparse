#!/usr/bin/env python3

import os
from setuptools import setup, find_packages

import hostparse

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
        name = 'hostparse',
        version = hostparse.__version__,
        author = 'Yonathan Klijnsma',
        author_email = 'admin@0x3a.com',
        url = 'https://github.com/0x3a/hostparse',
        packages=find_packages(),
        include_package_data=True,
        description = 'A command-line client for URL and hostname swizzling ',
        long_description=read('README.md'),
        install_requires=[
            'tldextract',
        ],
        entry_points={
            'console_scripts': [
                'hostparse=hostparse:main',
            ],
        },
        zip_safe=False,
     )
