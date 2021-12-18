import os
import redis
import sys

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

from lib.Singleton import Singleton
from lib.Config    import Configuration as conf
from etc.Settings  import Settings

class CacheDB(metaclass=Singleton):
    def __init__(self):
        pass


def bulk_hset(db, data):
    with db.pipeline() as pipe:
        for key, val in data.items():
            pipe.hmset(key, val)
        pipe.execute()
    db.bgsave()



class Songs():
    def __init__(self):
        self.db = conf.redis_song_db


    def cache_all(self, songs):
        bulk_hset(self.db, songs)


    def get(self, id):
        return self.db.hget(id)
