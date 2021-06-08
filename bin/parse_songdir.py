import base64
import copy
import csv
import os
import sys
import zipfile

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

from lib.TJA import read_tja, decode_tja, parse_tja

def read_tja_zip(file):
    tjas = []
    if not zipfile.is_zipfile(file):
        return []
    zip = zipfile.ZipFile(file)
    for c_file in zip.filelist:
        if c_file.filename.endswith('.tja'):
            data = decode_tja( zip.read(c_file) )
            tjas.append( (file + "#" + c_file.filename, data) )
    return tjas


def read_dir(dir):
    tjas = [] #(path, data)
    for path, dirs, files in os.walk(dir):
        for file in files:
            file = os.path.join(path, file)
            if file.endswith('.tja'):
                tjas.append( (file, read_tja(file)) )
            elif file.endswith('.zip'):
                tjas.extend( read_tja_zip(file) )
    return tjas


def create_csv(dir):
    data = [('title_orig', 'title_eng', 'subtitle_orig', 'subtitle_eng',
             'artist_orig', 'artist_eng', 'charter', 'bpm', 'vetted', 'd_kantan',
             'd_futsuu', 'd_muzukashii', 'd_oni', 'd_ura', 'source_orig',
             'source_eng', 'genre', 'comments', 'video_link', 'path', 'songpath',
             'added', 'updated')]
    for tja in read_dir(dir):
        d = parse_tja(tja[1])
        data.append( (d['title'], '', d['sub'], '', '', '', '', d['bpm'], 'no',
                      d['easy'], d['normal'], d['hard'], d['oni'], d['ura'], '',
                      '', d['genre'], '', '', tja[0], d['song'], '', '') )

    with open('songlist.csv', mode='w', encoding="utf-8") as _f:
        writer = csv.writer(_f, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
        for line in data:
            writer.writerow(line)
    print("songlist.csv generated")


if __name__ == '__main__':
    import argparse
    argParser = argparse.ArgumentParser(description='Parse .tja files in a songdir and parse to csv')
    argParser.add_argument('dir', help='Directory to parse')
    args = argParser.parse_args()

    create_csv(args.dir)
