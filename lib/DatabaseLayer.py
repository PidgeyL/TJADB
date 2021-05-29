import os
import sys

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

import lib.SQLiteDB as Database
from lib.Objects            import Song
from lib.ObjectVerification import verify_song, verify_genre, verify_charter
from lib.Singleton          import Singleton

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
                song.comments, song.video_link, song.path, song.md5)
        return self.db.add_song(*vars)


#    def get_all(self):
#        data = []
#        for s in self.db.get_all_songs():
#            x = Song(s['ID'], s['Title_Orig'], s['Title_Eng'], s['Subtitle_Orig'],
#                     s['Subtitle_Eng'], s['Artist_Orig'], s['Artist_Eng'],
#                     s['Source_Orig'], s['Source_Eng'], s['BPM'], genre)

class Genres():
    def __init__(self):
        self.db = Database.Database()


    def add(self, genre):
        if not verify_genre(genre):
            sys.exit("Could not verify object!")
        return self.db.add_genre(genre.name_jp, genre.name_eng, genre.genre)


class Charters():
    def __init__(self):
        self.db = Database.Database()


    def add(self, charter):
        if not verify_charter(charter):
            sys.exit("Could not verify object!")
        return self.db.add_charter(charter.name, charter.image, charter.about,
                                   charter.staff )

