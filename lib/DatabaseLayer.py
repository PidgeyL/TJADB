import functools
import os
import shutil
import sys

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

#import lib.SQLiteDB as Database
import lib.PSQLDB as Database

from lib.Config     import Configuration
from lib.Singleton  import Singleton
from etc.Settings   import Settings
from lib.TJA        import prepare_orig_tja, generate_md5s

cdb  = Configuration().redis_ID_db

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

        self.charters    = Charters()
        self.tjas        = TJAs()


def redisify(value):
    if isinstance(value, bool):
        return int(value)
    return value


def cacheid(cname):
    def wrapper(funct):
        @functools.wraps(funct)
        def inner(self, cid):
            if not cid:
                return None
            ckey  = f"{cname}_{cid}"
            cache = cdb.hgetall(ckey)
            if cache:
                return self.obj(**cache)
            result = funct(self, cid)
            result = self.obj(**result) if result else None
            if cname and not cache and result:
                asdict = {k: redisify(v) for k, v in result.as_dict().items() if v}
                cdb.hmset(ckey, asdict)
            return result
        return inner
    return wrapper



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
        from lib.objects import Song
        self.db  = Database.Database()
        self.obj = Song

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

    @cacheid(cname="song")
    def get_by_id(self, id):
        return self.db.get_song_by_id(id)

    def get_all(self):
        return  [self.obj(**x) for x in self.db.get_all_songs()]

    def read_tja(self, song):
        if song.obj_tja:
            return self.db.get_obj(song.obj_tja)
        return None

    def read_ogg(self, song):
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



#########
# To Do #
#########


class Charters():
    def __init__(self):
        self.db = Database.Database()


    def add(self, charter):
        if not verify_charter(charter):
            sys.exit("Could not verify object!")
        return self.db.add_charter(charter.name, charter.image, charter.about,
                                   charter.staff )


    @functools.lru_cache(maxsize=None)
    def get_by_id(self, id):
        c = self.db.get_charter_by_id(id)
        if len(c) == 0:
            return None
        c = c[0]
        return Charter(c['ID'], c['Name'], c['Image'], c['About'], bool(c['Staff']))


    @functools.lru_cache(maxsize=None)
    def get_by_name(self, name):
        c = self.db.get_charter_by_name(name)
        if len(c) == 0:
            return None
        c = c[0]
        return Charter(c['ID'], c['Name'], c['Image'], c['About'], bool(c['Staff']))


    def get_all(self):
        data = []
        for c in self.db.get_all_charters():
            x = Charter(c['ID'], c['Name'], c['Image'], c['About'], bool(c['Staff']))
            data.append(x)
        return data


class TJAs():

    def get_info(self, song):
        def _score(i):
            if i == None:
                return '*'
            return str(i)
        def _alt(orig, alt):
            if orig != alt:
                return " (%s)\n"%alt
            return '\n'
        def _difficulty(song):
            scores = [song.d_kantan, song.d_futsuu, song.d_muzukashii, song.d_oni, song.d_ura]
            return '/'.join([_score(i) for i in scores])

        text =  "Title: " + song.title_orig + _alt(song.title_orig, song.title_eng)
        text += "Artist: " + song.artist_orig + _alt(song.artist_orig, song.artist_eng)
        text += "From: " + song.source_orig + _alt(song.source_orig, song.source_eng)
        text += "Charter: " + song.charter.name + "\n"
        text += "Difficulty: " + _difficulty(song) + "\n"
        text += "Genre: %s (%s)\n"%(song.genre.name_jp, song.genre.name_eng)
        text += "BPM: %s\n"%song.bpm
        text += "Last update: %s\n\n"%song.updated
        return text
