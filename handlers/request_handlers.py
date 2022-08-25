from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from bot_requests import standart_request
from Initialization.create_bot import dp, bot, control_load_file, user_track_inf
from Initialization.create_keyboard import Main_Keyboard, Cancel_Keyboard
from bot_requests.standart_request import create_parce_call

import aioschedule as schedule
import os

class FSMRequest(StatesGroup):
    requested_items = State()

class FSMScheduler(StatesGroup):
    requested_items = State()

async def send_in_scheduler(message: types.Message, state:FSMContext):
    if user_track_inf[message.from_user.id]:
        control_load_file[message.from_user.id] = False
        await create_parce_call(message)
        await message.answer("Виберіть потрібну дію", reply_markup=Main_Keyboard)
        os.remove(f"data_{message.from_user.id}.csv")
    else:
        await state.finish()

async def start_mgmt():
    while True:
        await schedule.run_pending()

# @dp.message_handler(commands=["Make_request"])
async def FSM_Start(message: types.Message):
    await message.reply("Відправте назву товару для пошуку", reply_markup=Cancel_Keyboard)
    await FSMRequest.requested_items.set()
   # file = open("data.csv", "rb")
   # await bot.send_document(message.chat.id, file)

# @dp.message_handler(state=FSMRequest.requested_items)
async def singl_request(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "Making request...")
    control_load_file[message.from_user.id] = False
    await standart_request.create_parce_call(message)
    await message.answer("Виберіть потрібну дію", reply_markup=Main_Keyboard)
    os.remove(f"data_{message.from_user.id}.csv")
    await state.finish()

# @dp.message_handler(commands=["Track_in_time"])
async def track_scheduler(message: types.Message):
    await message.reply("Відправте назву товару для відстежування", reply_markup=Cancel_Keyboard)
    await FSMScheduler.requested_items.set()

# @dp.message_handler(state=FSMScheduler.requested_items)
async def track(message: types.Message, state: FSMContext):
    user_track_inf[message.from_user.id] = True # Will be replaced by dp
    schedule.every(60).seconds.do(send_in_scheduler, message, state)
    await start_mgmt() # Schedule pending
    # track = task_manager.TaskManagerThread(message)
    # track.start()

# @dp.message_handler(commands=["Cancel"], state="*")
async def fsm_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Відміна дій", reply_markup=ReplyKeyboardRemove())
    await message.answer("Виберіть потрібну дію", reply_markup=Main_Keyboard)

def register_request_handlers(dp: Dispatcher):
    dp.register_message_handler(fsm_cancel, commands=["Cancel"], state="*")
    dp.register_message_handler(FSM_Start, commands=["Make_request"], state=None)
    dp.register_message_handler(singl_request, state=FSMRequest.requested_items)
    dp.register_message_handler(track_scheduler, commands=["Track_in_time"], state=None)
    dp.register_message_handler(singl_request, state=FSMRequest.requested_items)
