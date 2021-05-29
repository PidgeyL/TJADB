#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Singleton Class
#  Ensures only one object is created in memory
#
# Software is free software released under the "GNU Affero General Public License v3.0"
#
# Copyright (c) 2021  Pieter-Jan Moreels - pieter-jan@pidgey.net

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
