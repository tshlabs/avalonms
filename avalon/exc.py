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


"""Errors thrown by the Avalon music server."""


__all__ = [
    'ApiError',
    'AvalonError',
    'ConnectionError',
    'DatabaseError',
    'InvalidParameterError',
    'PermissionError',
    'ServerNotReadyError'
    ]


class AvalonError(Exception):
    
    """Base for all exceptions."""

    def __init__(self, msg, err=None):
        """Set the error message and optional original error."""
        self.message = msg
        self.err = err

    def __str__(self):
        """Return a string representation of this error."""
        msg = self.message
        if None is not self.err:
            msg += ': %s' % self.err.message
        return msg

    @property
    def name(self):
        """The name of this error class."""
        return self.__class__.__name__


class DatabaseError(AvalonError):
    """There was an error performing an operation on the database."""
    pass


class ConnectionError(DatabaseError):
    """There was an error connecting to the database."""
    pass


class PermissionError(AvalonError):
    """We don't have the required permission."""
    pass


class ApiError(AvalonError):
    """Base for all errors relating to invalid API requests."""
    pass


class InvalidParameterError(ApiError):
    """An invalid parameter or parameter value was given."""
    pass


class ServerNotReadyError(ApiError):
    """The API server is not ready to handle requests."""
    pass

