import functools
import os
import sys

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

import lib.SQLiteDB as Database
from lib.Objects            import Song, Genre, Charter
from lib.ObjectVerification import verify_song, verify_genre, verify_charter
from lib.Singleton          import Singleton
from etc.Settings           import Settings

conf = Settings()

class DatabaseLayer(metaclass=Singleton):
    def __init__(self):
        self.songs    = Songs()
        self.genres   = Genres()
        self.charters = Charters()


class Songs():
    def __init__(self):
        self.db = Database.Database()


    def add(self, song):
        if not verify_song(song):
            sys.exit("Could not verify object!")
        vars = (song.title_orig, song.title_eng, song.subtitle_orig,
                song.subtitle_eng, song.artist_orig, song.artist_eng,
                song.source_orig, song.source_eng, song.bpm, song.genre._id,
                song.charter._id, song.d_kantan, song.d_futsuu,
                song.d_muzukashii, song.d_oni, song.d_ura, song.vetted,
                song.comments, song.video_link, song.path, song.md5, song.added,
                song.updated)
        return self.db.add_song(*vars)


    def update(self, song):
        if not verify_song(song):
            sys.exit("Could not verify object!")
        if not song._id:
            raise Exception("Song has no ID")

        vars = (song._id, song.title_orig, song.title_eng, song.subtitle_orig,
                song.subtitle_eng, song.artist_orig, song.artist_eng,
                song.source_orig, song.source_eng, song.bpm, song.genre._id,
                song.charter._id, song.d_kantan, song.d_futsuu,
                song.d_muzukashii, song.d_oni, song.d_ura, song.vetted,
                song.comments, song.video_link, song.path, song.md5, song.added,
                song.updated)
        return self.db.update_song(*vars)


    def get_all(self):
        data = []
        for s in self.db.get_all_songs():
            g = DatabaseLayer().genres.get_by_id(s['Genre_ID'])
            c = DatabaseLayer().charters.get_by_id(s['Charter_ID'])
            x = Song(s['ID'], s['Title_Orig'], s['Title_Eng'], s['Subtitle_Orig'],
                     s['Subtitle_Eng'], s['Artist_Orig'], s['Artist_Eng'],
                     s['Source_Orig'], s['Source_Eng'], s['BPM'], g, c,
                     s['D_Kantan'], s['D_Futsuu'], s['D_Muzukashii'],
                     s['D_Oni'], s['D_Ura'], bool(s['Vetted']), s['Comments'],
                     s['Video_Link'], s['Path'], s['MD5'], s['Added'], s['Updated'])
            data.append(x)
        return data


    def generate_path(self, song):
        def _clean(s):
            for c in " %:/,.\\[]<>*?":
                s = s.replace(c, '_')
            return s

        if not song._id:
            raise Execption("No ID set")
        if not song.title_orig:
            raise Exception("No title set")

        path = conf.file_db
        if not os.path.isabs(path):
            path = os.path.join(run_path, '..', path)
        path = os.path.join(path, str(song._id), _clean(song.title_orig)) + ".tja"
        return os.path.normpath(path)


class Genres():
    def __init__(self):
        self.db = Database.Database()


    def add(self, genre):
        if not verify_genre(genre):
            sys.exit("Could not verify object!")
        return self.db.add_genre(genre.name_jp, genre.name_eng, genre.genre)


    @functools.cache
    def get_by_id(self, id):
        g = self.db.get_genre_by_id(id)
        if len(g) == 0:
            return None
        g = g[0]
        return Genre(g['ID'], g['Title_JP'], g['Title_EN'], g['Genre'])


    @functools.cache
    def get_by_genre(self, genre):
        g = self.db.get_genre_by_genre(genre)
        if len(g) == 0:
            return None
        g = g[0]
        return Genre(g['ID'], g['Title_JP'], g['Title_EN'], g['Genre'])


class Charters():
    def __init__(self):
        self.db = Database.Database()


    def add(self, charter):
        if not verify_charter(charter):
            sys.exit("Could not verify object!")
        return self.db.add_charter(charter.name, charter.image, charter.about,
                                   charter.staff )


    @functools.cache
    def get_by_id(self, id):
        g = self.db.get_charter_by_id(id)
        if len(g) == 0:
            return None
        g = g[0]
        return Charter(g['ID'], g['Name'], g['Image'], g['About'], bool(g['Staff']))


    @functools.cache
    def get_by_name(self, name):
        g = self.db.get_charter_by_name(name)
        if len(g) == 0:
            return None
        g = g[0]
        return Charter(g['ID'], g['Name'], g['Image'], g['About'], bool(g['Staff']))

