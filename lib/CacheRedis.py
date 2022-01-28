#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Redis CacheDB
#  Use a redis server to cache search results
#
# Software is free software released under the "GNU Affero General Public License v3.0"
#
# Copyright (c) 2021-2022  PidgeyL

import json

from lib.Config    import Configuration
from lib.Singleton import Singleton

####################
# Helper Functions #
####################
def redisify(value):
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, list):
        return json.dumps(value)
    return value

###################
# Cache DB Object #
###################
class CacheDB(metaclass=Singleton):
    def __init__(self):
        self.id_db = Configuration().redis_ID_db

    def _pipe_delete(self, keys):
        with self.id_db.pipeline() as pipe:
            for key in keys:
                pipe.delete(key)
            pipe.execute()


    def set_id(self, cname, obj_id, obj):
        if not (isinstance(cname, str) and isinstance(obj_id, (str, int))):
            return False
        key    = f"{cname}_{obj_id}"
        asdict = {k: redisify(v) for k, v in obj.as_dict().items() if v}
        self.id_db.hmset(key, asdict)
        return True


    def get_id(self, cname, obj_id, obj_type):
        if not (isinstance(cname, str) and isinstance(obj_id, (str, int))):
            return None
        key   = f"{cname}_{obj_id}"
        cache = self.id_db.hgetall(key)
        if cache:
            return obj_type(**cache)
        return None


    def multi_set_id(self, cname, objects):
        if not isinstance(cname, str):
            return False
        with self.id_db.pipeline() as pipe:
            for obj in objects:
                asdict = {k: redisify(v) for k, v in obj.as_dict().items() if v}
                pipe.hmset(f'{cname}_{obj.id}', asdict)
            pipe.execute()
        return True


    def get_all_keys(self, cname=None):
        if cname:
            return list(self.id_db.scan_iter(f"{cname}_*"))
        return list(self.id_db.scan_iter())


    def get_all(self, cname, obj_type):
        if not isinstance(cname, str):
            return []
        with self.id_db.pipeline() as pipe:
            for key in self.get_all_keys(cname):
                pipe.hgetall(key)
            objs = pipe.execute()
            return [obj_type(**o) for o in objs]


    def clear_key(self, cname, obj_id):
        if not (isinstance(cname, str) and isinstance(obj_id, (str, int))):
            return False
        self.id_db.delete(f"{cname}_{obj_id}")
        return True


    def clear_collection(self, cname):
        if not isinstance(cname, str):
            return False
        self._pipe_delete(self.get_all_keys(cname))
        return True


    def clear_id_cache(self):
        self._pipe_delete(self.get_all_keys())
        return True


    def cache_size(self):
        # Get size in bytes
        size = self.id_db.memory_stats()['dataset.bytes']
        # return in KB
        return int(size / 1024)
