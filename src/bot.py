"""
bot.py

The main Bot class.
"""
from __future__ import annotations

import logging
from typing import Any

import tomli

import discord
from discord.ext import commands

from .env import *
from .help import HelpCmd

logger = logging.getLogger(__name__)


class Bot(commands.Bot):
    """
    The main class for the bot.
    """

    def __init__(self) -> None:
        # All intents excepted presence intent
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        # Set activity to "listening to [prefix]help"
        activity = discord.Activity(name=f"{PREFIX}help", type=discord.ActivityType.listening)

        super().__init__(
            command_prefix=commands.when_mentioned_or(PREFIX),
            intents=intents,
            activity=activity,
            help_command=HelpCmd(),
        )

        with open(PYPROJECT_TOML_PATH) as f:
            logger.info("Loading pyproject.toml to parse version.")
            toml_dict = tomli.loads(f.read())
        self.version: str = toml_dict["project"]["version"]
        logger.info("[bold green]Bot version: %s[/bold green]", self.version, extra={"markup": True})

    async def start(self, input_token=None, *args: Any, **kwargs: Any) -> None:
        """
        Start the bot using the TOKEN env.
        """

        # CHANGE BOT TOKEN HERE IN COMMAND LINE ARGUMENTS

        if input_token:
            logger.debug(f"USING input token: {input_token}")
            await super().start(input_token, *args, **kwargs)
        else:
            logger.debug(f"USING env token: {TOKEN}")
            await super().start(TOKEN, *args, **kwargs)

    async def setup_hook(self) -> None:
        """
        This is called on bot start.
        """

        if SYNC_SLASH_COMMANDS:
            logger.info("Syncing slash commands (this may take a while).")
            if not DEBUG_MODE:
                # Sync global slash commands
                await self.tree.sync()
                for guild_id in DEBUG_GUILDS:  # remove debug commands
                    await self.tree.sync(guild=discord.Object(guild_id))
                logger.info("Slash commands synced.")
            else:
                # Sync debug guilds slash commands
                for guild_id in DEBUG_GUILDS:
                    self.tree.copy_global_to(guild=discord.Object(guild_id))
                    await self.tree.sync(guild=discord.Object(guild_id))
                    logger.info("Synced app command tree to debug guild %d.", guild_id)
        else:
            logger.info("Slash commands sync skipped.")

    # noinspection PyMethodMayBeStatic
    async def on_ready(self) -> None:
        """
        This is called when the bot is ready.
        """
        logger.info("[bold green]Bot is ready.[/bold green]", extra={"markup": True})

        # logger.info("test" + str(bot.guilds))    
        # logger.info("test" + str(self.guilds[0]))
        # logger.info(str(self.cogs))

        # 00:52:48,846 [INFO] Text Channels                                                                           bot.py:101
        # 00:52:48,847 [INFO] 1113650739160555580                                                                     bot.py:102
        # 00:52:48,849 [INFO] Voice Channels                                                                          bot.py:101
        # 00:52:48,850 [INFO] 1113650739160555581                                                                     bot.py:102
        # 00:52:48,851 [INFO] general                                                                                 bot.py:101
        # 00:52:48,853 [INFO] 1113650739160555582                                                                     bot.py:102
        # 00:52:48,854 [INFO] General                                                                                 bot.py:101
        # 00:52:48,855 [INFO] 1113650739160555583                                                                     bot.py:102
        # 00:52:48,857 [INFO] thoughts                                                                                bot.py:101
        # 00:52:48,858 [INFO] 1135520426689298512                                                                     bot.py:102
        # 00:52:48,859 [INFO] quotes-i-like                                                                           bot.py:101
        # 00:52:48,861 [INFO] 1135559338992353330                                                                     bot.py:102
        # 00:52:48,862 [INFO] 中文                                                                                    bot.py:101
        # 00:52:48,863 [INFO] 1149414854294253628                                                                     bot.py:102
        # 00:52:48,864 [INFO] jokes                                                                                   bot.py:101
        # 00:52:48,866 [INFO] 1166713661235146772                                                                     bot.py:102
        # 00:52:48,867 [INFO] workout                                                                                 bot.py:101
        # 00:52:48,869 [INFO] 1176571392251142154                                                                     bot.py:102
        # 00:52:48,870 [INFO] busking                                                                                 bot.py:101
        # 00:52:48,871 [INFO] 1183539342510137444  

        Mind = self.guilds[0]
        leon = Mind.get_member(184164823725113344)
        # channel = Mind.channels[0]
        channels = Mind.channels 
        # for channel in channels:
        #     logger.info(channel)
        #     logger.info(channel.id)

        channel = Mind.get_channel(1113650739160555582)
            
        # logger.info(channels)

        scheduler = self.cogs['Scheduler']

        await scheduler.first_message(leon, channel)

    _TYPE_CLEAN_NAME: dict[str, str] = {
        discord.TextChannel.__name__: "text channel",
        discord.VoiceChannel.__name__: "voice channel",
        discord.Thread.__name__: "thread",
        discord.DMChannel.__name__: "DM channel",
        discord.GroupChannel.__name__: "group DM channel",
        discord.CategoryChannel.__name__: "category",
        discord.ForumChannel.__name__: "forum",
        discord.StageChannel.__name__: "stage channel",
        int.__name__: "number",
    }

    @classmethod
    def _get_name(cls, x: Any) -> str:
        try:
            name = x.__name__
        except AttributeError:
            if hasattr(x, "__origin__"):
                name = repr(x)
            else:
                name = x.__class__.__name__
        return cls._TYPE_CLEAN_NAME.get(name, name)

    async def on_command_error(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        context: commands.Context[Bot],
        exception: commands.CommandError,
        /,
    ) -> None:
        """
        This is called when a command raises a command-related error.

        :param context: The command context.
        :param exception: The raised exception.
        """
        # Failed to convert an argument to a union of types
        if isinstance(exception, commands.BadUnionArgument):
            ephemeral = context.interaction is not None  # ephemeral when slash command

            to_string = [self._get_name(x) for x in exception.converters]
            if len(to_string) > 2:
                fmt = "{}, or {}".format(", ".join(to_string[:-1]), to_string[-1])
            else:
                fmt = " or ".join(to_string)
            arg = discord.utils.escape_markdown(context.current_argument or "", ignore_links=False)
            embed = discord.Embed(description=f"**{arg}** is not a valid {fmt}.", colour=COLOUR)
            await context.reply(embed=embed, ephemeral=ephemeral)
        else:
            await super().on_command_error(context, exception)
