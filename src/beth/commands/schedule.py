import discord
from discord.ext import commands, tasks
from discord import app_commands
import datetime
from .. import defines


PERMISSION_INT = 541367626816


def next_monday(d):
    days_ahead = 7 - d.weekday()  # Next Monday
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


def build_date_list(msg_datetime, current_week=False):
    get_day = lambda i: start + datetime.timedelta(days=i)

    if current_week:
        start = next_monday(msg_datetime - datetime.timedelta(days=7))
    else:
        start = next_monday(msg_datetime)

    return [get_day(i) for i in range(defines.NUM_DAYS) if get_day(i) >= msg_datetime]


# TODO: will be used for scheduling automation still WIP
def get_next_schedule_time():
    current_start_time = datetime.datetime.now()
    days = build_date_list(current_start_time, current_week=True)
    return current_start_time
    # return days[len(days) - 1]


# START_SCHEDULE_TIME = get_next_schedule_time()
# print(f"Next schedule post: {START_SCHEDULE_TIME}")


def cog_is_bot_cmd_channel(interaction: discord.Interaction):
    return interaction.channel.name.lower() == defines.CMD_CHANNEL


def cmd_is_bot_cmd_channel(ctx: commands.Context):
    return ctx.channel.name.lower() == defines.CMD_CHANNEL


class ScheduleCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # self.schedule_otb_meeting.start()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.bot.tree.copy_global_to(guild=guild)

    # TODO: scheduling POC
    # @tasks.loop(time=START_SCHEDULE_TIME.timetz())
    # @tasks.loop(seconds=15)
    # async def schedule_otb_meeting(self):
    #     print("Sending OTB schedule post")
    # schedule_time = get_next_schedule_time()
    # self.schedule_otb_meeting.change_interval(
    #     time=datetime.time(second=1, tzinfo=datetime.timezone.utc)
    # )
    # self.schedule_otb_meeting.change_interval(seconds=1)

    # @schedule_otb_meeting.after_loop
    # async def before_schedule_otb_meeting(self):
    #     schedule_time = get_next_schedule_time()
    #     print(f"[before_loop] Next schedule post: {str(schedule_time)}")

    #     # self.schedule_otb_meeting.next_iteration = schedule_time
    #     self.schedule_otb_meeting.change_interval(time=schedule_time.time())
    #     print(self.schedule_otb_meeting.next_iteration)

    @commands.command(name="sync")
    @commands.has_any_role("Staff")
    @commands.check(cmd_is_bot_cmd_channel)
    async def sync(self, ctx) -> None:
        self.bot.tree.copy_global_to(guild=ctx.guild)
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"Synced {len(fmt)} commands to the current guild")

    @app_commands.command(
        name="schedule", description="Schedule new chess OTB meet up."
    )
    @app_commands.describe(
        location="Location of OTB meet up (Default value: Sugar House Coffee).",
        start_time="Specify start time of meetup (Default value: 6pm - 6:30pm).",
        current_week="Whether or not to calculate poll based on the current week or the following week.",
    )
    @app_commands.choices(
        current_week=[
            discord.app_commands.Choice(name="Current Week", value=True),
            discord.app_commands.Choice(name="Next Week", value=False),
        ]
    )
    @app_commands.checks.has_any_role("Staff")
    @app_commands.check(cog_is_bot_cmd_channel)
    async def schedule(
        self,
        interaction: discord.Interaction,
        current_week: discord.app_commands.Choice[int],
        location: str = defines.DEFAULT_LOCATION,
        start_time: str = defines.DEFAULT_START_TIME,
    ):
        await interaction.response.defer()

        channel = discord.utils.get(interaction.guild.channels, name=defines.CHANNEL)

        days = build_date_list(interaction.created_at, current_week=current_week.value)

        description = "\n\n".join(
            [
                f"{defines.emoji_letters[count]} - {i.strftime('**%A**, %d %b, %Y')}"
                for count, i in enumerate(days)
            ]
        )

        embed = discord.Embed(
            title="",
            description=description,
            color=0x13B3A3,
        )

        content = f"""
    :chess_pawn: **OTB Meet Up Poll** @everyone

    **Location**: {location}
    **Start Time**: {start_time}

    Please react which days you can make it.
    """
        poll_message = await channel.send(
            embed=embed,
            content=content,
        )
        for i in range(len(days)):
            await poll_message.add_reaction(defines.emoji_letters[i])

        await interaction.followup.send(
            f"Successfully created poll for the following week\n {days[0].strftime('**%A**, %d %b, %Y')} - {days[len(days) - 1].strftime('**%A**, %d %b, %Y')}",
            ephemeral=True,
        )
