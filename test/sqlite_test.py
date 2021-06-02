import os
import sys

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

from lib.SQLiteDB import Database

db = Database()

#g_id = db.add_genre('ボーカロイド', 'Vocaloid', 'ボーカロイド')
g_id = 3
c_id = db.add_charter('Bandai Namco', b'png', '', False)

db.add_song('千本桜', 'Senbonzakura', '黒うさP feat.初音ミク',
            'Kurousa-P feat. Hatsune Miku', '黒うさP', 'Kurousa-P', None, None,
            154, g_id, c_id, 3, 5, 6, 7, 8, True, None, None, '/tmp/test.zip',
            'some_md5', '2021-04-31', '2021-04-31')
