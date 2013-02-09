#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Avalon Music Server
#
# Copyright 2013 TSH Labs <projects@tshlabs.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from __future__ import print_function

import os
import re
import subprocess

try:
    from setuptools import setup, Command
except ImportError:
    from distutils.core import setup, Command


AUTHOR = 'TSH Labs'
DESCRIPTION = 'Avalon Music Server'
EMAIL = 'projects@tshlabs.org'
URL = 'http://www.tshlabs.org/'
LICENSE = 'BSD'
CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: BSD License",
    "Operating System :: POSIX",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Multimedia :: Sound/Audio"
    ]


_VERSION_FILE = 'VERSION'


def get_requires(filename):
    """Get the required packages from the pip file."""
    out = []
    with open(filename, 'rb') as handle:
        for line in handle:
            package, _ = re.split('[^\w\-]', line, 1)
            out.append(package.strip())
    return out


def get_contents(filename):
    """Get the contents of the given file."""
    with open(filename, 'rb') as handle:
        return handle.read().strip()


class VersionGenerator(Command):

    """Command to generate the current release from git."""

    description = "Generate the release version from the git tag"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def _get_version_from_git(self):
        """Get the current release version from git."""
        proc = subprocess.Popen(
            ['git', 'describe', '--tags', '--abbrev=0'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        (out, err) = proc.communicate()
        tag = out.strip()

        if not tag:
            raise ValueError('Could not determine tag: [%s]' % err)
        try:
            return tag.split('-')[1]
        except ValueError:
            raise ValueError('Could not determine version: [%s]' % tag)

    def _write_version(self, filename):
        """Write the current release version from git to a file."""
        with open(filename, 'wb') as handle:
            handle.write(self._get_version_from_git())

    def run(self):
        """Write the current release version from Git."""
        self._write_version(_VERSION_FILE)


class StaticCompilation(Command):

    """Command to compress and concatenate CSS and JS"""

    description = "Build static assets for the status page"

    user_options = []

    _static_base = 'avalon/web/data'

    _css_files = ['css/bootstrap.css', 'css/bootstrap-responsive.css', 'css/avalon.css']

    _js_files = ['js/jquery.js', 'js/bootstrap.js', 'js/mustache.js']

    _yui = '/opt/yui/current.jar'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def _compress(self, contents, out_file):
        """Compress the given contents and write it to the output file."""
        ext = os.path.splitext(out_file)[1].lstrip('.')

        proc = subprocess.Popen(
            ['java', '-jar', self._yui, '--type', ext, '-o', out_file],
            stdin=subprocess.PIPE, stdout=None, stderr=subprocess.PIPE)

        out, err = proc.communicate(input=contents)
        if 0 != proc.wait():
            raise OSError("Could not minimize %s: %s" % (out_file, err))

    def _compress_all(self, all_files, out_file):
        """Compress the collection of files and write the contents to the
        given output file.
        """
        all_content = []
        for a_file in all_files:
            full_path = os.path.join(self._static_base, a_file)
            with open(full_path, 'rb') as handle:
                all_content.append(handle.read())
        self._compress('\n\n'.join(all_content), os.path.join(self._static_base, out_file))

    def run(self):
        """Compress all CSS and JS files and write them to respective
        single files.
        """
        self._compress_all(self._css_files, 'css/all.min.css')
        self._compress_all(self._js_files, 'js/all.min.js')


REQUIRES = get_requires('requires.txt')
README = get_contents('README.rst')
VERSION = None


try:
    VERSION = get_contents(_VERSION_FILE)
except IOError:
    pass


setup(
    name='avalonms',
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    long_description=README,
    author_email=EMAIL,
    classifiers=CLASSIFIERS,
    license=LICENSE,
    url=URL,
    cmdclass={
        'version': VersionGenerator,
        'static': StaticCompilation},
    install_requires=REQUIRES,
    packages=['avalon', 'avalon.app', 'avalon.tags', 'avalon.web'],
    package_data={'avalon.web': [
            'data/status.html',
            'data/config.ini',
            'data/css/*.css',
            'data/js/*.js',
            'data/img/*.png',

            ]},
    scripts=[os.path.join('bin', 'avalonmsd')])

