from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import OLX_Get_Data
import urllib.parse

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
button_history = KeyboardButton("/Історія моїх запитів")
Main_Keyboard.add(button_make_request)
Main_Keyboard.add(button_track)
Main_Keyboard.add(button_history)


Cancel_Keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button_cancel = KeyboardButton("/Cancel")
Cancel_Keyboard.add(button_cancel)

#Start handlers
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.message):
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

@dp.message_handler(commands=["Cancel"], state="*")
async def FSM_Start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Відміна дій", reply_markup=ReplyKeyboardRemove())
    await message.answer("Виберіть потрібну дію", reply_markup=Main_Keyboard)

@dp.message_handler(state=FSMRequest.requested_items)
async def Request(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "Making request...")
    goods = str(message.text)
    goods = urllib.parse.quote(goods)
    url = 'https://www.olx.ua/d/list/q-' + goods + '/'
    num_of_pages = OLX_Get_Data.Get_Num_Pages(url)
    OLX_Get_Data.CrateFile()
    OLX_Get_Data.GetFromPages(num_of_pages, url)
    file = open("data.csv", "rb")
    await bot.send_document(message.chat.id, file)
    await message.answer("Виберіть потрібну дію", reply_markup=Main_Keyboard)
    await state.finish()

@dp.message_handler()
async def echo_message(msg: types.Message):

    pass

if __name__ == "__main__":
    executor.start_polling(dispatcher=dp)
