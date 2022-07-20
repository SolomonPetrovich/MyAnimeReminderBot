import asyncio
from aiogram import Bot, Dispatcher
import logging
from Database.postgresql import Database
from Config import bot_config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=bot_config.TOKEN)
dp = Dispatcher(bot)
loop = asyncio.get_event_loop()

db = loop.run_until_complete(Database.create())