import functools
import os
import shutil
import sys

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

import lib.SQLiteDB as Database
from lib.Objects            import Song, Genre, Charter
from lib.ObjectVerification import verify_song, verify_genre, verify_charter
from lib.Singleton          import Singleton
from etc.Settings           import Settings
from lib.TJA                import read_tja, parse_tja, set_tja_metadata, clean_path, write_tja

conf = Settings()



class DatabaseLayer(metaclass=Singleton):
    def __init__(self):
        self.songs    = Songs()
        self.genres   = Genres()
        self.charters = Charters()
        self.tjas     = TJAs()


class Songs():
    def __init__(self):
        self.db = Database.Database()


    def add(self, song):
        if not verify_song(song):
            sys.exit("Could not verify object!")
        if song.updated in (None, ''):  song.updated = song.added
        vars = (song.title_orig, song.title_eng, song.subtitle_orig,
                song.subtitle_eng, song.artist_orig, song.artist_eng,
                song.source_orig, song.source_eng, song.bpm, song.genre._id,
                song.charter._id, song.d_kantan, song.d_futsuu,
                song.d_muzukashii, song.d_oni, song.d_ura, song.vetted,
                song.comments, song.video_link, song.path, song.md5_orig,
                song.md5_eng, song.added, song.updated)
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
                song.comments, song.video_link, song.path, song.md5_orig,
                song.md5_eng, song.added, song.updated)
        return self.db.update_song(*vars)


    def get_by_id(self, id):
        song = self.db.get_song_by_id(id)
        if len(song) == 0:
            return None
        s = song[0]
        g = DatabaseLayer().genres.get_by_id(s['Genre_ID'])
        c = DatabaseLayer().charters.get_by_id(s['Charter_ID'])
        return Song(s['ID'], s['Title_Orig'], s['Title_Eng'], s['Subtitle_Orig'],
                    s['Subtitle_Eng'], s['Artist_Orig'], s['Artist_Eng'],
                    s['Source_Orig'], s['Source_Eng'], s['BPM'], g, c,
                    s['D_Kantan'], s['D_Futsuu'], s['D_Muzukashii'],
                    s['D_Oni'], s['D_Ura'], bool(s['Vetted']), s['Comments'],
                    s['Video_Link'], s['Path'], s['MD5_Orig'], s['MD5_Eng'],
                    s['Added'], s['Updated'])


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
                     s['Video_Link'], s['Path'], s['MD5_Orig'], s['MD5_Eng'],
                     s['Added'], s['Updated'])
            data.append(x)
        return data


    def generate_path(self, song):
        if not song._id:
            raise Execption("No ID set")
        if not song.title_orig:
            raise Exception("No title set")

        path = conf.file_db
        if not os.path.isabs(path):
            path = os.path.join(run_path, '..', path)
        path = os.path.join(path, str(song._id),
                            clean_path(song.title_orig)) + ".tja"
        return os.path.normpath(path)


class Genres():
    def __init__(self):
        self.db = Database.Database()


    def add(self, genre):
        if not verify_genre(genre):
            sys.exit("Could not verify object!")
        return self.db.add_genre(genre.name_jp, genre.name_eng, genre.genre)


    @functools.lru_cache(maxsize=None)
    def get_by_id(self, id):
        g = self.db.get_genre_by_id(id)
        if len(g) == 0:
            return None
        g = g[0]
        return Genre(g['ID'], g['Title_JP'], g['Title_EN'], g['Genre'])


    @functools.lru_cache(maxsize=None)
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


    @functools.lru_cache(maxsize=None)
    def get_by_id(self, id):
        g = self.db.get_charter_by_id(id)
        if len(g) == 0:
            return None
        g = g[0]
        return Charter(g['ID'], g['Name'], g['Image'], g['About'], bool(g['Staff']))


    @functools.lru_cache(maxsize=None)
    def get_by_name(self, name):
        g = self.db.get_charter_by_name(name)
        if len(g) == 0:
            return None
        g = g[0]
        return Charter(g['ID'], g['Name'], g['Image'], g['About'], bool(g['Staff']))


class TJAs():
    def store_tja(self, song, tja, song_path):
        path = DatabaseLayer().songs.generate_path(song)[:-4]+'.ogg'
        tja = set_tja_metadata(tja, title=song.title_orig, sub=song.subtitle_orig,
                                    song=clean_path(song.title_orig)+'.ogg')
        if not os.path.exists(os.path.dirname(song.path)):
            os.makedirs(os.path.dirname(song.path))
        write_tja(tja, song.path)
        shutil.move(song_path, path)


    def get_tja(self, song):
        return open(song.path, "rb").read()


    def get_ogg(self, song):
        return open(song.path[:-3]+"ogg", "rb").read()


    def get_mov(self, song):
        meta = parse_tja(self.get_tja(song))
        if meta['movie'] in [None, '', False]:
            return None
        path = os.path.join(os.path.dirname(song.path), meta['movie'])
        return open(path, "rb").read()


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
