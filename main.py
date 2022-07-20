import asyncio
from Parse import parse
from aiogram import executor
from Bot.bot import dp


async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        await parse.check()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(5))
    executor.start_polling(dp, skip_updates=True)
