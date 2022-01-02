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
                result = cur.fetchone()
            except Exception as e:
                self.conn.rollback()
                raise(e)
            else:
                self.conn.commit()
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
    def update_user(self, cur, id=None, charter_name=None, discord_id=None,
                    email=None, password=None, salt=None, hashcount=None,
                    staff=None, image_url=None, about=None,
                    preferred_difficulty_id=None, preferred_language_id=None):
        s = """UPDATE users
               SET charter_name = %s, discord_id = %s, email = %s, password = %s,
                 salt = %s, hashcount = %s, staff = %s, image_url = %s,
                 about = %s, preferred_difficulty_id = %s,
                 preferred_language_id = %s):
               WHERE id = %s"""
        cur.execute(s, (charter_name, discord_id, email, password, salt,
                        hashcount, staff, image_url, about,
                        preferred_difficulty_id, preferred_language_id, id))


    def get_user_by_id(self, id):
        return self._get_by_id('users', id)


    def get_all_users(self):
        return self._get_all('users')


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
    @committing
    def add_song(self, cur, id=None, ):
        s = """INSERT INTO """
        cur.execute(s, ())
