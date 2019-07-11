import discord


def s_embed(self, ctx, big_embed: bool = False):
    avatar = self.bot.user.avatar_url_as(format=None, static_format='png', size=1024)
    embed = discord.Embed(color=discord.Colour.from_rgb(245, 151, 47))
    embed.set_author(name=self.bot.user.name, icon_url=avatar)
    embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
    if big_embed:
        embed.set_thumbnail(url=avatar)
    return embed
