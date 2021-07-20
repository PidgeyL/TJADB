import os
import sys

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

from lib.DatabaseLayer import DatabaseLayer
from lib.Objects       import Charter

# Python3 compatibility & safety
try:
    input = raw_input
except NameError:
    pass


def query_info():
    while True:
        name  = input('Charter Name: ')
        staff = True if input('Staff? y/n: ').lower() == 'y' else False
        if input("Is this correct? y/n: ").lower() == 'y':
            return Charter(None, name, None, None, staff)


if __name__ == '__main__':
    db = DatabaseLayer()
    while True:
        charter = query_info()
        db.charters.add(charter)
        if input("Add more? y/n: ").lower() == 'n':
            break
