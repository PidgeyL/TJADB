#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Database-ready "Difficulty" object
#
# Software is free software released under the "GNU Affero General Public License v3.0"
#
# Copyright (c) 2021-2022  PidgeyL

from lib.objects.helpers import multi_assert, Object

class Difficulty(Object):
    def __init__(self, id=None, name_jp=None, name_en=None):
        self._id     = id
        self.name_jp = name_jp
        self.name_en = name_en


    def verify(self):
        multi_assert(self._id,                    types=( int, type(None) ))
        multi_assert(self.name_jp, self.name_en,  types=( str ))
