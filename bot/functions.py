import asyncio
import os
import random
import sys

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

from etc.Settings      import Settings
from lib.DatabaseLayer import DatabaseLayer
from bot.formatting    import embed_searchlist_en, embed_random_song_en, embed_sotd_en, embed_error, embed_website_en, embed_settings

dbl = DatabaseLayer()

def search_songs(term, songlist):
    return [song for song in songlist if match_song(song)]


def get_website():
    count  = str(len(dbl.cache.get_all_keys('song')))
    return embed_website_en(count)


def search_songs(term):
    def match_song(song, search):
        fields = ['title_orig', 'title_en']
        values = [getattr(song, f) for f in fields]
        values.extend([a.name_orig for a in song.artists])
        values.extend([a.name_en   for a in song.artists])
        if song.source:
            values.extend([song.source.name_en, song.source.name_orig])
        for field in values:
            if search.lower() in field.lower():
                return True
        return False

    songs = [song for song in dbl.songs.get_all() if match_song(song, term)]
    return embed_searchlist_en(term, songs)


def random_song():
    rand = random.choice(dbl.cache.get_all_keys('song'))
    return embed_random_song_en(dbl.songs.get_by_id(rand))


def get_sotd():
    return embed_sotd_en( dbl.songs.get_sotd() )


def publish_sotd(bot):
    async def _send_to_channel(channel_id, embed):
        channel = bot.get_channel(channel_id)
        await channel.send(embed=embed)

    embed = get_sotd()
    try:
        for channel_id in dbl.bot.get_sotd_channels():
            bot.loop.create_task(_send_to_channel(channel_id, embed))
    except Exception as e:
        print("Could not publish SotD")
        print(e)


def set_setting(setting, value):
    settings = dbl.settings.get_all()
    if 'bot_color_' + setting.lower() in [x['name'] for x in settings]:
        setting = 'bot_color_'+setting
        try:
            if value.startswith("#"):
                value = value[1:]
            value = int(value, 16)
        except Exception as e:
            return "Invalid hex code"
    if setting.lower() not in [x['name'] for x in settings]:
        return "Unknown setting"
    dbl.settings.save(setting.lower(), value)
    return f'Setting "{setting}" set to "{value}"'


def get_current_settings():
    bot_settings = ['sotd_channels']
    settings = dbl.settings.get_all()
    colors = [s for s in settings if s['name'].startswith('bot_color_')]
    return embed_settings(colors)

