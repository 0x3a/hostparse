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
        long_description_content_type="text/markdown",
        install_requires=[
            'tldextract',
        ],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        entry_points={
            'console_scripts': [
                'hostparse=hostparse:main',
            ],
        },
     )
