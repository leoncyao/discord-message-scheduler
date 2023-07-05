"""
start.py

Entrypoint for the bot.
"""
from __future__ import annotations

import asyncio
import logging
import sys
import json
from src.bot import Bot
import datetime

import shutil

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    bot = Bot()


    @bot.event
    async def on_reaction_add(reaction, user):
        
        # logger.debug(str(user))
        # 1203 is my bot id, i dont want my bot to trigger itself by reacting
        if user.discriminator != '1203':
            f = open('test.json')
            tasks = json.load(f)
            task_names = list(tasks.keys())
            strs = list(reaction.emoji)
            logger.debug(strs)
            index = int(''.join(strs[:-1]))
            clicked_task_name = task_names[index]
            tasks[clicked_task_name].append(datetime.datetime.today().isoformat())


            with open('test_copy.json', 'w') as outfile:
                json.dump(tasks, outfile, indent=4)

            shutil.copyfile("test_copy.json", "test.json")


    async def main() -> None:
        """
        The main runner for the bot.
        """
        async with bot:
            await bot.load_extension("cogs.scheduler")
            await bot.load_extension("cogs.general")
            logger.info("[green]Starting bot.[/green]", extra={"markup": True})
            await bot.start()

    try:
        try:
            import uvloop
        except ModuleNotFoundError:
            logger.info("uvloop not installed.")
            asyncio.run(main())
        else:
            # Start event loop
            if sys.version_info >= (3, 11):
                # noinspection PyUnresolvedReferences
                with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
                    runner.run(main())
            else:
                uvloop.install()
                asyncio.run(main())
            del uvloop  # remove local variable
    except KeyboardInterrupt:
        pass
    logger.info("[red]Bot has stopped.[/red]", extra={"markup": True})
