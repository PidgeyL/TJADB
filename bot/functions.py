import asyncio
import os
import random
import sys

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

from etc.Settings      import Settings
from lib.DatabaseLayer import Cache, DatabaseLayer
from bot.formatting    import embed_searchlist_en, embed_random_song_en, embed_sotd_en, embed_error, embed_website_en


##
# Variables
##
_SOTD_ = None


def get_website():
    url    = Settings().url
    count  = str(len(Cache().get_all_songs()))
    return embed_website_en(url, count)


def search_songs(term):
    songs = Cache().search(term)
    return embed_searchlist_en(term, songs)


def random_song():
    rand = random.choice(Cache().get_all_songs())
    return embed_random_song_en(rand)


def get_sotd():
    if _SOTD_:
        return embed_sotd_en(_SOTD_)
    return embed_error("Song of the Day not set",
                       "Seems like for some reason, the bot has not selected a SotD. Please contact the bot admin.")


def update_sotd():
    try:
        global _SOTD_
        _SOTD_ = random.choice(Cache().get_all_songs())
    except:
        pass


def publish_sotd(bot):
    async def _send_to_channel(channel_id, embed):
        channel = bot.get_channel(channel_id)
        await channel.send(embed=embed)

    embed = get_sotd()
    try:
        for channel_id in DatabaseLayer().bot.get_sotd_publish_channels():
            bot.loop.create_task(_send_to_channel(channel_id, embed))
    except Exception as e:
        print("Could not publish SotD")
        print(e)
