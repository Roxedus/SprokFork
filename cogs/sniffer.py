# Discord Packages
import discord
from discord.ext import commands

import asyncio
import random

# Bot Utilities
from cogs.utils.Defaults import save_json


class Sniffer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.presence())
    """Søker etter ord"""

    async def msg_sniffer(self, message):
        big = False
        rate = 50  # %av 100
        try:
            big = message.guild.large
        except AttributeError:
            pass
        try:
            rate = self.bot.settings["rate"][str(message.guild.id)]
        except KeyError:
            pass
        except AttributeError:
            pass
        if message.author.bot:
            return
        elif str(message.author.id) == "249588134021562368":
            pass
        elif int(random.randint(0, 100)) >= int(rate):
            return
        elif str(message.channel.id) in self.bot.settings["channel_blacklist"]:
            return

        await self.create_msg(message, big)

    async def create_msg(self, message, big):
        """Generate bad words"""
        word_list = self.bot.bad_words.keys()
        f_bad_words = []
        s_bad_words = ""
        desc = ""
        embed = discord.Embed(title="Melding fra språkrådet", color=discord.Colour.from_rgb(245, 151, 47))

        for word in word_list:
            if word in message.content.split(" ") and word not in f_bad_words:
                if big and word not in self.bot.settings["bigserver_whitelist"]:
                    f_bad_words.append(word)
                if not big and word not in self.bot.settings["smallserver_whitelist"]:
                    f_bad_words.append(word)

        # Detect length of bad words
        if len(f_bad_words) == 0:
            return
        elif len(f_bad_words) == 1:
            index_bad_words = f_bad_words[0]
            desc = f"Du brukte ordet `{index_bad_words}`. Dette er et lånord, og bør erstattes med et av følgende " \
                f"gode norske alternativer: \n {self.bot.bad_words[index_bad_words]}"
        elif len(f_bad_words) > 1:
            for i_word in f_bad_words:
                s_bad_words += f"{i_word}, "
                embed.add_field(name=f"**{i_word}**", value=self.bot.bad_words[i_word])
            desc = f"Du brukte flere ord **`{s_bad_words[:-2]}`**. Disse er lånord, og bør erstattes med et av " \
                f"følgende gode norske alternativer:"
        else:
            return

        # Counting
        self.bot.settings["counter"] += len(f_bad_words)
        save_json(self)

        # Finishing, and sending embed element
        embed.description = desc
        foot = f"Takk for at du lærer, {message.author}"
        embed.set_footer(text=foot, icon_url=message.author.avatar_url)
        try:
            print(f"Sent message to {message.author}")
            await message.author.send(embed=embed)
        except discord.errors.Forbidden:
            print(f"Sent in {message.channel} for {message.author}")
            msg = f"Du har blokkert meg fra å sende deg meldinger, {message.author.mention}"
            await message.channel.send(content=msg, embed=embed)
        await message.channel.send(embed=embed)

    async def presence(self):
        await self.bot.wait_until_ready()
        while True:
            new_pres = f"{self.bot.settings['playing']}, funnet {self.bot.settings['counter']}"
            await self.bot.change_presence(activity=discord.Activity(type=3, name=new_pres),
                                           status=discord.Status.online)
            await asyncio.sleep(10)

    async def stupid(self):
        return await self.presence()


def setup(bot):
    n = Sniffer(bot)
    bot.add_listener(n.msg_sniffer, "on_message")
    bot.add_cog(n)
