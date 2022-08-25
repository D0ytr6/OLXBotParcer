from aiogram import executor

from Initialization.connection_to_db import create_db_if_none
from Initialization.create_bot import dp

from handlers import main_handlers, request_handlers

if __name__ == "__main__":
    create_db_if_none()
    main_handlers.register_main_handlers(dp)
    request_handlers.register_request_handlers(dp)

    executor.start_polling(dispatcher=dp)
    #dp.loop.create_task() # You can get async loop from dp and add task to it
    # Dp create async loop and automatically make and start tasks /