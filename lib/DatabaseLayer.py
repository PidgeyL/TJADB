import functools
import json
import os
import pydoc
import random
import shutil
import sys

from datetime  import date
from threading import Thread
run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

#import lib.SQLiteDB as Database
import lib.PSQLDB as Database

from lib.Config     import Configuration
from lib.Singleton  import Singleton
from etc.Settings   import Settings
from lib.TJA        import prepare_orig_tja, generate_md5s

cdb  = Configuration().cache_db

class DatabaseLayer(metaclass=Singleton):
    def __init__(self):
        self.users        = Users()
        self.artists      = Artists()
        self.songs        = Songs()
        self.genres       = Genres()
        self.sources      = Sources()
        self.song_states  = SongStates()
        self.languages    = Languages()
        self.difficulties = Difficulties()
        self.bot          = Bot(self)
        self.settings     = Settings()
        self.cache        = cdb

        # Fill cache in separate thread, to avoid recursion due to imports in the
        # objects. When the __init__ does not finish, the obj does not exist in the
        # Singleton.
        Thread(target = self.fill_cache).start()

    def fill_cache(self):
        # TODO: save downloads once implemented
        cdb.clear_collection('song')
        self.songs.get_all()


############
# Wrappers #
############
def cacheid(cname):
    def wrapper(funct):
        @functools.wraps(funct)
        def inner(self, cid):
            cache = cdb.get_id(cname, cid, self.obj)
            if cache:
                return cache
            result = funct(self, cid)
            result = self.obj(**result) if result else None
            if cname and not cache and result:
                cdb.set_id(cname, cid, result)
            return result
        return inner
    return wrapper


def cacheall(cname):
    def wrapper(funct):
        @functools.wraps(funct)
        def inner(self):
            cache = cdb.get_all(cname, self.obj)
            if cache:
                return cache
            result = funct(self)
            result = [self.obj(**item) for item in result]
            if cname and not cache and result:
                cdb.multi_set_id(cname, result)
            return result
        return inner
    return wrapper


###############
# Collections #
###############
class Artists():
    def __init__(self):
        from lib.objects import Artist
        self.db  = Database.Database()
        self.obj = Artist

    def add(self, artist):
        artist.verify()
        return self.db.add_artist(**artist.as_dict())

    @cacheid(cname="artist")
    def get_by_id(self, id):
        return  self.db.get_artist_by_id(id)

    def get_all(self):
        return [self.obj(**x) for x in self.db.get_all_artists()]


class Genres():
    def __init__(self):
        from lib.objects import Genre
        self.db  = Database.Database()
        self.obj = Genre

    def add(self, genre):
        artist.verify()
        return self.db.add_genre(**(genre.as_dict()))

    @cacheid(cname="genre")
    def get_by_id(self, id):
        return self.db.get_genre_by_id(id)

    def get_all(self):
        return [self.obj(**x) for x in self.db.get_all_genres()]



class Sources():
    def __init__(self):
        from lib.objects import Source
        self.db  = Database.Database()
        self.obj = Source

    def add(self, source):
        source.verify()
        return self.db.add_source(**(source.as_dict()))

    @cacheid(cname="source")
    def get_by_id(self, id):
        return self.db.get_source_by_id(id)

    def get_all(self):
        return [self.obj(**x) for x in self.db.get_all_sources()]


class SongStates():
    def __init__(self):
        from lib.objects import SongState
        self.db  = Database.Database()
        self.obj = SongState

    @cacheid(cname="songstate")
    def get_by_id(self, id):
        return self.db.get_song_state_by_id(id)

    def get_all(self):
        return [self.obj(**x) for x in self.db.get_all_song_states()]



