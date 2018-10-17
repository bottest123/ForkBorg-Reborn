from __future__ import unicode_literals
from pathlib import Path
from telethon import TelegramClient, events
from config import *
from set_variables import *

import logging

bot = TelegramClient('userbot',API_ID,API_HASH)
bot.start()
