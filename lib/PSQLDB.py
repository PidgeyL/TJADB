#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# PostgreSQL database layer
#
# Software is free software released under the "GNU Affero General Public License v3.0"
#
# Copyright (c) 2021  PidgeyL

import psycopg2.extras

from lib.Config    import Configuration
from lib.Singleton import Singleton

class Database(metaclass=Singleton):
    def __init__(self):
        self.conn = Configuration().db_connection
        if not self.conn:
            raise Exception("Could not connect to the database")

    ############
    # Wrappers #
    ############
    def committing(funct):
        def wrapper(self, *args, **kwargs):
            try:
                cur    = self.conn.cursor()
                funct(self, cur, *args, **kwargs)
                # Fetch ID if returning, else return True
                result = cur.fetchone() if cur.description else True
            except Exception as e:
                self.conn.rollback()
                raise(e)
            else:
                self.conn.commit()
                if result == True:
                    return True
                return result[0] if result else None
        return wrapper


    def fetchall(funct):
        def wrapper(self, *args, **kwargs):
            cur = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
            funct(self, cur, *args, **kwargs)
            return cur.fetchall()
        return wrapper


    def fetchone(funct):
        def wrapper(self, *args, **kwargs):
            cur = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
            funct(self, cur, *args, **kwargs)
            return cur.fetchone()
        return wrapper


    ##################
    # Helper Queries #
    ##################
    @fetchall
    def _get_by_field(self, cur, table, field, value):
        cur.execute("SELECT * FROM %s WHERE %s = %%s"%(table, field), (value,))


    @fetchall
    def _get_all(self, cur, table):
        cur.execute("SELECT * FROM %s"%(table))


    @fetchone
    def _get_by_id(self, cur, table, value):
        cur.execute("SELECT * FROM %s WHERE id = %%s"%(table), (value,))


    #########
    # Users #
    #########
    @committing
    def add_user(self, cur, id=None, charter_name=None, discord_id=None,
                 email=None, password=None, salt=None, hashcount=None, staff=None,
                 image_url=None, about=None, preferred_difficulty_id=None,
                 preferred_language_id=None):
        s = """INSERT INTO users(charter_name, discord_id, email, password,
                 salt, hashcount, staff, image_url, about,
                 preferred_difficulty_id, preferred_language_id)
               VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)  RETURNING id;"""
        cur.execute(s, (charter_name, discord_id, email, password, salt,
                        hashcount, staff, image_url, about,
                        preferred_difficulty_id, preferred_language_id))


    @committing
    def update_user_password(self, cur, password, salt, hashcount):
        s = """UPDATE users SET password = %s, salt = %s, hashcount = %s,
               WHERE id = %s"""
        cur.execute(s, (password, salt, hashcount))


    @committing
    def update_user(self, cur, id=None, charter_name=None, discord_id=None,
                    email=None, staff=None, image_url=None, about=None,
                    preferred_difficulty_id=None, preferred_language_id=None,
                    **kwargs):
        if not id:
            return False
        # Update builder
        fields = [('charter_name', charter_name), ('discord_id', discord_id),
                  ('email', email), ('staff', staff), ('image_url', image_url),
                  ('about', about),
                  ('preferred_difficulty_id', preferred_difficulty_id),
                  ('preferred_language_id',   preferred_language_id)]
        values = []
        querystring = ""
        for field, value in fields:
            if not value:
                continue
            values.append(value)
            querystring += f"{field} = %s, "
        # Query builder
        if not querystring:
            return False
        querystring = querystring[:-2]
        values.append(id)
        cur.execute(f"UPDATE users  SET {querystring}  WHERE id = %s;", values)


    def get_user_by_id(self, id):
        return self._get_by_id('users', id)


    def get_user_by_charter_name(self, name):
        return self._get_by_field('users', 'charter_name', name)


    def get_user_by_discord_id(self, id):
        return self._get_by_field('users', 'discord_id', id)


    def get_staff_users(self):
        return self._get_by_field('users', 'staff', True)


    def get_all_users(self):
        return self._get_all('users')


    @fetchall
    def get_charters(self, cur):
        s = """SELECT * FROM users WHERE id IN (
                   SELECT charter_id FROM songs);"""
        cur.execute(s)

    ##########
    # Artist #
    ##########
    @committing
    def add_artist(self, cur, id=None, name_orig=None, name_en=None, link=None,
                   info=None):
        s = """INSERT INTO artists(name_orig, name_en, link, info)
               VALUES(%s, %s, %s, %s)  RETURNING id;"""
        cur.execute(s, (name_orig, name_en, link, info))


    @committing
    def update_artist(self, cur, id=None, name_orig=None, name_en=None,
                      link=None, info=None):
        s = """UPDATE artists
               SET name_orig = %s, name_en = %s, link = %s, info = %s
               WHERE id = %s"""
        cur.execute(s, (name_orig, name_en, link, info, id))


    def get_artist_by_id(self, id):
        return self._get_by_id('artists', id)


    def get_all_artists(self):
        return self._get_all('artists')


    ##############
    # Difficulty #
    ##############
    def get_difficulty_by_id(self, id):
        return self._get_by_id('difficulties', id)


    def get_all_difficulties(self):
        return self._get_all('difficulties')


    ############
    # Language #
    ############
    def get_language_by_id(self, id):
        return self._get_by_id('languages', id)


    def get_all_languages(self):
        return self._get_all('languages')


    ###############
    # Song_States #
    ###############
    def get_song_state_by_id(self, id):
        return self._get_by_id('song_states', id)


    def get_all_song_states(self):
        return self._get_all('song_states')


    ##########
    # Genres #
    ##########
    @committing
    def add_genre(self, cur, id=None, name_en=None, name_jp=None, tja_genre=None):
        s = """INSERT INTO genres(name_en, name_jp, tja_genre)
               VALUES(%s, %s, %s)  RETURNING id;"""
        cur.execute(s, (name_en, name_jp, tja_genre))


    @committing
    def update_genre(self, cur, id=None, name_en=None, name_jp=None,
                     tja_genre=None):
        s = """UPDATE genres
               SET name_en = %s, name_jp = %s, tja_genre = %s,
               WHERE id = %s"""
        cur.execute(s, (name_en, name_jp, tja_genre, id))


    def get_genre_by_id(self, id):
        return self._get_by_id('genres', id)


    def get_all_genres(self):
        return self._get_all('genres')



    ###########
    # Sources #
    ###########
    @committing
    def add_source(self, cur, id=None, name_orig=None, name_en=None, genre_id=None,
                   about=None):
        s = """INSERT INTO sources(name_orig, name_en, genre_id, about)
               VALUES(%s, %s, %s, %s)  RETURNING id;"""
        cur.execute(s, (name_orig, name_en, genre_id, about))


    @committing
    def update_source(self, cur, id=None, name_orig=None, name_en=None,
                      genre_id=None, about=None):
        s = """UPDATE sources
               SET name_orig = %s, name_en = %s, genre_id = %s, about = %s
               WHERE id = %s"""
        cur.execute(s, (name_orig, name_en, genre_id, about, id))


    def get_source_by_id(self, id):
        return self._get_by_id('sources', id)


    def get_all_sources(self):
        return self._get_all('sources')


    #########
    # Songs #
    #########
    def add_obj(self, data):
        obj = self.conn.lobject(mode='wb')
        obj.write(data)
        obj.close()
        self.conn.commit()
        return obj.oid


    @committing
    def delete_obj(self, cur, oid):
        obj = self.conn.lobject(oid=oid, mode='rb')
        obj.unlink()


    # Clearing out old objects to recuperate disk space
    def vacuum(self):
        old = self.conn.isolation_level
        self.conn.set_isolation_level(0) # Move out of transaction block
        self.conn.cursor().execute("VACUUM FULL")
        self.conn.commit()
        self.conn.set_isolation_level(old)


    def get_obj(self, oid):
        try:
            obj = self.conn.lobject(oid=oid, mode='rb')
            return obj.read()
        except:
            self.conn.rollback()
        return None


    @committing
    def add_song(self, cur, id=None, title_orig=None, title_en=None,
                 subtitle_orig=None, subtitle_en=None, source_id=None, bpm=None,
                 genre_id=None, charter_id=None, d_kantan=None,
                 d_kantan_charter_id=None, d_futsuu=None, d_futsuu_charter_id=None,
                 d_muzukashii=None, d_muzukashii_charter_id=None, d_oni=None,
                 d_oni_charter_id=None, d_ura=None, d_ura_charter_id=None,
                 d_tower=None, d_tower_lives=None, downloads=None,
                 last_updated=None, created=None, uploaded=None, info=None,
                 video_link=None, state_id=None, obj_tja=None, obj_ogg=None,
                 obj_bg_video_picture=None, tja_orig_md5=None, tja_en_md5=None):
        s = """INSERT INTO songs(title_orig, title_en, subtitle_orig, subtitle_en,
                 source_id, bpm, genre_id, charter_id, d_kantan,
                 d_kantan_charter_id, d_futsuu, d_futsuu_charter_id, d_muzukashii,
                 d_muzukashii_charter_id, d_oni, d_oni_charter_id, d_ura,
                 d_ura_charter_id, d_tower, d_tower_lives, downloads,
                 last_updated, created, uploaded, info, video_link, state_id,
                 obj_tja, obj_ogg, obj_bg_video_picture, tja_orig_md5, tja_en_md5)
               VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                      %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                      %s, %s)
               RETURNING ID;"""
        cur.execute(s, (title_orig, title_en, subtitle_orig, subtitle_en,
                 source_id, bpm, genre_id, charter_id, d_kantan,
                 d_kantan_charter_id, d_futsuu, d_futsuu_charter_id, d_muzukashii,
                 d_muzukashii_charter_id, d_oni, d_oni_charter_id, d_ura,
                 d_ura_charter_id, d_tower, d_tower_lives, downloads,
                 last_updated, created, uploaded, info, video_link, state_id,
                 obj_tja, obj_ogg, obj_bg_video_picture, tja_orig_md5, tja_en_md5))


    def get_song_by_id(self, id):
        return self._get_by_id('songs', id)


    @fetchall
    def get_song_by_artist_id(self, cur, artist_id):
        s = """SELECT * FROM songs
               WHERE id IN(
                 SELECT song_id FROM artists_per_song
                 WHERE artist_id = %s
               );"""
        cur.execute(s, (artist_id, ))


    def get_song_by_charter_id(self, id):
        return self._get_by_field('songs', 'charter_id', id)


    def get_song_by_source_id(self, id):
        return self._get_by_field('songs', 'source_id', id)


    def get_all_songs(self):
        return self._get_all('songs')



    #####################
    # Artists for Songs #
    #####################
    @committing
    def add_artist_to_song(self, cur, song_id, artist_id):
        s = """INSERT INTO artists_per_song(song_id, artist_id)
               VALUES(%s, %s);"""
        cur.execute(s, (song_id, artist_id))


    @fetchall
    def get_artists_for_song_id(self, cur, song_id):
        s = """SELECT * FROM artists
               WHERE id IN(
                 SELECT artist_id FROM artists_per_song
                 WHERE song_id = %s );"""
        cur.execute(s, (song_id, ))


    ###################
    # Song of the Day #
    ###################
    @fetchone
    def get_song_of_the_day(self, cur, day):
        s = """SELECT * FROM songs
               WHERE id IN(
                 SELECT song_id FROM song_of_the_day_history
                 WHERE "date" = %s );"""
        cur.execute(s, (day, ))


    @committing
    def set_song_of_the_day(self, cur, day, song_id):
        s = """INSERT INTO song_of_the_day_history(date, song_id)
               VALUES(%s, %s)""";
        cur.execute(s, (day, song_id, ))


    #####################
    # Database Settings #
    #####################
    @committing
    def save_setting(self, cur, name, type, value):
        s = """INSERT INTO tjadb_settings(name, type, value)
               VALUES(%s, %s, %s)
               ON CONFLICT (name) DO UPDATE
                 SET type  = excluded.type,
                     value = excluded.value;""";
        cur.execute(s, (name, type, value))

    @fetchone
    def get_setting(self, cur, name):
        s = """SELECT * FROM tjadb_settings WHERE name = %s;"""
        cur.execute(s, (name, ))

    @fetchall
    def get_settings(self, cur):
        s = """SELECT * FROM tjadb_settings;"""
        cur.execute(s)

    @committing
    def add_to_list_setting(self, cur, name, value):
        s = """UPDATE tjadb_settings
               SET value = value::jsonb || '[%s]'::jsonb
               WHERE name = %s;"""
        cur.execute(s, (value, name))

    @committing
    def remove_from_list_setting(self, cur, name, value):
        s = """UPDATE tjadb_settings
               SET value = value::jsonb - %s::jsonb
               WHERE name = %s;"""
        cur.execute(s, (value, name))
