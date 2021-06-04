import base64
import copy
import csv
import os
import sys
import zipfile


def decode_tja(raw):
    for enc in ['utf-8-sig', 'utf-8', 'utf-16', 'shift-jis', 'shift-jis_2004']:
        try:
            data = raw.decode(enc)
            assert 'TITLE:' in data
            return data
        except Exception as e:
            pass
    print("unknown encoding")
    print("Copy the below in cyberchef for bruteforcing:")
    print(base64.b64encode(raw[:300]))
    sys.exit()


def read_tja(file):
    raw = open(file, 'rb').read()
    return decode_tja(raw)


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


# returns title, sub, bpm, genre, kantan, futsuu, muzukashii, oni, ura, song, path
def parse_tja(path, data):
    title = ''
    sub   = ''
    bpm   = ''
    song  = ''
    genre = ''
    dif   = {'kantan': '', 'futsuu': '', 'muzukashii': '', 'oni': '', 'ura': ''}
    difficulty = None

    for line in data.splitlines():
        if line.lower().startswith('title:'):    title = line.split(':')[1]
        if line.lower().startswith('subtitle:'): sub   = line.split(':')[1]
        if line.lower().startswith('bpm:'):      bpm   = line.split(':')[1]
        if line.lower().startswith('wave:'):     song  = line.split(':')[1]
        if line.lower().startswith('genre:'):    genre = line.split(':')[1]
        if line.lower().startswith('course'):
            if 'easy'   in line.lower(): difficulty = 'kantan'
            if 'normal' in line.lower(): difficulty = 'futsuu'
            if 'hard'   in line.lower(): difficulty = 'muzukashii'
            if 'oni'    in line.lower(): difficulty = 'oni'
            if 'ura'    in line.lower(): difficulty = 'ura'
        if line.lower().startswith('level:'):
            dif[difficulty] = line.split(':')[1]
    return ( title, sub, bpm, genre, dif['kantan'], dif['futsuu'], dif['muzukashii'], dif['oni'], dif['ura'], song, path )


def create_csv(dir):
    data = [('title_orig', 'title_eng', 'subtitle_orig', 'subtitle_eng',
             'artist_orig', 'artist_eng', 'charter', 'bpm', 'vetted', 'd_kantan',
             'd_futsuu', 'd_muzukashii', 'd_oni', 'd_ura', 'source_orig',
             'source_eng', 'genre', 'comments', 'video_link', 'path', 'songpath',
             'added', 'updated')]
    for tja in read_dir(dir):
        d = parse_tja(*tja)
        data.append( (d[0], '', d[1], '', '', '', '', d[2], 'no', d[4], d[5], d[6],
                      d[7], d[8], '', '', d[3], '', '', d[10], d[9], '', '') )

    with open('songlist.csv', mode='w', encoding="utf16") as _f:
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
