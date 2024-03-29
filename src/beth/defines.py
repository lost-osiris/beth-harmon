import os
from dotenv import load_dotenv

load_dotenv()

CHANNEL = os.getenv("DEV_CHANNEL", "scheduling")
CMD_CHANNEL = os.getenv("DEV_CHANNEL", "bot-commands")

COMMAND_PREFIX = "/"

TOKEN = os.getenv("TOKEN")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

DEFAULT_LOCATION = "Sugar House Coffee"
DEFAULT_START_TIME = "6pm - 6:30pm"
NUM_DAYS = 7

emoji_letters = [
    "🇦",
    "🇧",
    "🇨",
    "🇩",
    "🇪",
    "🇫",
    "🇬",
    "🇭",
    "🇮",
    "🇯",
    "🇰",
    "🇱",
    "🇲",
    "🇳",
    "🇴",
    "🇵",
    "🇶",
    "🇷",
    "🇸",
    "🇹",
    "🇺",
    "🇻",
    "🇼",
    "🇽",
    "🇾",
    "🇿",
]

emoji_numbers = [
    "1️⃣",
    "2️⃣",
    "3️⃣",
    "4️⃣",
    "5️⃣",
    "6️⃣",
    "7️⃣",
    "8️⃣",
    "9️⃣",
    "0️⃣",
]
