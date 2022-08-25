from Initialization.connection_to_db import connection
from Initialization.create_bot import dp, bot, control_load_file
from aiogram import types
from olx_scraper import request_olx, soup_olx, settings

import asyncio
import urllib
import datetime

async def check_dict(id):
    while True:
        if control_load_file[id] == True:
            return
        await asyncio.sleep(5)

async def create_parce_call(message: types.Message):
    now = datetime.datetime.now()
    print(now.strftime("%d-%m-%Y %H:%M"))
    cur = connection.cursor()
    cur.execute(
        "INSERT INTO users_requests (telegram_id, telegram_username, Request, Request_time) VALUES (%s, %s, %s, %s)",
        (message.from_user.id, message.from_user.username, message.text, now.strftime("%d-%m-%Y %H:%M")))
    connection.commit()
    goods = str(message.text)
    goods = urllib.parse.quote(goods)
    url = 'https://www.olx.ua/d/list/q-' + goods + '/'
    num_of_pages = soup_olx.Get_Num_Pages(url)
    settings.CreateFile(message.from_user.id)
    # await OLX_Get_Data.start_loop(url, page_number=num_of_pages)

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    pages = list()
    th = settings.DownloadThread(request_olx.load_data_async, url, num_of_pages, pages)
    th.start()
    th.join()

    thread_soup = settings.Parce_Thread(soup_olx.create_tsk, message, bot, dict_control=control_load_file,
                                           pages=pages)
    thread_soup.start()
    th.join()
    # await asyncio.sleep(12)
    await check_dict(message.from_user.id)
    # OLX_Get_Data.get_data_from_page(Pages=OLX_Get_Data.pages)
    file = open(f"data_{message.from_user.id}.csv", "rb")
    await bot.send_document(message.chat.id, file)  # send an empty file, async thread continuous working