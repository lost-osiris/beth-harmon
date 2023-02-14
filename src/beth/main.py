import discord
from discord.ext import commands
from . import defines
from . import commands as beth_commands

import logging

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
discord.utils.setup_logging(level=logging.DEBUG, handler=handler, root=False)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=defines.COMMAND_PREFIX, intents=intents)

def main():
    @bot.command(name="schedule")
    async def cmd(ctx):
        await beth_commands.schedule.run(ctx)

    bot.run(defines.TOKEN)