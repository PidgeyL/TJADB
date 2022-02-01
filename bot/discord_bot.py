import discord
import functools
import os
import sys
from   discord.ext import commands

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

import bot.formatting as forms

from bot.functions     import search_songs, random_song, get_sotd, publish_sotd, get_website, get_current_settings, set_setting
from etc.Settings      import Settings
from lib.DatabaseLayer import DatabaseLayer
from lib.Config        import Configuration
from lib.Scheduler     import Scheduler

def log(message):
    print(message)


class TJADB_Bot(commands.Bot):
    def __init__(self, command_prefix, self_bot):
        commands.Bot.__init__(self, command_prefix=command_prefix,
                                    self_bot=self_bot)
        self.prefix   = command_prefix
        self.dbl      = DatabaseLayer()
        self.schedule = Scheduler()
        #Schedule tasks
        self.schedule.add_daily(publish_sotd, self)
        #CACHE
        self.moderators = [ u.discord_id for u in self.dbl.users.get_staff() ]
        self.banned = []
        # Set up commands
        self.add_commands()


    ##############
    # Decorators #
    ##############
    def moderator(self, func):
        async def decorator(ctx, *args, **kwargs):
            if ctx.author.id in self.moderators:
                await func(ctx, *args, **kwargs)
        return decorator



    #################
    # Bot functions #
    #################
    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name="with fire"))
        print("Awww shii--")
        self.schedule.start()


    async def on_message(self, message):
        if message.author.id in self.banned:
            return
        await bot.process_commands(message)


    def add_commands(self):
        @self.command(name = "search", aliases=['s'], pass_context=True)
        async def cmd_search(ctx, term: str):
            await ctx.send(embed = search_songs(term))

        @self.command(name = "random", aliases=['r', 'rand'], pass_context=True)
        async def cmd_random(ctx):
            await ctx.send(embed = random_song())

        @self.command(name = "sotd", aliases=['songoftheday'])
        async def cmd_sotd(ctx):
            await ctx.send(embed = get_sotd())

        @self.command(name = "link", aliases=['web', 'home', 'homepage', 'about'])
        async def cmd_about(ctx):
            await ctx.send(embed = get_website())

        @self.command(name = "donate", aliases=['sponsor', 'support'])
        async def cmd_donate(ctx):
            await ctx.send(embed = forms.embed_donate())

        @self.command(name = "config", aliases=['set', 'conf'])
        @self.moderator
        async def cmd_config(ctx, setting: str, value: str):
            await ctx.send(set_setting(setting, value))

        @self.command(name = "settings")
        @self.moderator
        async def cmd_settings(ctx):
            await ctx.send(embed = get_current_settings())

        # Errors
        @cmd_config.error
        async def cmd_config_error(ctx, error):
            print(error)
            await ctx.send(f"Usage: {self.prefix}set <key> <value>")


if __name__ == "__main__":
    bot = TJADB_Bot(command_prefix="~", self_bot=False)
    bot.run( Configuration().discord_bot_key )
