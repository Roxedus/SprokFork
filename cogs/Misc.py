# Discord Packages
import discord
from discord.ext import commands
from discord.utils import escape_mentions

import platform
import time

# Bot Utilities
from cogs.utils import Bot_version


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.repo = "https://github.com/Roxedus/SprokFork"

    def get_uptime(self):
        now = time.time()
        diff = int(now - self.bot.uptime)
        days, remainder = divmod(diff, 24 * 60 * 60)
        hours, remainder = divmod(remainder, 60 * 60)
        minutes, seconds = divmod(remainder, 60)
        return days, hours, minutes, seconds

    @commands.command(name='ping', hidden=True)
    async def _ping(self, ctx):
        start = time.perf_counter()
        message = await ctx.send('Ping...')
        end = time.perf_counter()
        duration = int((end - start) * 1000)
        edit = f'Pong!\nPing: {duration}ms' \
            + f' | websocket: {int(self.bot.latency * 1000)}ms'
        await message.edit(content=edit)

    @commands.command(name='oppetid', aliases=["uptime"], hidden=True)
    async def _uptime(self, ctx):
        days, hours, minutes, seconds = self.get_uptime()
        await ctx.send(f'{days}d {hours}h {minutes}m {seconds}s')

    @commands.command(name='servere', aliases=["guilds"], hidden=True)
    @commands.is_owner()
    async def _guilds(self, ctx):
        guilds = f"{self.bot.user.name} is in:\n"
        for guild in self.bot.guilds:
            guilds += f"{guild.name}\n"
        await ctx.send(guilds)

    @commands.command()
    async def klag(self, ctx, *, klage):
        try:
            webhook_chan = self.bot.get_channel(int(ctx.bot.settings["complaints"]))
            try:
                avatar_url = ctx.author.avatar_url_as(format="gif", size=1024)
            except:
                avatar_url = ctx.author.avatar_url_as(format="png", size=1024)
            whook_id = await webhook_chan.create_webhook(name=ctx.author.name, avatar=await avatar_url.read(),
                                                        reason="Klage")
            embed = discord.Embed(title='Klage mottat', description=escape_mentions(klage), color=ctx.author.color)
            embed.set_footer(text=f'sent av {ctx.author.name}', icon_url=avatar_url)
            if not isinstance(ctx.message.channel, discord.DMChannel):
                embed.add_field(name='Melding', value=f'[Hopp!]({ctx.message.jump_url})', inline=False)
            await whook_id.send(embed=embed)
            await whook_id.delete()
        except KeyError:
            pass

    @commands.command()
    async def info(self, ctx):
        """
        Lister info om botten, og serverrelaterte instillinger
        """
        membercount = []
        for guild in self.bot.guilds:
            for member in guild.members:
                if member.id in membercount:
                    pass
                else:
                    membercount.append(member.id)

        dev = await self.bot.fetch_user(self.bot.settings["owner"])

        desc = f"Discord-programvareagent som reagerer på bruken av " \
               f"[lånord](https://www.sprakradet.no/sprakhjelp/Skriverad/Avloeysarord/), " \
               f"og forslår norske alternativer. " \
               f"Forbedringforslag mottas på [GitHub]({self.repo})"

        py_ver = platform.python_version()
        how = f"**Python-versjon:** " \
              f"[{py_ver}](https://python.org/downloads/release/python-{py_ver.replace('.', '')}/)" \
              f"\n**Discord.py-versjon:** " \
              f"[{discord.__version__}](https://github.com/Rapptz/discord.py/releases/tag/v{discord.__version__}/)" \
              f"\n**SprokFork-versjon:** {Bot_version.bot_version}"

        guilds = len(self.bot.guilds)
        members = len(membercount)
        days, hours, minutes, seconds = self.get_uptime()
        avatar = self.bot.user.avatar_url_as(format=None, static_format='png', size=1024)

        uptimetext = f'{days}d {hours}t {minutes}m {seconds}s'
        embed = discord.Embed(color=discord.Colour.from_rgb(245, 151, 47), description=desc)
        embed.set_author(name=dev.name, icon_url=dev.avatar_url)
        embed.set_thumbnail(url=avatar)

        embed.add_field(name="Tjenere", value=str(guilds))

        embed.add_field(name="Ord i listen", value=str(len(self.bot.bad_words)))
        try:
            embed.add_field(name="Rate på denne serveren", value=self.bot.settings["rate"][str(ctx.guild.id)])
        except KeyError:
            embed.add_field(name="Rate på denne serveren", value="50")

        embed.add_field(name="Hvor mange?", value=f'Retter på {members} brukere')
        embed.add_field(name="Oppetid", value=uptimetext)
        embed.add_field(name="Hvordan?", value=how, inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))
