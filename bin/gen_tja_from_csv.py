# Imports
import csv
import os
import sys

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

from lib.TJA import read_tja, set_tja_metadata, parse_tja, write_tja

# Functions
def update_tja(path, title, sub, song, numbered=False):
    def valid_path(string):
        for c in '\/:*?"<>|':
            string = string.replace(c, "_")
        return string

    print(path)
    title     = valid_path(title)
    orig_dir  = os.path.dirname(path)
    to_dir    = os.path.join(*os.path.split(orig_dir)[:-1], title)
    if numbered:
        topdir = os.path.join(*os.path.split(to_dir)[:-1])
        number = os.path.split(orig_dir)[-1].split(' ')[0]
        to_dir =os.path.join(topdir, number+' '+title)
    orig_file = os.path.splitext(path)[0]
    to_file   = os.path.join(os.path.dirname(path), title)

    # update TJA
    tja       = read_tja(path)
    orig_song = parse_tja(tja)['song']
    tja = set_tja_metadata(tja, title=title, sub=sub, song=valid_path(title))
    write_tja(tja, path)

    # Rename everything
    if orig_file != to_file: os.rename(orig_file+'.tja', to_file+'.tja')
    if orig_file != to_file: os.rename(os.path.join(orig_dir,orig_song), to_file+'.ogg')
    if orig_dir  != to_dir:  os.rename(orig_dir, to_dir)


def csv_to_tjas(songfile, to_orig=False, numbered=False, prefix=''):
    offset = 0 if to_orig else 1
    with open(songfile, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line in list(csv_reader)[1:]:
            path  = prefix + line[19]
            title = line[0+offset]
            sub   = line[2+offset]
            song  = line[20]
            update_tja(path, title, sub, song, numbered)


if __name__ == '__main__':
    import argparse
    argParser = argparse.ArgumentParser(description="Generate tja's in the alternative language")
    argParser.add_argument('songfile', help='songlist csv')
    argParser.add_argument('-o', action='store_true',  help='to original: read english, write original')
    argParser.add_argument('-n', action='store_true',  help='directories have numbers')
    argParser.add_argument('-p', type=str, default='', help='prefix for the path')

    args = argParser.parse_args()

    csv_to_tjas(args.songfile, to_orig=args.o, numbered=args.n, prefix=args.p)
