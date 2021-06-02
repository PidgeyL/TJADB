import os
import sys

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

from lib.DatabaseLayer import DatabaseLayer
from lib.Objects       import Genre

# Python3 compatibility & safety
try:
    input = raw_input
except NameError:
    pass


def query_info():
    while True:
        name_jp = input('Japanese Title: ')
        name_en = input('English Title: ')
        genre   = input('Genre tag: ')
        if input("Is this correct? y/n").lower() == 'y':
            return Genre(None, name_jp, name_en, genre)


if __name__ == '__main__':
    db = DatabaseLayer()
    while True:
        genre = query_info()
        db.genres.add(genre)
        if input("Add more? y/n").lower() == 'n':
            break
