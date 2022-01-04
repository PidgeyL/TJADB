#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Database object helper functions
#
# Software is free software releasedunder the "GNU Affero General Public License v3.0"
#
# Copyright (c) 2021-2022  PidgeyL
from copy import copy

def multi_assert(*args, types):
    try:
        for arg in args:
            assert(isinstance(arg, types))
    except Exception:
        raise ObjectException


class ObjectException(Exception):
    pass


class Object:
    def __init__(self):
        pass

    def verify(self):
        raise ObjectException

    def as_dict(self):
        d = copy(vars(self))
        d['id'] = self._id
        del d['_id']
        return d

    @property
    def id(self):
        return int(self._id) if self._id else None

    @id.setter
    def id(self, i):
        self._id = int(i)
