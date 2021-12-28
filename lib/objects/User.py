#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Database-ready "User" object
#
# Software is free software released under the "GNU Affero General Public License v3.0"
#
# Copyright (c) 2021  PidgeyL

from lib.DatabaseLayer   import DatabaseLayer as dbl
from lib.objects.helpers import multi_assert

class User:
    def __init__(self, id=None, charter_name=None, discord_id=None, email=None,
                 password=None, salt=None, hashcount=None, staff=None,
                 image_url=None, about=None, preferred_difficulty_id=None,
                 preferred_difficulty=None, preferred_language_id=None,
                 preferred_language=None):
        self.id           = id
        self.charter_name = charter_name
        self.discord_id   = discord_id
        self.email        = email
        self.password     = password
        self.salt         = salt
        self.hashcount    = hashcount
        self.staff        = staff
        self.image_url    = image_url
        self.about        = about
        if preferred_difficulty:
            self.preferred_difficulty = preferred_difficulty
        elif preferred_difficulty_id:
            self.preferred_difficulty = dbl.difficulty.get_by_id(preferred_difficulty_id)

        if preferred_language:
            self.preferred_language = preferred_language
        elif preferred_language_id:
            self.preferred_language = dbl.languages.get_by_id(preferred_language_id)
