import discord
from discord.ext import commands
from typing import Optional
from bot import BotSetup
import dataIO


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
        Lists whitelist of this servertype
        """
        if ctx.guild.large:
            big = True
        w_list = BotSetup.settings["smallserver_whitelist"]
        if big:
            w_list = BotSetup.settings["bigserver_whitelist"]
        embed = discord.Embed(title="Ord i listen", color=ctx.author.colour, description=", ".join(w_list))
        embed.add_field(name=f"**Guild Type**", value=f"Er stor: **{big}**", inline=True)
        embed.add_field(name=f"**Lengde på liste**", value=f"{len(w_list)}", inline=True)
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @checks.is_mod()
    @commands.command()
    async def wordlist(self, ctx, word, big: Optional[bool] = False):
        """
        Adds or removes word from blacklist
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
        Adds or removes channel from blacklist
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
        Sets the rate on hits for this server. 0-100
        """
        if int(num) > 100:
            await ctx.send("Rate over 100, skipping")
            return
        BotSetup.settings["rate"][str(ctx.guild.id)] = str(num)
        self.save_json()

    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.CheckFailure):
            pass

    def save_json(self):
        dataIO.js.dump(BotSetup.settings, "data/conf.json", overwrite=True, indent_format=True,
                       enable_verbose=False)


def setup(bot):
    bot.add_cog(Sprakradet(bot))
