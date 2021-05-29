import os
import sqlite3
import sys

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

from lib.Singleton import Singleton


class Database(metaclass=Singleton):
    def __init__(self):
        path = os.path.join(run_path, '..', 'db', 'database.db')
        path = "/tmp/test.db" # TEMPORARY VALUE
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(path)
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
            db = self._ensure_database()
            result = funct(self, db, *args, **kwargs)
            db.close()
            return result
        return wrapper


    @_db_wrapped
    def add_song(self, db, title_o, title_e, sub_o, sub_e, artist_o, artist_e,
                 source_o, source_e, bpm, genre_id, charter_id, kantan, futsuu,
                 muzukashii, oni, ura, vetted, comments, video, path, md5):
        s = """INSERT INTO Songs(
                 Title_Orig, Title_Eng, Subtitle_Orig, Subtitle_Eng, Artist_Orig,
                 Artist_Eng, Source_Orig, Source_Eng, BPM, Genre_ID, Charter_ID,
                 D_Kantan, D_Futsuu, D_Muzukashii, D_Oni, D_Ura, Vetted,
                 Comments, Video_Link, Path, MD5)
               VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        v = (title_o, title_e, sub_o, sub_e, artist_o, artist_e, source_o,
             source_e, bpm, genre_id, charter_id, kantan, futsuu,
             muzukashii, oni, ura, vetted, comments, video, path, md5)
        db.execute(s, v)
        db.commit()


    @_db_wrapped
    def add_genre(self, db, title_jp, title_eng, genre):
        s = """INSERT INTO Genre(Title_JP, Title_EN, Genre) VALUES(?, ?, ?)"""
        db.execute(s, (title_jp, title_eng, genre))


    @_db_wrapped
    def get_all_songs(self, db):
        s = """SELECT s.* g.FROM Songs as s
               INNER JOIN Genre  as g ON s.Genre_ID=g.ID
               INNER JOIN Mapper as m on s.Mapper_ID=m.ID"""
        cur = db.cursor()
        data  = list(cur.execute("SELECT * FROM Songs"))
        names = list(map(lambda x: x[0], cur.description))
        return dict(zip(names, data))
