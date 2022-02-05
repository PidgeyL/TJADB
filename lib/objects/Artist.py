#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Database-ready "Artist" object
#
# Software is free software releasedunder the "GNU Affero General Public License v3.0"
#
# Copyright (c) 2021-2022  PidgeyL

from lib.objects.helpers import multi_assert, Object

class Artist(Object):
    def __init__(self, id=None, name_orig=None, name_en=None, link=None,
                 info=None):
        self._id       = id
        self.name_orig = name_orig
        self.name_en   = name_en
        self.link      = link
        self.info      = info


    def verify(self):
        multi_assert(self._id,                     types=( int, type(None) ))
        multi_assert(self.name_orig, self.name_en, types=( str ))
        multi_assert(self.link, self.info,         types=( str, type(None) ))
