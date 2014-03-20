#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Avalon Music Server
#
# Copyright 2012-2014 TSH Labs <projects@tshlabs.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#


from __future__ import print_function
import sys

import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from avalon import __version__

DESCRIPTION = 'Avalon Music Server'
AUTHOR = 'TSH Labs'
EMAIL = 'projects@tshlabs.org'
URL = 'http://www.tshlabs.org/'
LICENSE = 'MIT'
CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: MIT License",
    "Operating System :: POSIX",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Multimedia :: Sound/Audio",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7"
]


def get_contents(filename):
    """Get the contents of the given file."""
    with open(filename, 'rb') as handle:
        return handle.read().strip()


# If this is a version of Python prior to 2.7, argparse was
# not included in the standard library and we must list it as
# an installation dependency.
_python_version = (sys.version_info[0], sys.version_info[1])
_argparse_included = (2, 7)

REQUIRES = [
    'cherrypy',
    'mutagen',
    'simplejson',
    'sqlalchemy'
]

if _python_version < _argparse_included:
    REQUIRES.append('argparse')

README = get_contents('README.rst')

setup(
    name='avalonms',
    version=__version__,
    author=AUTHOR,
    description=DESCRIPTION,
    long_description=README,
    author_email=EMAIL,
    classifiers=CLASSIFIERS,
    license=LICENSE,
    url=URL,
    install_requires=REQUIRES,
    packages=['avalon', 'avalon.app', 'avalon.tags', 'avalon.web'],
    scripts=[os.path.join('bin', 'avalonmsd')])

