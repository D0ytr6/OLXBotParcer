from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

TOKEN = "5293509218:AAFKYC5Zk2zrerO25Vb3vueFYFPB01FZTtI"
storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

control_load_file = {}
user_track_inf = {}
