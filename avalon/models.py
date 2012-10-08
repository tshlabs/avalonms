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
Models representing types of metadata loaded from a music collection
along with functionality to manage connections to the backing database.
"""


import uuid

from sqlalchemy import (
    create_engine,
    CHAR,
    Column,
    ForeignKey,
    Integer,
    String,
    TypeDecorator)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import ArgumentError, OperationalError, SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

import avalon.exc


__all__ = [
    'Album',
    'Artist',
    'Base',
    'Genre',
    'SessionHandler',
    'Track',
    'UUIDType'
    ]


class UUIDType(TypeDecorator):
    """Platform-independent GUID type.

    See http://docs.sqlalchemy.org/en/rel_0_7/core/types.html
    """

    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        elif not isinstance(value, uuid.UUID):
            return "%.32x" % uuid.UUID(value)
        return "%.32x" % value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return uuid.UUID(value)


class Base(object):

    """A Base for all models that defines name and id fields."""

    id = Column(UUIDType, primary_key=True)
    name = Column(String)


Base = declarative_base(cls=Base)


class Track(Base):
    
    """Model representing metadata of a media file with
    relations to other entities (album, artist, genre).
    """
    
    __tablename__ = 'tracks'
 
    track = Column(Integer)
    year = Column(Integer)

    album_id = Column(UUIDType, ForeignKey('albums.id'), index=True)
    artist_id = Column(UUIDType, ForeignKey('artists.id'), index=True)
    genre_id = Column(UUIDType, ForeignKey('genres.id'), index=True)

    album = relationship('Album', backref='tracks', lazy='joined', order_by='Track.id')
    artist = relationship('Artist', backref='tracks', lazy='joined', order_by='Track.id')
    genre = relationship('Genre', backref='tracks', lazy='joined', order_by='Track.id')


class Album(Base):
    
    """Model that represents the album of a song."""
    
    __tablename__ = 'albums'


class Artist(Base):

    """Model that represents the artist of a song."""

    __tablename__ = 'artists'


class Genre(Base):

    """Model that represents the genre of a song."""

    __tablename__ = 'genres'


class SessionHandler(object):

    """Wrapper for connecting to a database and generating
    new sessions.
    """

    def __init__(self, url, log):
        """Initialize the session factory and database connection."""
        self._url = url
        self._log = log
        self._session_factory = sessionmaker()
        self._engine = None

    def close(self, session):
        """Safely close a session."""
        if session is None:
            return
        try:
            session.close()
        except SQLAlchemyError, e:
            self._log.warn('Problem closing session: %s', e.message, exc_info=True)

    def connect(self, clean=False):
        """Connect to the database and configure the session factory
        to use the connection, and create any needed tables (optionally
        dropping them first).
        """
        try:
            # Attempt to connect to the engine immediately after it
            # is created in order to make sure it's valid and flush
            # out any errors we're going to encounter before trying
            # to create tables or insert into it.
            self._engine = create_engine(self._url)
            self.validate()
        except ArgumentError, e:
            raise avalon.exc.ConnectionError(
                'Invalid database path or URL %s' % self._url, e)
        except OperationalError, e:
            raise avalon.exc.ConnectionError(
                'Could not connect to database URL %s' % self._url, e)
        except ImportError, e:
            raise avalon.exc.ConnectionError(
                'Invalid database connector', e)

        self._session_factory.configure(bind=self._engine)

        if clean:
            try:
                Base.metadata.drop_all(self._engine)
            except OperationalError, e:
                raise avalon.exc.PermissionError(
                    'Insufficient permission to remove existing tables or '
                    'data in the database [%s]' % self._url, e)        
        Base.metadata.create_all(self._engine)

    def get_open_paths(self):
        """Return the path to the database being used (if we are using
        a file-backed DB engine).

        This is more-or-less a hack to deal with having to open the db
        while we have root permissions but then dropping them and still
        expecting to be able to write to the database.
        """
        db_url = make_url(self._url)
        if 'sqlite' != db_url.drivername:
            return []
        return [db_url.database]

    def validate(self):
        """Ensure our database engine is valid by attempting a connection."""
        conn = None
        
        try:
            conn = self._engine.connect()
        finally:
            self.close(conn)

    def get_session(self):
        """Get a new session."""
        return self._session_factory()

