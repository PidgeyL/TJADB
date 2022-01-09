#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Database-ready "User" object
#
# Software is free software released under the "GNU Affero General Public License v3.0"
#
# Copyright (c) 2021-2022  PidgeyL

from copy                import copy
from lib.DatabaseLayer   import DatabaseLayer as dbl
from lib.objects.helpers import multi_assert, Object

class User(Object):
    def __init__(self, id=None, charter_name=None, discord_id=None, email=None,
                 password=None, salt=None, hashcount=None, staff=None,
                 image_url=None, about=None, preferred_difficulty_id=None,
                 preferred_difficulty=None, preferred_language_id=None,
                 preferred_language=None):
        self._id          = id
        self.charter_name = charter_name
        self.discord_id   = discord_id
        self.email        = email
        self.password     = password
        self.salt         = salt
        self.hashcount    = hashcount
        self.staff        = bool(staff)
        self.image_url    = image_url
        self.about        = about
        if preferred_difficulty:
            self.preferred_difficulty = preferred_difficulty
        else:
            self.preferred_difficulty = dbl().difficulties.get_by_id(preferred_difficulty_id)

        if preferred_language:
            self.preferred_language = preferred_language
        else:
            self.preferred_language = dbl().languages.get_by_id(preferred_language_id)


    def verify(self):
        from lib.objects import Language, Difficulty
        multi_assert(self._id, self.discord_id, self.hashcount,
                                                 types=( int,        type(None) ))
        multi_assert(self.charter_name, self.email, self.password, self.salt,
                     self.image_url, self.about, types=( str,        type(None) ))
        multi_assert(self.staff,                 types=( bool ))
        multi_assert(self.preferred_language,    types=( Language,   type(None) ))
        multi_assert(self.preferred_difficulty,  types=( Difficulty, type(None) ))

    def as_dict(self):
        d = copy(vars(self))
        d['id'] = self._id
        d['preferred_difficulty_id'] = None
        d['preferred_language_id']   = None

        if self.preferred_difficulty:
            d['preferred_difficulty_id'] = self.preferred_difficulty.id
        if self.preferred_language:
            d['preferred_language_id'] = self.preferred_language.id
        for k in ['_id', 'preferred_difficulty', 'preferred_language']:
            del d[k]
        return d
