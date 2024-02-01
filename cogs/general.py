"""
general.py

A collection of general commands.
"""
from __future__ import annotations

import random
import logging
import subprocess
from typing import TYPE_CHECKING

import os
import json
import shutil
import discord
from discord.ext import commands

import datetime
import pandas as pd
from dateutil import parser
import tabulate


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

        f = open('data/test.json', 'r')
        asdf = json.load(f)
        asdf[" ".join(task_name_word_list)] = [datetime.datetime.today().isoformat()]

        outfile = open('data/test_copy.json', 'w')
        json.dump(asdf, outfile, indent=4)
        outfile.close()
        shutil.copyfile("data/test_copy.json", "data/test.json")

    @commands.command()
    async def download_music(self, ctx: commands.Context[Bot], playlist_link) -> None:

        # Specify the directory path
        directory_path = '/home/leon/Desktop/music/'

        # Change the current working directory to the specified directory
        subprocess.Popen(f'sh download_music.sh {playlist_link}', cwd=directory_path, shell=True)

    @commands.command()
    async def reset_task(self, ctx: commands.Context[Bot], *task_name_word_list) -> None:
        """Shows info about me."""

        f = open('data/test.json')
        asdf = json.load(f)

        task_name = " ".join(task_name_word_list)
        
        if task_name in asdf.keys():
            logger.debug(f"RESETTING {task_name}")
            asdf[task_name] = []

            with open('data/test_copy.json', 'w') as outfile:
                json.dump(asdf, outfile, indent=4)

            shutil.copyfile("data/test_copy.json", "data/test.json")
        
        # await self.show_tasks(ctx)

    @commands.command(aliases=['青青'])
    async def get_sayings(self, ctx: commands.Context[Bot]) -> None:
        f = open('data/morning_vibes.json', 'r')
        asdf = json.load(f)
        成语 = asdf['成语']
        selection = random.choice(成语)
        await ctx.send(selection)

    @commands.command(aliases=['show'])
    async def show_tasks(self, ctx: commands.Context[Bot]) -> None:
        """Shows info about me."""

        # guild = self.bot.get_guild(event.guild_id)





async def setup(bot: Bot) -> None:
    await bot.add_cog(General(bot))
