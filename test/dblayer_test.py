import os
import sys

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

from lib.DatabaseLayer import DatabaseLayer
from lib.Objects       import Song, Genre, Charter

db = DatabaseLayer()

g = Genre(None, 'ボーカロイド', 'Vocaloid', 'ボーカロイド')
c = Charter(None, 'Bandai Namco', b'png', '', False)

g._id = db.genres.add(g)
c._id = db.charters.add(c)

s = Song(None,'千本桜', 'Senbonzakura', '黒うさP feat.初音ミク',
           'Kurousa-P feat. Hatsune Miku', '黒うさP', 'Kurousa-P', None, None,
            154, g, c, 3, 5, 6, 7, 8, True, None, None, '/tmp/test.zip',
           'c5f8f41459bdbc3f77e72601b7f5ebd1')

db.songs.add(s)
