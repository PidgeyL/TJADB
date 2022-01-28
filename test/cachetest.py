import os
import random
import sys

from time import perf_counter, sleep

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

import lib.CacheRedis
import lib.CachePy
from lib.DatabaseLayer import DatabaseLayer
from lib.objects import Song

_ROUNDS_ = 10
_TESTS_ = ['cache_clear', 'cache_all_songs', 'get_all_songs', 'get_one_song']
_DBS_   = {'redis': lib.CacheRedis.CacheDB(),
           'pycache': lib.CachePy.CacheDB()}
results = {cdb: {t: [] for t in _TESTS_} for cdb in _DBS_.keys()}
sizes   = {}

# Helper functions
def timeit(funct, *args, **kwargs):
    start = perf_counter()
    result = funct(*args, **kwargs)
    end = perf_counter()
    return (end - start)

def mili(t):
    if t > 1:
        return f"{int(t*1000)/1000} s"
    else:
        return f"{int(t*10000)/10} ms"

# Get songs
db    = DatabaseLayer()
songs = db.songs.get_all()
print(f"[i] Working with {len(songs)} songs")

# Start with an empty cache
for cdb in _DBS_.values():
    cdb.clear_id_cache()

for cdbname, cdb in _DBS_.items():
    print(f"[i] testing {cdbname}")
    for i in range(_ROUNDS_):
        # cache_all_songs
        t = timeit(cdb.multi_set_id, 'song', songs)
        results[cdbname]['cache_all_songs'].append(t)
        # get_all_songs
        t = timeit(cdb.get_all, 'song', Song)
        results[cdbname]['get_all_songs'].append(t)
        # get_one_song
        rand_id = random.choice(songs).id
        t = timeit(cdb.get_id, 'song', rand_id, Song)
        results[cdbname]['get_one_song'].append(t)
        # cache_clear
        t = timeit(cdb.clear_id_cache)
        results[cdbname]['cache_clear'].append(t)
    # Get cache size
    cdb.multi_set_id('song', songs)
    sizes[cdbname] = cdb.cache_size()


for cdb, tests in results.items():
    print(f"[ {cdb} ]")
    for test, results in tests.items():
        print(f" |- {test} ({_ROUNDS_} rounds)")
        if len(results) == 0:
            print(" |    |- No results\n |")
        else:
            print(f" |    |- max: {mili(max(results))}", end = " - ")
            print(f"min: {mili(min(results))}", end = " - ")
            print(f"avg: {mili(sum(results)/len(results))}")
            print(" |")
    print(f' |- Cache size: {sizes[cdb]}KB')
    print()
