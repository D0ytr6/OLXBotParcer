from aiogram import types, Dispatcher
from Initialization.create_bot import bot
from Initialization.create_keyboard import Main_Keyboard, Cancel_Keyboard
from Initialization.connection_to_db import connection

#Start handlers
# @dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    ID = message.from_user.id
    username = message.from_user.username
    await message.answer(str(username))
    await message.answer(str(ID))
    cur = connection.cursor()
    cur.execute(
        "INSERT INTO telegram_base_users_data (telegram_id, telegram_username) VALUES (%s, %s)", (ID, username))
    connection.commit()
    await message.reply("Привіт! Це бот для пошуку потрібних товарів в OLX", reply_markup=Main_Keyboard)

# @dp.message_handler(commands=['data'])
async def get_data(message: types.Message):
    file = open("data.csv", "rb")
    await bot.send_document(message.chat.id, file)

# @dp.message_handler(commands=["My_history"])
async def user_history(message: types.Message):
    await message.reply("Зачекайте декілька секунд")
    cur = connection.cursor()
    cur.execute("SELECT * FROM users_requests Where telegram_id = %s", (message.from_user.id, )) #old DB
    rows = cur.fetchall()
    for row in rows:
        answ = str(row[4]) + " " + str(row[3])
        await message.answer(answ)

# @dp.message_handler()
async def echo_message(msg: types.Message):
    pass

def register_main_handlers(dp: Dispatcher):
    dp.register_message_handler(process_start_command, commands=['start'])
    dp.register_message_handler(get_data, commands=['data'])
    dp.register_message_handler(user_history, commands=['My_history'])