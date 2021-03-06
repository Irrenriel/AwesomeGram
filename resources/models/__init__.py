import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import config

from resources.tools import *


# Here you can create tool instances if you needed.

# Loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# MemoryStorage
storage = MemoryStorage()


# Bots
bot = Bot(token=config.BOT_TOKEN, loop=loop, parse_mode=config.PARSE_MODE)

# Dispatchers
dp = Dispatcher(bot, storage=storage, loop=loop)


# Comment if you no need to user PostgreSQL Database
# db = PostgreSQLDatabase(*config.POSTGRES_DB)
# db = SQLite3Database(config.SQLITE_DB_PATH)
