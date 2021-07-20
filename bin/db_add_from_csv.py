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
from lib.TJA           import read_tja, parse_tja, set_tja_metadata

def make_abs(path):
    if not os.path.isabs(path):
        #return os.path.normpath(os.path.join(run_path, '..', path))
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


def clean_path(path):
    for c in  "%:/,.\\[]<>*?":
        path = path.replace(c, '_')
    return path


def find_song(path):
    if os.path.isfile(path[:-3]+"ogg"):
        return path[:-3]+"ogg"
    path  = os.path.dirname(path)
    for f in next(os.walk(path), (None, None, []))[2]:
        if f[-4:] == ".ogg":
            return os.path.join(path, f)


def store_tja(path, song):
    '''Ensures the TJA is stored with the original file name, subtitle and song'''
    try:
        tja = read_tja(path)
        tja = set_tja_metadata(tja, title=song.title_orig, sub=song.subtitle_orig,
                               song=clean_path(song.title_orig))

        if not os.path.exists(os.path.dirname(song.path)):
            os.makedirs(os.path.dirname(song.path))
        open(song.path, 'w').write(tja)
        shutil.move(find_song(path), song.path[:-3]+"ogg")

    except Exception as e:
        print("Could not prepare tja file: %s"%path)
        sys.exit(e)


def get_md5(file):
    try:
        data = open(file, 'rb').read()
        return hashlib.md5(data).hexdigest()
    except Exception as e:
        raise Exception("Could not open file %s"%file)


def add_row_to_db(l):
    def _int(s):
        if s == '':
            return None
        return int(s)

    genre   = db.genres.get_by_genre(l['genre'])
    charter = db.charters.get_by_name(l['charter'])
    md5     = get_md5(make_abs(l['path']))
    path    = '<Not Set>'
    if genre == None:
        raise Exception("Unknown Genre")
    if charter == None:
        raise Exception("Unknown Charter")

    s = Song(None, l['title_orig'], l['title_eng'], l['subtitle_orig'],
             l['subtitle_eng'], l['artist_orig'], l['artist_eng'],
             l['source_orig'], l['source_eng'], int(l['bpm']), genre, charter,
             _int(l['d_kantan']), _int(l['d_futsuu']), _int(l['d_muzukashii']),
             _int(l['d_oni']), _int(l['d_ura']), bool(l['vetted']), l['comments'],
             l['video_link'], path, md5, l['added'], l['updated'])
    s._id  = db.songs.add(s)
    s.path = db.songs.generate_path(s)
    db.songs.update(s)
    store_tja(make_abs(l['path']), s)


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
