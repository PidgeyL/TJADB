#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Python memory CacheDB
#  Use a variables in memory to cache search results
#
# Software is free software released under the "GNU Affero General Public License v3.0"
#
# Copyright (c) 2021-2022  PidgeyL
from collections   import defaultdict

from lib.functions import deep_getsizeof
from lib.Singleton import Singleton

###################
# Cache DB Object #
###################
class CacheDB(metaclass=Singleton):
    def __init__(self):
        self.id_db = defaultdict(dict)


    def set_id(self, cname, obj_id, obj):
        if not (isinstance(cname, str) and isinstance(obj_id, (str, int))):
            return False
        self.id_db[cname][obj_id] = obj
        return True


    def get_id(self, cname, obj_id, obj_type):
        if not (isinstance(cname, str) and isinstance(obj_id, (str, int))):
            return None
        return self.id_db[cname].get(obj_id)


    def multi_set_id(self, cname, objects):
        if not isinstance(cname, str):
            return False
        for obj in objects:
            self.set_id(cname, obj.id, obj)
        return True


    def get_all_keys(self, cname=None):
        if cname:
            return list(self.id_db[cname].keys())
        keys = [[f"{cname}_{id}" for id in col.keys()]
                  for cname, col in self.id_db.items()]
        return [item for sublist in keys for item in sublist]


    def get_all(self, cname, obj_type):
        if not isinstance(cname, str):
            return []
        return self.id_db[cname].items()


    def clear_key(self, cname, obj_id):
        if not (isinstance(cname, str) and isinstance(obj_id, (str, int))):
            return False
        self.id_db[cname].pop(obj_id, None)
        self.id_db.delete(f"{cname}_{obj_id}")
        return True


    def clear_collection(self, cname):
        if not isinstance(cname, str):
            return False
        self.id_db[cname] = {}
        return True


    def clear_id_cache(self):
        self.id_db = defaultdict(dict)
        return True


    def cache_size(self):
        # get size in bytes
        size = deep_getsizeof(self.id_db)
        # return in KB
        return int(size/1024)
