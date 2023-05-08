import discord
from discord.ext import commands
from . import defines
from . import commands as beth_commands
from beth.commands.schedule import ScheduleCog
import logging

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
discord.utils.setup_logging(level=logging.DEBUG, handler=handler, root=False)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=defines.COMMAND_PREFIX, intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    await bot.add_cog(ScheduleCog(bot))


def main():
    bot.run(defines.TOKEN)
