"""
general.py

A collection of general commands.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import json
import shutil
import discord
from discord.ext import commands

from src.commands import Cog
from src.env import COLOUR

if TYPE_CHECKING:
    from src.bot import Bot

logger = logging.getLogger(__name__)


class General(Cog):
    """A collection of general commands."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(aliases=["about"])
    async def info(self, ctx: commands.Context[Bot]) -> None:
        """Shows info about me."""
        embed = discord.Embed(
            description=f"**{self.bot.user.name}** "  # type: ignore[reportOptionalMemberAccess]
            'is a "helper" bot made by Taku.\n\n'
            "My source code can be found "
            "[here](https://github.com/Taaku18/discord-message-scheduler).",
            colour=COLOUR,
        )
        embed.set_footer(text=f"Bot version: {self.bot.version} · Please leave a star on my GitHub repo. <3")
        await ctx.send(embed=embed)

    @commands.command()
    async def add(self, ctx: commands.Context[Bot], *task_name_word_list) -> None:
        """Shows info about me."""

        f = open('test.json', 'r')
        asdf = json.load(f)
        asdf[" ".join(task_name_word_list)] = []

        outfile = open('test_copy.json', 'w')
        json.dump(asdf, outfile, indent=4)
        outfile.close()
        shutil.copyfile("test_copy.json", "test.json")

    @commands.command()
    async def reset_task(self, ctx: commands.Context[Bot], *task_name_word_list) -> None:
        """Shows info about me."""

        f = open('test.json')
        asdf = json.load(f)

        task_name = " ".join(task_name_word_list)
        
        if task_name in asdf.keys():
            logger.debug(f"RESETTING {task_name}")
            asdf[task_name] = []

            with open('test_copy.json', 'w') as outfile:
                json.dump(asdf, outfile, indent=4)

            shutil.copyfile("test_copy.json", "test.json")




async def setup(bot: Bot) -> None:
    await bot.add_cog(General(bot))
