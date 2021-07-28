import csv
import hashlib
import os
import shutil
import sys

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

from etc.Settings      import Settings
from lib.DatabaseLayer import DatabaseLayer
from lib.Objects       import Genre, Song
from lib.TJA           import read_tja, parse_tja, set_tja_metadata, generate_md5s

def make_abs(path):
    if not os.path.isabs(path):
        return os.path.normpath(os.path.abspath(path))
    return os.path.normpath(path)

filedb = make_abs(Settings.file_db)
db     = DatabaseLayer()

print("[+] Writing to: %s"%filedb)

header = ['title_orig', 'title_eng', 'subtitle_orig', 'subtitle_eng',
          'artist_orig', 'artist_eng', 'charter', 'bpm', 'vetted', 'd_kantan',
          'd_futsuu', 'd_muzukashii', 'd_oni', 'd_ura', 'source_orig',
          'source_eng', 'genre', 'comments', 'video_link', 'path', 'songpath',
          'added', 'updated']


def find_song(path):
    if os.path.isfile(path[:-3]+"ogg"):
        return path[:-3]+"ogg"
    path  = os.path.dirname(path)
    for f in next(os.walk(path), (None, None, []))[2]:
        if f[-4:] == ".ogg":
            return os.path.join(path, f)


def add_row_to_db(l):
    def _int(s):
        if s == '':
            return None
        return int(s)

    genre   = db.genres.get_by_genre(l['genre'])
    charter = db.charters.get_by_name(l['charter'])
    path    = '<Not Set>'
    if genre == None:
        raise Exception("Unknown Genre")
    if charter == None:
        raise Exception("Unknown Charter")

    s = Song(None, l['title_orig'], l['title_eng'], l['subtitle_orig'],
             l['subtitle_eng'], l['artist_orig'], l['artist_eng'],
             l['source_orig'], l['source_eng'], float(l['bpm']), genre, charter,
             _int(l['d_kantan']), _int(l['d_futsuu']), _int(l['d_muzukashii']),
             _int(l['d_oni']), _int(l['d_ura']), bool(l['vetted']), l['comments'],
             l['video_link'], path, None, None, l['added'], l['updated'])
    try:
        s.md5_orig, s.md5_eng = generate_md5s(read_tja(l['path']), s)
    except Exception as e:
        raise Exception("Could not read the TJA")

    s._id  = db.songs.add(s)
    s.path = db.songs.generate_path(s)
    db.songs.update(s)

    tja = read_tja(l['path'])

    db.tjas.store_tja(s, tja, find_song(l['path']))


def read_from_csv(path):
    data = list(csv.DictReader(open(path, 'r')))
    if len(data) == 0:
        sys.exit('No data')
    # Assert all keys are present
    for key in header:
        assert key in data[0].keys()
    print("[+] Songlist keys OK")

    for i, l in enumerate(data):
        try:
            add_row_to_db(l)
        except Exception as e:
            print("Could not add song from row %s"%str(i+2))
            print(e)

if __name__ == '__main__':
    import argparse
    argParser = argparse.ArgumentParser(description="Import the songlist.csv to the database")
    argParser.add_argument('songfile', help='songlist csv')

    args = argParser.parse_args()

    read_from_csv(args.songfile)
