#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Config reader to read the configuration file
#
# Software is free software released under the "GNU Affero General Public License v3.0"
#
# Copyright (c) 2021  PidgeyL

# imports
import configparser
import os
import psycopg2
import redis
import sys
runPath = os.path.dirname(os.path.realpath(__file__))

class Configuration():
    ConfigParser = configparser.ConfigParser()
    ConfigParser.read(os.path.join(runPath, "../etc/configuration.ini"))
    default = {'Redis': {'Host':    'localhost', 'Port':      6379,
                         'SongDB':   10,         'UserDB':    11,
                         'SourceDB': 12,         'ArtistDB':  13,
                         'TagDB':    14,         'CommentDB': 15,
                         'IDDB':     1,          'Password':  None,},
               'Database': {'Host':   'localhost', 'Port':     5432,
                            'User':   'tjadb',     'Password': '',
                            'DBName': 'tjadb'},
               'BotColors': {'SOTD':   0xf3f8fc, 'RandomSong': 0xa3f8fc,
                             'Search': 0x449920, 'About':      0xff1122,
                             'Donate': 0x338929,},
               'Bot': {'API': '', },
               'Web': {'Host': 'localhost', 'Port':  4987,
                       'URL':  'change.me', 'Debug': True, 'SSL':   False,
                       'CertFile': './ssl/tjadb.crt',
                       'KeyFile':  './ssl/tjadb.key',}}


    @classmethod
    def readSetting(cls, section, item):
        result = cls.default.get(section, {}).get(item)
        try:
            if type(result) == bool:
                result = cls.ConfigParser.getboolean(section, item)
            elif type(result) == int:
                result = cls.ConfigParser.getint(section, item)
            else:
                result = cls.ConfigParser.get(section, item)
        except:
            pass
        return result


    #########
    # Redis #
    #########
    @classmethod
    def getRedisConnectionParams(cls):
        return {'host':     cls.readSetting("Redis", "Host"),
                'port':     cls.readSetting("Redis", "Port"),
                'password': cls.readSetting("Redis", "Password"),
                'charset':  'utf-8', 'decode_responses': True}

    @classmethod
    def _genRedisConnection(cls, db):
        conn = cls.getRedisConnectionParams()
        conn['db'] =  cls.readSetting("Redis", db)
        return redis.StrictRedis(**conn)

    @classmethod
    @property
    def redis_ID_db(cls):
        return cls._genRedisConnection('IDDB')

    @classmethod
    @property
    def redis_user_db(cls):
        return cls._genRedisConnection('UserDB')

    @classmethod
    @property
    def redis_source_db(cls):
        return cls._genRedisConnection('SourceDB')

    @classmethod
    @property
    def redis_artist_db(cls):
        return cls._genRedisConnection('ArtistDB')

    @classmethod
    @property
    def redis_tag_db(cls):
        return cls._genRedisConnection('TagDB')

    @classmethod
    @property
    def redis_comment_db(cls):
        return cls._genRedisConnection('CommentDB')

    @classmethod
    @property
    def redis_song_db(cls):
        return cls._genRedisConnection('SongDB')


    ############
    # Postgres #
    ############
    @classmethod
    @property
    def db_connection(cls):
        host = cls.readSetting("Database", 'Host')
        port = cls.readSetting("Database", 'Port')
        user = cls.readSetting("Database", 'User')
        db   = cls.readSetting("Database", 'DBName')
        pwd  = cls.readSetting("Database", 'Password')
        try:
            return psycopg2.connect("host='%s' port='%s' dbname=%s user=%s password=%s"%(host, port, db, user, pwd))
        except Exception as e:
            print("WARNING: Could not connect to Postgres DB:")
            print(e)
            return None
