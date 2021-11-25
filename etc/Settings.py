import os
import sys

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

from lib.Singleton import Singleton

def full_path(path):
    path = os.path.join(run_path, '..', path)
    return os.path.normpath(path)


class Settings(metaclass=Singleton):
    # Logging
    # Web server
    port      = 4987
    host      = "127.0.0.1"
    url       = "https://dev.pidgey.net"
    debug     = True
    # SSL
    ssl       = True
    certfile  = './ssl/tjadb.crt'
    keyfile   = './ssl/tjadb.key'

    # Database
    file_db   = full_path('./db/files/')
    sqlite_db = full_path('./db/metadata.db')

    # Discord Bot
    bot_sotd_color        = 0xf3f8fc
    bot_random_song_color = 0xa3f8fc
    bot_search_color      = 0x449920
    bot_about_color       = 0xff1122
    bot_donate_color      = 0x338929
    bot_api_key           = ''
    bot_sotd_channels     = []
