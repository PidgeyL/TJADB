#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Database-ready "Song" object
#
# Software is free software releasedunder the "GNU Affero General Public License v3.0"
#
# Copyright (c) 2021-2022  PidgeyL

from copy import copy

from lib.DatabaseLayer   import DatabaseLayer as dbl
from lib.objects.helpers import multi_assert, Object

class Song(Object):
    def __init__(self, id=None, title_orig=None, title_en=None, subtitle_orig=None,
                 subtitle_en=None, source_id=None, source=None, bpm=None,
                 genre_id=None, genre=None, charter_id=None, charter=None,
                 d_kantan=None, d_kantan_charter_id=None, d_kantan_charter=None,
                 d_futsuu=None, d_futsuu_charter_id=None, d_futsuu_charter=None,
                 d_muzukashii=None, d_muzukashii_charter_id=None,
                 d_muzukashii_charter=None, d_oni=None, d_oni_charter_id=None,
                 d_oni_charter=None, d_ura=None, d_ura_charter_id=None,
                 d_ura_charter=None, d_tower=None, d_tower_lives=None,
                 downloads=None, last_updated=None, created=None, uploaded=None,
                 info=None, video_link=None, state=None, state_id=None,
                 obj_tja=None, obj_ogg=None, obj_bg_video_picture=None,
                 tja_orig_md5=None, tja_en_md5=None, artists=None):
        self._id           = id
        self.title_orig    = title_orig
        self.title_en      = title_en
        self.subtitle_orig = subtitle_orig
        self.subtitle_en   = subtitle_en
        self.bpm           = bpm
        self.d_kantan      = d_kantan
        self.d_futsuu      = d_futsuu
        self.d_muzukashii  = d_muzukashii
        self.d_oni         = d_oni
        self.d_ura         = d_ura
        self.d_tower       = d_tower
        self.d_tower_lives = d_tower_lives
        self.last_updated  = last_updated
        self.created       = created
        self.uploaded      = uploaded
        self.info          = info
        self.video_link    = video_link
        self.obj_tja       = obj_tja
        self.obj_ogg       = obj_ogg
        self.obj_bg_video_picture = obj_bg_video_picture
        self.tja_orig_md5  = tja_orig_md5
        self.tja_en_md5    = tja_en_md5

        self.source  = source  if source  else dbl().sources.get_by_id(source_id)
        self.genre   = genre   if genre   else dbl().genres.get_by_id(genre_id)
        self.charter = charter if charter else dbl().users.get_by_id(charter_id)
        self.state   = state   if state   else dbl().song_states.get_by_id(state_id)

        if d_kantan_charter:
            self.d_kantan_charter = d_kantan_charter
        else:
            self.d_kantan_charter =  dbl().users.get_by_id(d_kantan_charter_id)

        if d_futsuu_charter:
            self.d_futsuu_charter = d_futsuu_charter
        else:
            self.d_futsuu_charter =  dbl().users.get_by_id(d_futsuu_charter_id)

        if d_muzukashii_charter:
            self.d_muzukashii_charter = d_muzukashii_charter
        else:
            self.d_muzukashii_charter =  dbl().users.get_by_id(d_muzukashii_charter_id)

        if d_oni_charter:
            self.d_oni_charter = d_oni_charter
        else:
            self.d_oni_charter =  dbl().users.get_by_id(d_oni_charter_id)

        if d_ura_charter:
            self.d_ura_charter = d_ura_charter
        else:
            self.d_ura_charter =  dbl().users.get_by_id(d_ura_charter_id)

        self.artists = []
        if artists:
            for artist in artists:
                if isinstance(artist, int):
                    self.artists.append(dbl().artists.get_by_id(artist))
                else:
                    self.artists.append(artist)


    def verify(self):
        from lib.objects import Genre, User, Source, SongState, Artist
        from datetime    import date
        multi_assert(self._id, self.d_kantan, self.d_futsuu, self.d_muzukashii,
                     self.d_oni, self.d_ura,          types=( int,   type(None) ))
        multi_assert(self.title_orig, self.title_en, self.subtitle_orig,
                     self. subtitle_en,               types=( str ))
        multi_assert(self.video_link, self.info,      types=( str,    type(None) ))
        multi_assert(self.bpm,                        types=( float ))
        multi_assert(self.last_updated, self.created, types=( date ))
        multi_assert(self.source,                     types=( Source, type(None) ))
        multi_assert(self.state,                   types=( SongState, type(None) ))
        multi_assert(self.genre,                      types=( Genre,  type(None) ))
        multi_assert(self.charter, self.d_kantan_charter, self.d_futsuu_charter,
                     self.d_muzukashii_charter, self.d_oni_charter,
                     self.d_ura_charter,              types=( User,   type(None) ))
        multi_assert(*self.artists,                   types=( Artist ))


    def as_dict(self):
        d = copy(vars(self))
        d['id'] = self._id
        d['source_id']  = d['source'].id if self.source else None
        d['genre_id']   = d['genre'].id
        d['charter_id'] = d['charter'].id
        d['state_id']   = d['state'].id
        d['artists']    = [ x.as_dict() for x in d['artists'] ]

        for key in ['d_kantan_charter', 'd_futsuu_charter', 'd_muzukashii_charter',
                    'd_oni_charter', 'd_ura_charter']:
            if d[key]:
                d[key+'_id'] = d[key].id

        for key in ['source', 'genre', 'charter', 'state', 'd_kantan_charter',
                    'd_futsuu_charter', 'd_muzukashii_charter', 'd_oni_charter',
                    'd_ura_charter', '_id']:
            d.pop(key, None)
        return d


    def as_info_string(self):
        _alt    = lambda orig, alt: orig if orig == alt else "%s (%s)"%(orig, alt)
        _course = lambda course: str(course) if course else '*'

        diff = [self.d_kantan, self.d_futsuu, self.d_muzukashii, self.d_oni,
                self.d_ura]
        diff = '/'.join([_course(d) for d in diff])
        charters =  [self.charter, self.d_kantan_charter, self.d_futsuu_charter,
                     self.d_muzukashii_charter, self.d_oni_charter,
                     self.d_ura_charter]
        charters = ' & '.join({c.charter_name for c in charters if c})

        text  = "Title:  %s\nArtist(s):  "%_alt(self.title_orig, self.title_en)
        text += ' & '.join([_alt(a.name_orig, a.name_en) for a in self.artists])
        if self.source:
            text += "\nFrom:  %s\n"%_alt(self.source.name_orig, self.source.name_en)
        text += "Charter(s):  %s\n"%charters
        text += "Difficulty:  %s\n"%diff
        text += "Genre:  %s (%s)\n"%(self.genre.name_jp, self.genre.name_en)
        text += "BPM:  %s\n"%self.bpm
        text += "Last Update:  %s"%self.last_updated.strftime("%Y-%m-%d")
        return text
