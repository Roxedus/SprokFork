import discord
from discord.ext import commands
from bot import BotSetup
import random
import dataIO


class Sniffer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    """Listen to words."""

    async def msg_sniffer(self, message):
        big = False
        status = BotSetup.settings["playing"]
        word_list = BotSetup.bad_words.keys()
        f_bad_words = []
        s_bad_words = ""
        rate = 50  # %av 100
        desc = ""
        embed = discord.Embed(title="Melding fra språkrådet", colour=message.author.colour)

        # Generate bad words
        big = message.guild.large

        try:
            rate = BotSetup.settings["rate"][str(message.guild.id)]
        except KeyError:
            pass
        if message.author.bot:
            return
        elif str(message.author.id) == "249588134021562368":
            pass
        elif int(random.randint(0, 100)) >= int(rate):
            return

        elif str(message.channel.id) in BotSetup.settings["channel_blacklist"]:
            return

        for word in word_list:
            if word in message.content.split(" ") and word not in f_bad_words:
                if big and word not in BotSetup.settings["bigserver_whitelist"]:
                    f_bad_words.append(word)
                if not big and word not in BotSetup.settings["smallserver_whitelist"]:
                    f_bad_words.append(word)

        # Detect length of bad words
        if len(f_bad_words) == 0:
            return
        elif len(f_bad_words) == 1:
            index_bad_words = f_bad_words[0]
            desc = f"Du brukte ordet '{index_bad_words}'. Dette er et lånord, og bør erstattes med et av følgende " \
                f"gode norske alternativer: \n {BotSetup.bad_words[index_bad_words]}"
        elif len(f_bad_words) > 1:
            for i_word in f_bad_words:
                s_bad_words += f"{i_word}, "
                embed.add_field(name=f"**{i_word}**", value=BotSetup.bad_words[i_word])
            desc = f"Du brukte flere ord **'{s_bad_words[:-2]}'**. Disse er lånord, og bør erstattes med et av " \
                f"følgende gode norske alternativer:"
        else:
            return

        # Counting
        BotSetup.settings["counter"] += len(f_bad_words)
        new_pres = f"{status}, funnet {BotSetup.settings['counter']}"
        await self.bot.change_presence(activity=discord.Activity(type=3, name=new_pres), status=discord.Status.online)
        self.save_json()

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

    def save_json(self):
        dataIO.js.dump(BotSetup.settings, "data/conf.json", overwrite=True, indent_format=True,
                       enable_verbose=False)


def setup(bot):
    n = Sniffer(bot)
    bot.add_listener(n.msg_sniffer, "on_message")
    bot.add_cog(n)
