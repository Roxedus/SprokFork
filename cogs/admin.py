# Discord Packages
import discord
from discord.ext import commands

from typing import Optional

# Bot Utilities
from cogs.utils.Defaults import s_embed, save_json


class checks:

    def is_mod():

        async def pred(ctx):
            is_owner = str(ctx.message.author.id) == str(ctx.bot.settings["owner"])
            is_admin = ctx.message.author.guild_permissions.administrator
            is_mod = ctx.message.author.guild_permissions.ban_members
            return is_admin or is_owner or is_mod

        return commands.check(pred)


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='endre')
    @checks.is_mod()
    async def _admin(self, ctx):
        """Kategori for styring av instillinger"""
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.bot.get_command('help'), ctx.command.qualified_name)

    @_admin.group(name='unntak')
    @checks.is_mod()
    async def _blacklist(self, ctx):
        """Kategori for styring av unntak"""
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.bot.get_command('help'), ctx.command.qualified_name)

    @commands.guild_only()
    @commands.command()
    async def list(self, ctx, big: Optional[bool] = False):
        """
        Lister hvilke låneord som er untatt
        """
        if ctx.guild.large:
            big = True
        w_list = self.bot.settings["smallserver_whitelist"]
        if big:
            w_list = self.bot.settings["bigserver_whitelist"]
        embed = s_embed(self, ctx, True)
        embed.title = "Untatte låneord"
        embed.description = ", ".join(w_list)
        embed.add_field(name=f"**Guild Type**", value=f"Er stor: **{big}**", inline=True)
        embed.add_field(name=f"**Lengde på liste**", value=f"{len(w_list)}", inline=True)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @_blacklist.command(name="ord")
    async def word_blacklist(self, ctx, word, big: Optional[bool] = False):
        """
        Legger til eller fjerner ord fra untakslisten
        """
        if ctx.guild.large:
            big = True
        w_list = self.bot.settings["smallserver_whitelist"]
        if big:
            w_list = self.bot.settings["bigserver_whitelist"]
        if word in w_list:
            w_list.remove(word)
            await ctx.send(f"**{word}** is already in the blacklist, removing")
        elif word not in w_list:
            await ctx.send(f"**{word}** is not in the blacklist, adding")
            w_list.append(word)
        save_json(self)

    @commands.guild_only()
    @_blacklist.command(name="kanal")
    async def channel_blacklist(self, ctx, channel: discord.TextChannel = None):
        """
        Legger til eller fjerner kanaler fra untakslisten
        """
        if channel is None:
            channel = ctx.message.channel

        c_list = self.bot.settings["channel_blacklist"]
        if str(channel.id) in str(c_list):
            c_list.remove(str(channel.id))
            await ctx.send(f"**{channel}** is already in the blacklist, removing")
        elif str(channel.id) not in str(c_list):
            await ctx.send(f"**{channel}** is not in the blacklist, adding")
            c_list.append(str(channel.id))
        save_json(self)

    @commands.guild_only()
    @_admin.command(hidden=True)
    async def rate(self, ctx, prosent):
        """
        Setter raten for hvor ofte botten skal reagere. 0-100
        """
        if int(prosent) > 100:
            await ctx.send("Rate over 100, hopper over")
            return
        elif int(prosent) < 0:
            await ctx.send("Rate under 0, hopper over")
            return
        self.bot.settings["rate"][str(ctx.guild.id)] = str(prosent)
        save_json(self)
        embed = s_embed(self, ctx)
        embed.add_field(name=f"**Rate for {ctx.guild.name}**",
                        value=self.bot.settings["rate"][str(ctx.guild.id)], inline=True)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Admin(bot))
