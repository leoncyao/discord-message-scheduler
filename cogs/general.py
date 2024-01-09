"""
general.py

A collection of general commands.
"""
from __future__ import annotations

import random
import logging
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

        class MyView(discord.ui.View):
            # async def on_timeout(self):
                # await self.message.edit(content='Button interaction timeout.')

            def __init__(self, buttons_data):
                super().__init__()
                self.buttons_data = buttons_data
                self.generate_buttons()

            def generate_buttons(self):
                sorted_button_data = sorted(self.buttons_data, key=lambda x : x['label'])
                for button_data in sorted_button_data:
                    # logger.debug(f"{button_data['label']}")
                    button = discord.ui.Button(style=discord.ButtonStyle.primary, label=button_data['label'])
                    button.callback = self.button_callback
                    button.callback.__annotations__['button'] = discord.ui.Button

                    self.add_item(button)

            async def button_callback(self, interaction):
                
                f = open('data/test.json', 'r')
                asdf = json.load(f)
                target_child = None
                # target_id = button.data['custom_id']


                # Super ghetto, couldn't figure out how to pass in the interaction, 
                # so just looked for button inside view.children with the custom_id
                # there has to be a better way, but perfect is the anthesis of better
                for child in self.children:
                    # child_id = child.custom_id
                    if child.custom_id == interaction.data['custom_id']:
                        target_child = child
                        break
                asdf[target_child.label].append(datetime.datetime.today().isoformat())

                outfile = open('data/test_copy.json', 'w')
                json.dump(asdf, outfile, indent=4)
                outfile.close()
                shutil.copyfile("data/test_copy.json", "data/test.json")

                await interaction.response.send_message(f'Button clicked! test')

        # logger.debug(os.getcwd())
        f = open('data/test.json')
        task_data = json.load(f)
        f.close()

        my_str = "data/Days_since: \n"
        tasks = list(task_data.keys())
        days_since_values = []

        buttons_data = []
        for i in range(len(tasks)):
            task = tasks[i]       
            days_for_task = task_data[task]
            if len(days_for_task) > 0:
                most_recent = parser.parse(days_for_task[-1])
                days_since_values.append(str((datetime.datetime.today() - most_recent).days))
            else:
                days_since_values.append("0")
            buttons_data.append({'label': task, 'days_since_value': days_since_values[-1]})

        view = MyView(buttons_data)

        df = pd.DataFrame({'Task Names' : tasks, 'Days Since' : days_since_values})

        my_str = "```" + tabulate.tabulate(df, headers='keys', tablefmt='psql') + "```"

        # logger.debug(my_str)

        # sent_message = await channel.send(my_str)
        # await channel.send(view=view)
        await ctx.send(my_str)
        await ctx.send(view=view)




async def setup(bot: Bot) -> None:
    await bot.add_cog(General(bot))
