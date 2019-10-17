# Discord Packages
import discord
from discord.ext import commands

import asyncio
import os
import time

from dataIO import js

# Bot Utilities
from tools import GetWords

basic_conf = {"token": "Token", "prefix": ["!"], "playing": "Teller"}

extra_bad_words = {'cringe': 'kringle', 'boomer': 'sprenger', '#unbanzibon': 'nei'}
extra_short_words = {'rph': 'Rister på hodet', 'fåvæ': 'For å være ærlig'}


class BotSetup:
    start_time = time.time()
    settings = js.load("data/conf.json", enable_verbose=False)
    bad_words = dict(GetWords.List.dict_to_json("https://www.sprakradet.no/sprakhjelp/Skriverad/Avloeysarord/"))
    bad_words.update(extra_bad_words)
    short_words = dict(GetWords.List.dict_to_json("https://www.sprakradet.no/sprakhjelp/Skriveregler/Forkortinger/"))
    short_words.update(extra_short_words)
    default_settings = {}

    @staticmethod
    def check_folders():
        folders = ["cogs", "data"]
        for folder in folders:
            if not os.path.exists(folder):
                print(f"Creating {folder} folder...")
                os.makedirs(folder)

    @staticmethod
    def check_files():
        f = "data/conf.json"
        if not js.is_json_file(f):
            print("Creating conf.json...")
            js.dump(basic_conf, f, enable_verbose=False)
        else:  # consistency check
            current = js.load(f)
            js.dump(current, f, overwrite=True, indent_format=True, enable_verbose=False)


def bot_start():
    try:
        token = BotSetup.settings["token"]
        prefix = BotSetup.settings["prefix"]
        status = BotSetup.settings["playing"]
    except KeyError:
        print("Config not valid")
        raise SystemExit(0)

    bot = commands.Bot(command_prefix=prefix, prefix=prefix)

    bot.short_words = BotSetup.short_words
    bot.bad_words = BotSetup.bad_words
    bot.settings = BotSetup.settings

    print("Logging in")

    cog_list = ""
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            name = file[:-3]
            cog_list += f"Loaded: {name}\n"
            bot.load_extension(f"cogs.{name}")

    @bot.event
    async def wait_until_ready_():
        await bot.wait_until_ready()
        print("Ready")

    @bot.event
    async def on_ready():
        if not hasattr(bot, 'appinfo'):
            bot.appinfo = await bot.application_info()
        print(discord.Client.is_ready(bot))
        print(cog_list)
        print(f'\nLogged in as: {bot.user.name} in {len(bot.guilds)} servers.')
        print(f'Version: {discord.__version__}\n')
        await bot.change_presence(activity=discord.Activity(type=3, name=status), status=discord.Status.online)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(bot.start(token, bot=True, reconnect=True))
    except KeyboardInterrupt:
        loop.run_until_complete(bot.logout())
        # cancel all tasks lingering
    finally:
        loop.close()


if __name__ == "__main__":
    BotSetup.check_files()
    BotSetup.check_folders()
    bot_start()
