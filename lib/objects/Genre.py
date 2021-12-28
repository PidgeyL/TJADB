#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Database-ready "Genre" object
#
# Software is free software released under the "GNU Affero General Public License v3.0"
#
# Copyright (c) 2021  PidgeyL

from lib.DatabaseLayer   import DatabaseLayer as dbl
from lib.objects.helpers import multi_assert, Object

class Genre(Object):
    def __init__(self, id=None, name_en=None, name_jp=None, tja_genre=None):
        self.id        = id
        self.name_en  = name_en
        self.name_jp  = name_jp
        self.tja_genre = tja_genre


    def verify(self):
        multi_assert(self.id, types=( int, type(None) ))
        multi_assert(self.name_en, self.name_jp, self.tja_genre, types=(str))
