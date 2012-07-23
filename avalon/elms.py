# -*- coding: utf-8 -*-
#
# Avalon Music Server
#
# Copyright (c) 2012 TSH Labs <projects@tshlabs.org>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are
# met:
# 
# * Redistributions of source code must retain the above copyright 
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


"""
Immutable wrappers for model objects suitable for being rendered as JSON
"""


import collections


__all__ = [
    'IdNameElm',
    'TrackElm'
    ]


class IdNameElm(collections.namedtuple('_IdNameElm', ['id', 'name'])):

    __slots__ = ()

    """Immutable, hashable representation of a model with ID
    and name attributes (everything besides Tracks)"""


class TrackElm(collections.namedtuple('_TrackElm', [
        'id',
        'name',
        'track',
        'year', 
        'album',
        'album_id',
        'artist',
        'artist_id',
        'genre',
        'genre_id'])):
    
    __slots__ = ()

    """Immutable, hashable representation of a Track model"""
     
