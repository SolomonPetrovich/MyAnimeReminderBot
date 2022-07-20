from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Bot.bot import dp, db
from aiogram import types
import json


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет {0.full_name}'.format(message.from_user) + ', я буду уведомлять вас о новых сериях '
                                                                            'аниме, чтобы получать уведомление, '
                                                                            'пожалуйста подпишитесь /subscribe')


@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    data = json.load(open('chapters.json'))
    episode = data[0]
    if not db.subscriber_exists(message.from_user.id):
        await db.sql_add_user(message.from_user.id, True)
        await message.answer('Вы успешно подписались☺')
        await dp.bot.send_message(f"Вышла {episode['title'][18:22]} "
                                  f"серия аниме {episode['title'][0:18]} "
                                  f"смотреть можно по ссылке ниже\n"
                                  f"{episode['link']}",
                                  reply_markup=InlineKeyboardMarkup(
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(text="смотреть", url=episode['link'],
                                                                   callback_data="watch")
                                          ]
                                      ]
                                  )
                                  )
    else:
        await message.answer('Вы и так подписаны🤨')


@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        await message.answer('Вы и так не подписаны😒')
    else:
        await db.sql_update_status(message.from_user.id, False)
        await message.answer('Вы успешно отписались☹')
