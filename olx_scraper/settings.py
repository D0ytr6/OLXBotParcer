# Creating Async thread
from threading import Thread
from aiogram import types
import asyncio
import csv

class DownloadThread(Thread):
    def __init__(self, func, url, count_pages, pages_list):
        super(DownloadThread, self).__init__()
        self.func = func
        self.url = url
        self.count = count_pages
        self.page_list = pages_list
        #Thread.__init__(self)

    def run(self):
        asyncio.run(self.func(self.url, self.count, self.page_list))

class Parce_Thread(Thread):
    def __init__(self, func, message: types.Message, bot, dict_control, pages):
        super(Parce_Thread, self).__init__()
        self.func = func
        self.id = id
        self.message = message
        self.bot = bot
        self.dict_control = dict_control
        self.pages = pages

    def run(self):
        asyncio.run(self.func(self.message, self.bot, self.dict_control, self.pages))


def CreateFile(user_id):
    with open(f"data_{user_id}.csv", "w", newline='') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(
            ["Продавець", "Силка на товар", "Ціна", "Наявність ОЛХ доставки", "Місто", "Дата"]
        )