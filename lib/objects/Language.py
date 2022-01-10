#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Database-ready "Language" object
#
# Software is free software released under the "GNU Affero General Public License v3.0"
#
# Copyright (c) 2021-2022  PidgeyL

from lib.objects.helpers import multi_assert, Object

class Language(Object):
    def __init__(self, id=None, name_orig=None, name_en=None):
        self._id       = id
        self.name_orig = name_orig
        self.name_en   = name_en


    def verify(self):
        multi_assert(self._id,                      types=( int, type(None) ))
        multi_assert(self.name_orig, self.name_en,  types=( str ))
