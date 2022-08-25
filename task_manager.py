import asyncio
import aioschedule as schedule
import time
from threading import Thread
from aiogram import Bot
from bot import bot



class TaskManagerThread(Thread):
    Bot.set_current(bot)
    def __init__(self, message,):
        super(TaskManagerThread, self).__init__()
        self.message = message

        # self.func = func
        # self.url = url
        # self.count = count_pages
        # self.page_list = pages_list
        #Thread.__init__(self)

    async def job(self, message):
        await message.answer("Testing scheduler")

    async def start_sched(self):
        schedule.every(2).seconds.do(job, self.message)
        await self.message.answer("Start tracking")
        i = 0
        while True:
            await schedule.run_pending()
            await asyncio.sleep(1)
            if (i == 10):
                schedule.cancel_job(job)
                return
            i += 1

    def run(self):
        asyncio.run(self.start_sched())

async def job(message='stuff', n=1):
    print("Asynchronous invocation (%s) of I'm working on:" % n, message)

schedule.every(1).seconds.do(job, n=2)

async def start_mgmt():
    while True:
        await schedule.run_pending()

async def main():
    task = asyncio.create_task(start_mgmt())
    await task

if __name__ == '__main__':
    asyncio.run(main())

    # loop = asyncio.get_event_loop()
    # while True:
    #     loop.run_until_complete(schedule.run_pending())
    #     time.sleep(0.1)