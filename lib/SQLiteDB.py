import os
import sqlite3
import sys

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

from lib.Singleton import Singleton
from etc.Settings  import Settings


class Database(metaclass=Singleton):
    def __init__(self):
        path = Settings().sqlite_db
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        self.struct = os.path.join(run_path, "sqlite_struct.sql")
        self.path   = path


    def _ensure_database(self):
        try:
            db = sqlite3.connect(self.path)
            for line in open(self.struct, 'r').read().split(';'):
                db.execute(line+';')
            return db
        except Exception as e:
            sys.exit("Could not verify database structure: %s"%e)


    def _db_wrapped(funct):
        def wrapper(self, *args, **kwargs):
            db  = self._ensure_database()
            cur = db.cursor()
            result = funct(self, db, cur, *args, **kwargs)
            db.close()
            return result
        return wrapper


    ###############
    # Adding data #
    ###############
    @_db_wrapped
    def add_song(self, db, cur, title_o, title_e, sub_o, sub_e, artist_o, artist_e,
                 source_o, source_e, bpm, genre_id, charter_id, kantan, futsuu,
                 muzukashii, oni, ura, vetted, comments, video, path, md5_orig,
                 md5_eng, added, updated):
        s = """INSERT INTO Songs(
                 Title_Orig, Title_Eng, Subtitle_Orig, Subtitle_Eng, Artist_Orig,
                 Artist_Eng, Source_Orig, Source_Eng, BPM, Genre_ID, Charter_ID,
                 D_Kantan, D_Futsuu, D_Muzukashii, D_Oni, D_Ura, Vetted,
                 Comments, Video_Link, Path, MD5_Orig, MD5_Eng, Added, Updated)
               VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                      ?, ?, ?, ?)"""
        v = (title_o, title_e, sub_o, sub_e, artist_o, artist_e, source_o,
             source_e, bpm, genre_id, charter_id, kantan, futsuu, muzukashii, oni,
             ura, vetted, comments, video, path, md5_orig, md5_eng, added, updated)
        cur.execute(s, v)
        db.commit()
        return cur.lastrowid


    @_db_wrapped
    def add_genre(self, db, cur, title_jp, title_eng, genre):
        s = "INSERT INTO Genres(Title_JP, Title_EN, Genre) VALUES(?, ?, ?)"
        cur.execute(s, (title_jp, title_eng, genre))
        db.commit()
        return cur.lastrowid


    @_db_wrapped
    def add_charter(self, db, cur, name, image, about, staff):
        s = "INSERT INTO Charters(Name, Image, About, Staff) VALUES(?, ?, ?, ?)"
        cur.execute(s, (name, image, about, staff))
        db.commit()
        return cur.lastrowid


    ################
    # reading data #
    ################
    @_db_wrapped
    def _get_all(self, db, cur, table):
        data  = list(cur.execute("SELECT * FROM %s"%table))
        names = list(map(lambda x: x[0], cur.description))
        return [dict(zip(names, d)) for d in data]


    @_db_wrapped
    def _get_by_field(self, db, cur, table, field, value):
        data  = list(cur.execute("SELECT * FROM %s WHERE %s=?"%(table, field),
                    (value,)))
        names = list(map(lambda x: x[0], cur.description))
        return [dict(zip(names, d)) for d in data]


    def get_genre_by_id(self, id):
        return self._get_by_field('Genres', 'ID', id)


    def get_genre_by_genre(self, genre):
        return self._get_by_field('Genres', 'Genre', genre)


    def get_all_genres(self):
        return self._get_all('Genres')


    def get_charter_by_id(self, id):
        return self._get_by_field('Charters', 'ID', id)


    def get_charter_by_name(self, name):
        return self._get_by_field('Charters', 'Name', name)


    def get_all_charters(self):
        return self._get_all('Charters')


    def get_all_songs(self):
        return self._get_all('Songs')


    def get_song_by_id(self, id):
        return self._get_by_field('Songs', 'ID', id)


    @_db_wrapped
    def update_song(self, db, cur, id, title_o, title_e, sub_o, sub_e, artist_o,
                 artist_e, source_o, source_e, bpm, genre_id, charter_id, kantan,
                 futsuu, muzukashii, oni, ura, vetted, comments, video, path,
                 md5_orig, md5_eng, added, updated):

        s = """UPDATE Songs SET
                   Title_Orig = ?,     Title_Eng = ?,
                   Subtitle_Orig = ?,  Subtitle_Eng = ?,
                   Artist_Orig = ?,    Artist_Eng = ?,
                   Source_Orig = ?,    Source_Eng = ?,
                   BPM = ?, Genre_ID = ?, Charter_ID = ?, D_Kantan = ?,
                   D_Futsuu = ?, D_Muzukashii = ?, D_Oni = ?, D_Ura = ?,
                   Vetted = ?, Comments = ?, Video_Link = ?, Path = ?,
                   MD5_Orig = ?, MD5_Eng = ?, Added = ?, Updated = ?
               WHERE
                   ID = ?;"""
        v = (title_o, title_e, sub_o, sub_e, artist_o, artist_e, source_o,
             source_e, bpm, genre_id, charter_id, kantan, futsuu, muzukashii,
             oni, ura, vetted, comments, video, path, md5_orig, md5_eng, added,
             updated, id)
        cur.execute(s, v)
        db.commit()
        return cur.lastrowid

