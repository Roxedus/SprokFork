# Discord Packages
from discord.ext import commands


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if hasattr(ctx.command, 'on_error'):
            return

        try:
            self.bot.get_command(f'{ctx.command}').reset_cooldown(ctx)
        except AttributeError:
            pass

        ignored = commands.CommandNotFound
        send_help = (commands.MissingRequiredArgument,
                     commands.TooManyArguments,
                     commands.BadArgument)

        if isinstance(error, ignored):
            return

        elif isinstance(error, send_help):
            return await ctx.send_help(ctx.command)

        elif isinstance(error, AssertionError):
            return await ctx.send("ApiFeil")

        elif isinstance(error, commands.CheckFailure):
            return


def setup(bot):
    bot.add_cog(Errors(bot))
