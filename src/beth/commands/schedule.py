import discord
from discord.ext import commands
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

def find_command_args(ctx):
    cmd_name = ctx.command.name
    msg = ctx.message.content.replace(defines.COMMAND_PREFIX + cmd_name + " ", "")

    parsed_args = {}
    key = ""
    value = ""
    key_done = False
    has_quotes = False
    quote_count = 0
    quote_char = None
    skip = False

    def next_arg():
        nonlocal key, value, key_done, has_quotes, quote_char, quote_count, parsed_args

        parsed_args[key] = value
        
        if quote_char:
            parsed_args[key] = value.replace(quote_char, "")
        
        key = ""
        value = ""
        key_done = False
        quote_count = 0
        quote_char = None
        has_quotes = False
        


    for idx, i in enumerate(msg):
        if skip:
            skip = False
            continue
        
        if i == '"' or i == "'":
            quote_char = i
            has_quotes = True
            quote_count += 1
        
        if idx == len(msg) -  1 or (key_done and has_quotes and quote_count == 2) or (key_done and not has_quotes and i == " "):
            next_arg()
            skip = True
            continue

        if not key_done and i != "=" and not value:
            key += i

        elif i == "=":
            key_done = True

        elif key_done and not has_quotes and i != " ":
            value += i

        elif key_done and has_quotes and i != quote_char:
            value += i
        

    return parsed_args

async def run(ctx):
    is_staff = [i.name for i in ctx.author.roles if i.name.lower() == "staff"]
    if not is_staff and ctx.channel.name.lower() != defines.CMD_CHANNEL:
        return

    default_command_args = {
        "current_week": False
    }

    command_args = find_command_args(ctx)

    for key, value in command_args.items():
        default_command_args[key] = value
    
    channel = discord.utils.get(ctx.guild.channels, name=defines.CHANNEL)

    days = build_date_list(ctx.message.created_at, current_week=bool(default_command_args['current_week']))

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

    content_data = {
        "location": defines.DEFAULT_LOCATION,
        "start_time": defines.DEFAULT_START_TIME 
    }


    for key, value in command_args.items():
        content_data[key] = value

    content = f"""
:chess_pawn: **OTB Meet Up Poll**  @everyone 

**Location**: {content_data['location']}
**Start Time**: {content_data['start_time']}

Please react which days you can make it.
"""
    poll_message = await channel.send(
        embed=embed,
        content=content,
    )
    for i in range(len(days)):
        await poll_message.add_reaction(defines.emoji_letters[i])