class Songs():
    def __init__(self):
        from lib.objects import Song, Artist
        self.db  = Database.Database()
        self.obj = Song
        self.artist_obj = Artist

    def add(self, song, tja=None, ogg=None, bg=None):
        song.verify()
        if not all([tja, ogg]):
            print("TJA or OGG missing")
            return False
        song=self.write_tja(song, tja, ogg)
        song=self.write_ogg(song, ogg)
        if bg:   song=self.write_bg_video_picture(song, bg)
        as_dict = song.as_dict()
        artists = as_dict.pop('artists')
        song_id = self.db.add_song(**as_dict)
        # Link artists
        for artist in artists:
            self.db.add_artist_to_song(song_id, artist['id'])
        return song_id

    def _enrich(self, song):
        if isinstance(song, self.obj):
            artists = self.db.get_artists_for_song_id(song.id)
            song.artists = [self.artist_obj(**a) for a in artists]
        else:
            artists = self.db.get_artists_for_song_id(song['id'])
            song['artists'] = [a['id'] for a in artists]
        return song

    @cacheid(cname="song")
    def get_by_id(self, id):
        song = self.db.get_song_by_id(id)
        return self._enrich(song)

    def get_by_artist_id(self, id):
        if isinstance(id, self.artist_obj):
            id = id.id
        songs = [self.obj(**x) for x in self.db.get_song_by_artist_id(id)]
        return [self._enrich(s) for s in songs]

    def get_by_source_id(self, id):
        if isinstance(id, self.artist_obj):
            id = id.id
        songs = [self.obj(**x) for x in self.db.get_song_by_source_id(id)]
        return [self._enrich(s) for s in songs]

    @cacheall(cname="song")
    def get_all(self):
        return [self._enrich(s) for s in self.db.get_all_songs()]

    def read_tja(self, song):
        if song.obj_tja:
            return self.db.get_obj(song.obj_tja)
        return None

    def read_wave(self, song):
        if song.obj_ogg:
            return self.db.get_obj(song.obj_ogg)
        return None

    def read_bg_video_picture(self, song):
        if song.obj_bg_video_picture:
            return self.db.get_obj(song.obj_bg_video_picture)
        return None

    def write_tja(self, song, data, wave):
        if song.obj_tja:
            self.db.delete_obj(song.obj_tja)
        data = prepare_orig_tja(data, song, wave)
        md5o, md5e = generate_md5s(data, song, wave)
        song.obj_tja      = self.db.add_obj(data)
        song.tja_orig_md5 = md5o
        song.tja_en_md5   = md5e
        return song

    def write_ogg(self, song, data):
        if song.obj_ogg:
            self.db.delete_obj(song.obj_ogg)
        song.obj_ogg = self.db.add_obj(data)
        return song

    def write_bg_video_picture(self, song, data):
        if song.obj_bg_video_picture:
            self.db.delete_obj(song.obj_bg_video_picture)
        song.obj_bg_video_picture = self.db.add_obj(data)
        return song

    def get_sotd(self):
        td   = date.today()
        sotd = self.db.get_song_of_the_day(td)
        if not sotd:
            sotd = random.choice( cdb.get_all_keys('song') )
            sotd = self.get_by_id(sotd)
            self.db.set_song_of_the_day(sotd.id)
            return sotd
        return self.obj(**sotd)


class Users():
    def __init__(self):
        from lib.objects import User
        self.db  = Database.Database()
        self.obj = User

    def add(self, user):
        user.verify()
        return self.db.add_user(**(user.as_dict()))

    @cacheid(cname="user")
    def get_by_id(self, id):
        return self.db.get_user_by_id(id)

    @cacheid(cname="user_cn")
    def get_by_charter_name(self, name):
        user = self.db.get_user_by_charter_name(name)
        return user[0] if user else None

    @cacheid(cname="user_did")
    def get_by_discord_id(self, id):
        user = self.db.get_user_by_discord_id(id)
        return user[0] if user else None

    def get_all(self):
        return [self.obj(**x) for x in self.db.get_all_users()]



class Difficulties():
    def __init__(self):
        from lib.objects import Difficulty
        self.db  = Database.Database()
        self.obj = Difficulty

    @cacheid(cname="diff")
    def get_by_id(self, id):
        return self.db.get_difficulty_by_id(id)

    def get_all(self):
        return [self.obj(**x) for x in self.db.get_all_difficulties()]



class Languages():
    def __init__(self):
        from lib.objects import Language
        self.db  = Database.Database()
        self.obj = Language

    @cacheid(cname="lang")
    def get_by_id(self, id):
        return self.db.get_language_by_id(id)

    def get_all(self):
        return [self.obj(**x) for x in self.db.get_all_languages()]


class Bot():
    def __init__(self, dbl):
        self.db  = Database.Database()
        self.dbl = dbl

    def get_sotd_channels(self):
        chans = self.dbl.settings.read('sotd_channels')
        return chans or []

    def add_sotd_channel(self, channel):
        self.dbl.settings.append('sotd_channels', channel)


class Settings():
    def __init__(self):
        self.db  = Database.Database()

    def save(self, name, value):
        _type = type(value).__name__
        value = json.dumps(value)
        self.db.save_setting(name, _type, value)

    def read(self, name):
        setting = self.db.get_setting(name)
        if not setting:
            return None
        return setting['value']

    def append(self, name, value):
        setting = self.read(name)
        if not setting:
            self.save(name, [value])
        else:
            if not isinstance(setting, list):
                return False
            self.db.add_to_list_setting(name, value)
            return True

    def remove(self, name, value):
        setting = self.read(name)
        if not setting:
            return
        if not isinstance(setting, list):
            return False
        # PSQL only is able to remove str from arrays, hence:
        if value in setting:
            setting.remove(value)
            self.save(name, setting)
        return True
