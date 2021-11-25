import discord
import os
import sys
from   discord.ext import commands

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

import bot.formatting as forms
import bot.functions  as funct

from bot.functions     import search_songs, random_song, get_sotd, update_sotd, publish_sotd, get_website
from etc.Settings      import Settings
from lib.DatabaseLayer import Cache
from lib.Scheduler     import Scheduler

bot      = commands.Bot(command_prefix='~', description="TJADB Search Bot")
schedule = Scheduler()


@bot.command(name = "search", aliases=['s'])
async def search_command(ctx, term: str):
    await ctx.send(embed = search_songs(term))


@bot.command(name = "random", aliases=['r', 'rand', 'randomsong'])
async def random_command(ctx):
    await ctx.send(embed = random_song())


@bot.command(name = "sotd", aliases=['songoftheday'])
async def sotd_command(ctx):
    await ctx.send(embed = get_sotd())


@bot.command(name = "refresh", aliases=['update'])
async def refresh_command(ctx):
    Cache().refresh()
    await ctx.send("Song cache updated")


@bot.command(name = "link", aliases=['web', 'home', 'homepage', 'about'])
async def about_command(ctx):
    await ctx.send(embed = get_website())


@bot.command(name = "donate", aliases=['sponsor', 'support'])
async def donate_command(ctx):
    await ctx.send(embed = forms.embed_donate())


# Events
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="with fire"))

    schedule.start()
    print('Aww shi-, here we go again.')


if __name__ == "__main__":
    # Scheduled Tasks
    schedule.add_minute(Cache().refresh)
    schedule.add_daily(update_sotd)
    schedule.add_daily(publish_sotd, bot)

    bot.run(Settings().bot_api_key)
