import requests
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bs4 import BeautifulSoup
import json

from Bot.bot import db, dp
from Config import parse_config


def get_html(url, params=None):
    r = requests.get(url, headers=parse_config.HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_="short-btn black video the_hildi")

    chapters = [{
        'title': items[-1].get_text(),
        'link': parse_config.HOST + items[-1]['href']
    }]
    return chapters


def saver(items, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for item in items:
            json.dump(item, file, indent=4, ensure_ascii=False)


def compare(items, filename):
    data = json.load(open(filename))
    if items[0][0] == data[0]:
        return True
    else:
        return False


async def check():
    chapters = []
    html = get_html(parse_config.URL)
    if html.status_code == 200:
        chapters.append(get_content(html.text))
        episode = chapters[0][0]
        users = await db.sql_get_user()
        if not compare(chapters, parse_config.FILE):
            for user in users:
                await dp.bot.send_message(user[0], f"Вышла {episode['title'][18:22]} "
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
            saver(chapters, parse_config.FILE)
    else:
        print('Error')
