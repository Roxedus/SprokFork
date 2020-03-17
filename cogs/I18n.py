# Discord Packages
from discord.ext import commands


class MyHelpCommand(commands.DefaultHelpCommand):
    def get_ending_note(self):
        """Has been overridden for i18n purposes."""
        command_name = self.invoked_with
        return "Skriv {0}{1} <kommando> for mer informasjon om en kommando.\n" \
               "Du kan også skrive {0}{1} <kategori> for mer informasjon om en " \
               "kategori.".format(self.clean_prefix, command_name)

    def command_not_found(self, string):
        """Has been overridden for i18n purposes."""
        return 'Ingen kommando med navnet "{}" ble funnet.'.format(string)

    def subcommand_not_found(self, command, string):
        """Has been overridden for i18n purposes."""
        if isinstance(command, commands.Group) and len(command.all_commands) > 0:
            return 'Kommandoen "{0.qualified_name}" har ingen under-kommandoer som kalt {1}'.format(command, string)
        return 'Kommandoen "{0.qualified_name}" har ingen under-kommandoer.'.format(command)


class I18n(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        paginator = commands.Paginator(prefix='```md', suffix='```', max_size=2000)
        bot.help_command = MyHelpCommand(Cog=None, commands_heading="> Kommandoer:", no_category="\n> Ingen kategori",
                                         command_attrs={"name": "help", "help": "Viser denne meldingen"},
                                         paginator=paginator)
        bot.help_command.cog = None

    def cog_unload(self):
        self.bot.help_command = self._original_help_command


def setup(bot):
    bot.add_cog(I18n(bot))
