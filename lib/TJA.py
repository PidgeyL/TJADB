
# Imports
import base64
import os
import sys

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))


# Functions
def read_tja(path):
    raw = open(path, 'rb').read()
    return decode_tja(raw)


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


def encode_tja(text):
    return text.encode('utf-8-sig')


def set_tja_metadata(tja=None, title=None, sub=None, song=None):
    return_raw = False
    if isinstance(tja, bytes):
        tja = decode_tja(tja)
        return_raw = True

    new_tja = ''
    for line in tja.splitlines():
        if title and line.lower().startswith('title:'):
            line = line.split(':')[0] + ':' + title
        if sub   and line.lower().startswith('subtitle:'):
            line = line.split(':')[0] + ':' + sub
        if song  and line.lower().startswith('wave:'):
            line = line.split(':')[0] + ':' + song
        new_tja = new_tja + line + '\r\n'
    if return_raw:
        return encode_tja(new_tja)
    return new_tja


def parse_tja(tja):
    return_raw = False
    if isinstance(tja, bytes):
        tja = decode_tja(tja)
        return_raw = True

    meta = {'title': '', 'sub': '', 'bpm': '', 'song': '', 'genre': '',
            'easy': '', 'normal': '', 'hard': '', 'oni': '', 'ura': ''}
    difficulty = None
    for line in tja.splitlines():
        if   line.lower().startswith('title:'):    meta['title'] = line.split(':')[1]
        elif line.lower().startswith('subtitle:'): meta['sub']   = line.split(':')[1]
        elif line.lower().startswith('bpm:'):      meta['bpm']   = line.split(':')[1]
        elif line.lower().startswith('wave:'):     meta['song']  = line.split(':')[1]
        elif line.lower().startswith('genre:'):    meta['genre'] = line.split(':')[1]
        elif line.lower().startswith('course'):
            difficulty = line.split(':')[1].lower()
            if difficulty == 'edit':
                difficulty = 'ura'
        elif line.lower().startswith('level:'):
            meta[difficulty] = line.split(':')[1]
        if all( [len(x) > 0 for x in meta.values()] ):
            return meta
    return meta
