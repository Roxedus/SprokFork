import discord
from discord.ext import commands
from typing import Optional
from bot import BotSetup
import dataIO

from cogs.utils.Defaults import s_embed


class checks:

    def is_mod():

        async def pred(ctx):
            is_owner = str(ctx.message.author.id) == str(BotSetup.settings["owner"])
            is_admin = ctx.message.author.guild_permissions.administrator
            return is_admin or is_owner

        return commands.check(pred)


class Sprakradet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command()
    async def list(self, ctx, big: Optional[bool] = False):
        """
        Lister hvilke låneord som er untatt
        """
        if ctx.guild.large:
            big = True
        w_list = BotSetup.settings["smallserver_whitelist"]
        if big:
            w_list = BotSetup.settings["bigserver_whitelist"]
        embed = s_embed(self, ctx, True)
        embed.title = "Untatte låneord"
        embed.description = ", ".join(w_list)
        embed.add_field(name=f"**Guild Type**", value=f"Er stor: **{big}**", inline=True)
        embed.add_field(name=f"**Lengde på liste**", value=f"{len(w_list)}", inline=True)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @checks.is_mod()
    @commands.command()
    async def wordlist(self, ctx, word, big: Optional[bool] = False):
        """
        Legger til eller fjerner ord fra untakslisten
        """
        if ctx.guild.large:
            big = True
        w_list = BotSetup.settings["smallserver_whitelist"]
        if big:
            w_list = BotSetup.settings["bigserver_whitelist"]
        if word in w_list:
            w_list.remove(word)
            await ctx.send(f"**{word}** is already in the blacklist, removing")
        elif word not in w_list:
            await ctx.send(f"**{word}** is not in the blacklist, adding")
            w_list.append(word)
        self.save_json()

    @commands.guild_only()
    @checks.is_mod()
    @commands.command()
    async def channellist(self, ctx, channel: discord.TextChannel = None):
        """
        Legger til eller fjerner kanaler fra untakslisten
        """
        if channel is None:
            channel = ctx.message.channel

        c_list = BotSetup.settings["channel_blacklist"]
        if str(channel.id) in str(c_list):
            c_list.remove(str(channel.id))
            await ctx.send(f"**{channel}** is already in the blacklist, removing")
        elif str(channel.id) not in str(c_list):
            await ctx.send(f"**{channel}** is not in the blacklist, adding")
            c_list.append(str(channel.id))
        self.save_json()

    @commands.guild_only()
    @checks.is_mod()
    @commands.command()
    async def rate(self, ctx, num):
        """
        Setter raten for hvor ofte botten skal reagere. 0-100
        """
        if int(num) > 100:
            await ctx.send("Rate over 100, hopper over")
            return
        BotSetup.settings["rate"][str(ctx.guild.id)] = str(num)
        self.save_json()

    def save_json(self):
        dataIO.js.dump(BotSetup.settings, "data/conf.json", overwrite=True, indent_format=True,
                       enable_verbose=False)


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.repo = "https://github.com/Roxedus/SprokFork"

    @commands.command()
    async def info(self, ctx):
        """
        Lister info om botten, og serverrelaterte instillinger
        """
        desc = f"Discord-programvareagent som reagerer på bruken av lånord, og forslår norske alternativer. " \
               f"Forbedringforslag mottas på [GitHub]({self.repo})"
        guilds = len(self.bot.guilds)
        avatar = self.bot.user.avatar_url_as(format=None, static_format='png', size=1024)
        embed = discord.Embed(color=discord.Colour.from_rgb(245, 151, 47), description=desc)
        embed.set_author(name=self.bot.user.name, icon_url=avatar)
        embed.set_thumbnail(url=avatar)
        embed.add_field(name="Tjenere", value=str(guilds))
        embed.add_field(name="Ord i listen", value=str(len(BotSetup.bad_words)))
        try:
            embed.add_field(name="Rate på denne serveren", value=BotSetup.settings["rate"][str(ctx.guild.id)])
        except KeyError:
            embed.add_field(name="Rate på denne serveren", value="50")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Sprakradet(bot))
    bot.add_cog(Info(bot))
