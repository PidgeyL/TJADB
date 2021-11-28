import discord

from etc.Settings import Settings
conf = Settings()


################################
# General Formatting Functions #
################################
def difficulty(song):
    result =  ""
    for dif in ['d_kantan', 'd_futsuu', 'd_muzukashii', 'd_oni', 'd_ura']:
        rate = getattr(song, dif)
        if not rate:
            rate="-"
        result += str(rate) + '/'
    return result[:-1]


##########################
# Embed return functions #
##########################
def embed_error(error, message):
    embed = discord.Embed(title = f"__**Whoops...**__",
                          color = conf.bot_sotd_color)
    embed.add_field( name = error, value = message )
    return embed


def embed_website_en(url, count):
    embed = discord.Embed(title = f"__**TJADB-Web (%s)**__"%url, url = url,
                          color = conf.bot_about_color,
                          description = "Custom TJA database, filled with TJA's from the **TJADB** community.\n Website and bot made by <@567430051168256012>")
    embed.set_footer(text="Database song count: %s"%count)
    return embed


def embed_donate():
    desc = """**Thank you for considering donating to the TJADB project!**
Donations are used to keep the website, discord bot, domain and ESE torrent alive.
Excess donations will be stored separately, to keep a buffer for months with less donations.
If we reach a point where we have a large excess of donations, we will notify any donors. For any questions, contact staff or <@567430051168256012> (sysadmin)

Once you make a donation, ping <@567430051168256012>. Certain donation tiers get rewarded with a small thank you, and every donation is noted down for full transparancy."""

    embed = discord.Embed(title = f"__**TJADB Donations**__",
                          color = conf.bot_donate_color,
                          description = desc)
    embed.add_field( name = "SubscribeStar",   value = "https://www.subscribestar.com/pidgey" , inline=False)
    embed.add_field( name = "GitHub Sponsors", value = "https://github.com/sponsors/PidgeyL" , inline=False)
    embed.add_field( name = "PayPal",          value = "https://www.paypal.com/donate?hosted_button_id=CDG9K5LHEHXKA", inline=False)
    return embed


def embed_sotd_en(song):
    embed = discord.Embed(title = f"__**Song of the Day**__",
                          color = conf.bot_sotd_color)
    embed.add_field( **song_namecard(song, en=True) )
    return embed


def embed_random_song_en(song):
    embed = discord.Embed(title = f"__**Random Song**__",
                          color = conf.bot_random_song_color)
    embed.add_field( **song_namecard(song, en=True) )
    return embed


def embed_searchlist_en(term, songs):
    embed = discord.Embed(title = f"__**Results for: {term}**__",
                          color = conf.bot_search_color)
    for song in songs:
        embed.add_field( **song_namecard(song, en=True) )
    return embed


#########################
# Embed build functions #
#########################
def song_namecard(song, en=True):
    title   = song.title_eng      if en else song.title_orig
    artist  = song.artist_eng     if en else song.artist_orig
    genre   = song.genre.name_eng if en else song.genre.name_jp
    charter = song.charter.name

    name  = f"**{title}** by {artist} ({genre})"
    body  = f"> Charter: {charter} | {song.bpm}bpm | {difficulty(song)}\n"
    body += f"> DL: [Original]({conf.url}/download/orig/{song._id})"
    body += f"  -  [English]({conf.url}/download/eng/{song._id})"
    return {'name': name, 'value': body}
