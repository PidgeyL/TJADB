#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Database-ready "Source" object
#
# Software is free software released under the "GNU Affero General Public License v3.0"
#
# Copyright (c) 2021-2022  PidgeyL

from copy import copy

from lib.DatabaseLayer   import DatabaseLayer as dbl
from lib.objects.Genre   import Genre
from lib.objects.helpers import multi_assert, Object

class Source(Object):
    def __init__(self, id=None, name_orig=None, name_en=None, genre_id=None,
                 genre=None, about=None):
        self._id       = id
        self.name_orig = name_orig
        self.name_en   = name_en
        self.about     = about
        if genre:
            self.genre = genre
        elif genre_id:
            self.genre = dbl().genres.get_by_id(genre_id)
        else:
            self.genre = None


    def verify(self):
        multi_assert(self._id,                     types=( int,   type(None) ))
        multi_assert(self.name_orig, self.name_en, types=  str )
        multi_assert(self.about,                   types=( str,   type(None) ))
        multi_assert(self.genre,                   types=( Genre, type(None) ))


    def as_dict(self):
        d = copy(vars(self))
        d['genre_id'] = d['genre'].id if self.genre else None
        d['id']       = self._id
        del d['genre']
        del d['_id']
        return d
