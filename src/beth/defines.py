import os
from dotenv import load_dotenv

load_dotenv()

CHANNEL = "scheduling"
CMD_CHANNEL = "bot-commands"
COMMAND_PREFIX = "/"

TOKEN = os.getenv("TOKEN")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

DEFAULT_LOCATION = "Nostalgia CafÃ©"
DEFAULT_START_TIME = "6pm - 6:30pm"
NUM_DAYS = 7

emoji_letters = [
    "ð¦",
    "ð§",
    "ð¨",
    "ð©",
    "ðª",
    "ð«",
    "ð¬",
    "ð­",
    "ð®",
    "ð¯",
    "ð°",
    "ð±",
    "ð²",
    "ð³",
    "ð´",
    "ðµ",
    "ð¶",
    "ð·",
    "ð¸",
    "ð¹",
    "ðº",
    "ð»",
    "ð¼",
    "ð½",
    "ð¾",
    "ð¿",
]

emoji_numbers = [
    "1ï¸â£",
    "2ï¸â£",
    "3ï¸â£",
    "4ï¸â£",
    "5ï¸â£",
    "6ï¸â£",
    "7ï¸â£",
    "8ï¸â£",
    "9ï¸â£",
    "0ï¸â£",
]
