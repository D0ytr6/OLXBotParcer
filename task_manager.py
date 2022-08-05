import asyncio
import aioschedule as schedule
import time


async def job(message='stuff', n=1):
    print("Asynchronous invocation (%s) of I'm working on:" % n, message)

schedule.every(1).seconds.do(job, n=2)

async def start_mgmt():
    while True:
        schedule.run_pending()

async def main():
    task = asyncio.create_task(start_mgmt())
    await task

if __name__ == '__main__':
    asyncio.run(main())

    # loop = asyncio.get_event_loop()
    # while True:
    #     loop.run_until_complete(schedule.run_pending())
    #     time.sleep(0.1)