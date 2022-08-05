import asyncio
import datetime
import threading
import time
import os
import urllib.parse

import aioschedule as schedule
import psycopg2

from aiogram import Bot, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

import OLX_Get_Data

connection = psycopg2.connect(
        database="users",
        user="postgres",
        password="1234",
        host="127.0.0.1",
        port="5432"
)

control_load_file = {}

async def test_print():
    print("It's test aioshedule!")

async def job(message='stuff', n=1):
    print("Asynchronous invocation (%s) of I'm working on:" % n, message)
    asyncio.sleep(1)

async def check_dict(id):
    while True:
        if control_load_file[id] == True:
            return
        await asyncio.sleep(5)

#async def create_shed_tsk():
 #   task = asyncio.create_task()

schedule.every(1).seconds.do(job)


class FSMRequest(StatesGroup):
    requested_items = State()

TOKEN = "5293509218:AAFKYC5Zk2zrerO25Vb3vueFYFPB01FZTtI"
storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

#Making the main reply keyboard
Main_Keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button_make_request = KeyboardButton("/Make_request")
button_track = KeyboardButton("/Відслідковувати потрібний товар")
button_history = KeyboardButton("/My_history")
Main_Keyboard.add(button_make_request)
Main_Keyboard.add(button_track)
Main_Keyboard.add(button_history)

Cancel_Keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button_cancel = KeyboardButton("/Cancel")
Cancel_Keyboard.add(button_cancel)

#Start handlers
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    ID = message.from_user.id
    username = message.from_user.username
    await message.answer(str(username))
    await message.answer(str(ID))
    cur = connection.cursor()
    cur.execute(
        "INSERT INTO users_data (telegram_id, telegram_username) VALUES (%s, %s)", (ID, username))
    connection.commit()
    await message.reply("Привіт! Це бот для пошуку потрібних товарів в OLX", reply_markup=Main_Keyboard)

@dp.message_handler(commands=['data'])
async def get_data(message: types.Message):
    file = open("data.csv", "rb")
    await bot.send_document(message.chat.id, file)

@dp.message_handler(commands=["Make_request"])
async def FSM_Start(message: types.Message):
    await message.reply("Відправте назву товару для пошуку", reply_markup=Cancel_Keyboard)
    await FSMRequest.requested_items.set()
   # file = open("data.csv", "rb")
   # await bot.send_document(message.chat.id, file)

@dp.message_handler(commands=["My_history"])
async def FSM_Start(message: types.Message):
    await message.reply("Зачекайте декілька секунд")
    cur = connection.cursor()
    cur.execute("SELECT * FROM users_requests Where telegram_id = %s", (message.from_user.id, ))
    rows = cur.fetchall()
    for row in rows:
        answ = str(row[4]) + " " + str(row[3])
        await message.answer(answ)

@dp.message_handler(commands=["Cancel"], state="*")
async def FSM_Start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Відміна дій", reply_markup=ReplyKeyboardRemove())
    await message.answer("Виберіть потрібну дію", reply_markup=Main_Keyboard)

@dp.message_handler(state=FSMRequest.requested_items)

async def Request(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "Making request...")
    control_load_file[message.from_user.id] = False
    now =  datetime.datetime.now()
    print(now.strftime("%d-%m-%Y %H:%M"))
    cur = connection.cursor()
    cur.execute(
        "INSERT INTO users_requests (telegram_id, telegram_username, Request, Request_time) VALUES (%s, %s, %s, %s)", (message.from_user.id, message.from_user.username, message.text, now.strftime("%d-%m-%Y %H:%M")))
    connection.commit()
    goods = str(message.text)
    goods = urllib.parse.quote(goods)
    url = 'https://www.olx.ua/d/list/q-' + goods + '/'
    num_of_pages = OLX_Get_Data.Get_Num_Pages(url)
    OLX_Get_Data.CreateFile(message.from_user.id)
    #await OLX_Get_Data.start_loop(url, page_number=num_of_pages)

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    pages = list()
    th = OLX_Get_Data.DownloadThread(OLX_Get_Data.load_data_async, url, num_of_pages)
    th.start()
    th.join()

    thread_soup = OLX_Get_Data.Parce_Thread(OLX_Get_Data.create_tsk, message, bot, dict_control=control_load_file)
    thread_soup.start()
    th.join()

    # await asyncio.sleep(12)
    await check_dict(message.from_user.id)

    #OLX_Get_Data.get_data_from_page(Pages=OLX_Get_Data.pages)
    file = open(f"data_{message.from_user.id}.csv", "rb")
    await bot.send_document(message.chat.id, file) # send an empty file, async thread continuous working
    await message.answer("Виберіть потрібну дію", reply_markup=Main_Keyboard)
    os.remove(f"data_{message.from_user.id}.csv")
    await state.finish()

@dp.message_handler()
async def echo_message(msg: types.Message):
    pass

if __name__ == "__main__":
    cur = connection.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Users_Data (ID SERIAL PRIMARY KEY, Telegram_ID bigint, Telegram_username TEXT)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Users_Requests (ID SERIAL PRIMARY KEY, Telegram_ID bigint, Telegram_username TEXT"
        ", Request TEXT, Request_time TEXT)")
    connection.commit()
    executor.start_polling(dispatcher=dp)

    # loop = asyncio.get_event_loop()
    #while True:
    #    loop.run_until_complete(schedule.run_pending())
    #asyncio.run(schedule.run_pending())
    #time.sleep(0.1)
