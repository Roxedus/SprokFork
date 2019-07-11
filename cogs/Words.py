import discord
from discord.ext import commands
import aiohttp

from cogs.utils.Defaults import s_embed


class Oppslag(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    @commands.command()
    async def prep(self, ctx, plass):
        """
        Bruker https://github.com/draperunner/preposisjon for å finne preosisjon.
        """
        async with self.session.get(f"https://preposisjon.no/api?place={plass}", timeout=30) as response:
            assert response.status == 200
            p = await response.json()
            embed = s_embed(self, ctx)
            embed.description = f"Du er {p['preposisjon']} {plass.title()}"
            await ctx.send(embed=embed)

    @commands.command(aliases=["forkort", "kort"])
    async def forkortelse(self, ctx, kort_ord):
        """
        Svarer med Språkrådets(og serverens) definasjon av kort_ord
        https://www.sprakradet.no/sprakhjelp/Skriveregler/Forkortinger/
        """
        word_list = self.bot.short_words
        try:
            desc = f"Språkrådet definerte `{kort_ord}` som `{word_list[kort_ord]}`"
        except KeyError:
            desc = "Ingen definisjon funnet (saksfølsom)"
        embed = s_embed(self, ctx)
        embed.description = desc
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Oppslag(bot))
