class Genre:
    def __init__(self, db_id:int, name_eng:str, name_jp:str, genre:str):
        self._id      = db_id
        self.name_eng = name_eng
        self.name_jp  = name_jp
        self.genre    = genre


class Charter:
    def __init__(self, db_id:int, name:str, image:bytes, about:str, staff:bool):
        self._id   = db_id
        self.name  = name
        self.image = image
        self.about = about
        self.staff = bool(staff)

class Song:
    def __init__(self, db_id:int, title_orig:str, title_eng:str,subtitle_orig:str,
                       subtitle_eng:str, artist_orig:str, artist_eng:str,
                       source_orig:str, source_eng:str, bpm:float, genre:Genre,
                       charter:Charter,kantan:int, futsuu:int,
                       muzukashii:int, oni:int, ura:int, vetted:bool,
                       comments:str, video_link:str, path:str, md5:str,
                       added:str, updated:str):
        self._id           = db_id
        self.title_orig    = title_orig
        self.title_eng     = title_eng
        self.subtitle_orig = subtitle_orig
        self.subtitle_eng  = subtitle_eng
        self.artist_orig   = artist_orig
        self.artist_eng    = artist_eng
        self.charter       = charter
        self.bpm           = bpm
        self.vetted        = bool(vetted)
        self.d_kantan      = kantan
        self.d_futsuu      = futsuu
        self.d_muzukashii  = muzukashii
        self.d_oni         = oni
        self.d_ura         = ura
        self.source_orig   = source_orig
        self.source_eng    = source_eng
        self.genre         = genre
        self.comments      = comments
        self.video_link    = video_link
        self.path          = path
        self.md5           = md5
        self.added         = added
        self.updated       = updated


    def to_dict(self):
        obj = dict(vars(self))
        difficulties = [x for x in obj.keys() if x.startswith('d_')]
        for remove in (['_id', 'path', 'genre', 'charter'] + difficulties):
            del obj[remove]
        obj['charter']    = self.charter.name
        obj['genre_eng']  = self.genre.name_eng
        obj['genre_jp']   = self.genre.name_jp
        obj['difficulty'] = {}
        for difficulty in difficulties:
            obj['difficulty'][difficulty[2:]] = getattr(self, difficulty)
        return obj
