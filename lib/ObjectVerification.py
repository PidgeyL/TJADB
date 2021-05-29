import os
import sys

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

from lib.Objects import Song


def verify_song(song):
    none = type(None)
    try:
        assert isinstance(song,                Song)
        assert isinstance(song._id,           (int, none))
        assert isinstance(song.title_orig,     str)
        assert isinstance(song.title_eng,      str)
        assert isinstance(song.subtitle_orig, (str, none))
        assert isinstance(song.subtitle_eng,  (str, none))
        assert isinstance(song.artist_orig,    str)
        assert isinstance(song.artist_eng,     str)
        assert isinstance(song.source_orig,   (str, none))
        assert isinstance(song.source_eng,    (str, none))
        #assert isinstance(song.mapper,         Mapper)
        #assert isinstance(song.Genre,          Genre)
        assert isinstance(song.bpm,            int)
        assert isinstance(song.vetted,         bool)
        assert isinstance(song.d_kantan,       int)
        assert isinstance(song.d_futsuu,       int)
        assert isinstance(song.d_muzukashii,   int)
        assert isinstance(song.d_oni,          int)
        assert isinstance(song.d_ura,          int)
        assert isinstance(song.comments,      (str, none))
        assert isinstance(song.video_link,    (str, none))
        assert isinstance(song.path,           str)
        assert isinstance(song.md5,            str)

        assert len(song.title_orig)  > 0
        assert len(song.title_eng)   > 0
        assert len(song.artist_orig) > 0
        assert len(song.artist_eng)  > 0
        assert len(song.path)        > 0
        assert len(song.md5)        == 32
        assert -1 < song.d_kantan     < 11
        assert -1 < song.d_futsuu     < 11
        assert -1 < song.d_muzukashii < 11
        assert -1 < song.d_oni        < 11
        assert -1 < song.d_ura        < 11
        return True
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(e)
        return False
