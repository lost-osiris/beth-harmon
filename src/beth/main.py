import discord
from discord.ext import commands
from . import defines
from . import commands as beth_commands


intents = discord.Intents.default()
bot = commands.Bot(command_prefix=defines.COMMAND_PREFIX, intents=intents)

def main():
    @bot.command(name="schedule")
    async def cmd(ctx):
        await beth_commands.schedule.run(ctx)

    bot.run(defines.TOKEN)