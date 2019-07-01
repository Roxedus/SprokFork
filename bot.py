import os
import time
from dataIO import js
import discord
from discord.ext import commands
import asyncio

from tools import GetList


basic_conf = {"token": "Token", "prefix": ["!"], "playing": "Sier morn"}


class BotSetup:
    start_time = time.time()
    settings = js.load("data/conf.json")
    bad_words = dict(GetList.List.dict_to_json())
    default_settings = {}

    def check_folders():
        folders = ["cogs", "data"]
        for folder in folders:
            if not os.path.exists(folder):
                print(f"Creating {folder} folder...")
                os.makedirs(folder)

    def check_files():
        f = "data/conf.json"
        if not js.is_json_file(f):
            print("Creating conf.json...")
            js.dump(basic_conf, f)
        else:  # consistency check
            current = js.load(f)
            js.dump(current, f, overwrite=True, indent_format=True)


def bot_start():
    try:
        token = BotSetup.settings["token"]
        prefix = BotSetup.settings["prefix"]
        status = BotSetup.settings["playing"]
    except KeyError:
        print("Config not valid")
        raise SystemExit(0)

    bot = commands.Bot(command_prefix=prefix, prefix=prefix)

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
