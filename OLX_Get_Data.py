from bs4 import BeautifulSoup
import urllib.parse
import requests
import csv
import asyncio
import aiohttp
import time
import os
import aiogram
from multiprocessing import Process
import psycopg2
from aiogram import types
from threading import Thread


# Creating Async thread
class DownloadThread(Thread):
    def __init__(self, func, url, count_pages):
        super(DownloadThread, self).__init__()
        self.func = func
        self.url = url
        self.count = count_pages
        #Thread.__init__(self)

    def run(self):
        asyncio.run(self.func(self.url, self.count))

class Parce_Thread(Thread):
    def __init__(self, func, message: types.Message, bot, dict_control):
        super(Parce_Thread, self).__init__()
        self.func = func
        self.id = id
        self.message = message
        self.bot = bot
        self.dict_control = dict_control

    def run(self):
        asyncio.run(self.func(self.message, self.bot, self.dict_control))


class ControlCycle(Thread):
    def __init__(self, func, url, count_pages):
        super(ControlCycle, self).__init__()
        self.func = func
        self.url = url
        self.count = count_pages
        #Thread.__init__(self)

    def control_loadfile(self, control_dict, id):
        while True:
            if control_dict[id] == True:
                pass


    def run(self):
        asyncio.run(self.func(self.url, self.count))


headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

pages = []


def CreateRequest(url, header): #return list
    pass

def CreateFile(user_id):
    with open(f"data_{user_id}.csv", "w", newline='') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(
            ["Продавець", "Силка на товар", "Ціна", "Наявність ОЛХ доставки", "Місто", "Дата"]
        )

async def get_data_from_page(Pages, message: types.Message, bot, control_dict):
    if(type(Pages) is list):
        for page in Pages:
            await LoadData(page, message.from_user.id)
        control_dict[message.from_user.id] = True
        # file = open(f"data_{message.from_user.id}.csv", "rb")
        # await bot.send_document(message.chat.id, file)
        # os.remove(f"data_{message.from_user.id}.csv")

    else:
        await LoadData(Pages, message.from_user.id)

async def create_tsk(message: types.Message, bot, dict_control):
    parse_task = asyncio.create_task(get_data_from_page(pages, message, bot, dict_control))
    await parse_task

async def LoadData(page, user_id):
    soup = BeautifulSoup(page, features="html.parser")
    page_items = soup.find_all(class_="css-19ucd76")
    print(len(page_items))
    count = 0
    count_error = 0
    for item in page_items:
        child_url = item.findChildren("a")  # return ResultSet
        child_title = item.findChildren("h6") # return ResultSet
        child_price = item.findChildren(class_="css-wpfvmn-Text eu5v0x0")
        child_OLX_delivering = item.findChildren(class_= "css-1ojrdd5")
        сhild_City_Date = item.findChildren(class_="css-p6wsjo-Text eu5v0x0")

        isDeliver = ""
        try:
            print(child_title[0].get_text())
            LstDateCity = сhild_City_Date[0].get_text().split(" - ")
            print(LstDateCity)
            if(len(child_OLX_delivering) == 1):
                isDeliver = "Так"
            elif(len(child_OLX_delivering) == 0):
                isDeliver = "Ні"
            parced_url = 'https://www.olx.ua' + child_url[0]['href']  # You can get value of tag like in dict
            # print(child_url[0]['href'])
            data_list = [child_title[0].get_text(), parced_url, child_price[0].get_text(), isDeliver, LstDateCity[0], LstDateCity[1]]
            with open(f"data_{user_id}.csv", "a", newline='') as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow(data_list)
            count = count + 1
        except:
            count_error = count_error + 1
        # item_title = item_soup.find_all(class_="css-1bbgabe")
        # print(item)

    print(count)
    print(count_error)

async def get_page_data_async(session, url):
    async with session.get(url, headers = headers) as responce:
        #print(responce.status)
        text = await responce.text()
        pages.append(text)


def GetFromPages_Async(num_of_pages, url):
    if (num_of_pages > 0):
        this_page = 1
        while (this_page != num_of_pages):
            if (this_page == 1):
                LoadData(url)
                this_page = this_page + 1
            else:
                if '?page=' not in url:
                    url = url + '?page=' + str(this_page)
                    # print(url)
                    LoadData(url)
                    this_page = this_page + 1

                else:
                    if (url[-2] == '='):
                        url = url[:-1]
                        url = url + str(this_page)
                        # print(url)
                        LoadData(url)
                        this_page = this_page + 1

                    elif (url[-3] == '='):
                        url = url[:-2]
                        url = url + str(this_page)
                        LoadData(url)
                        this_page = this_page + 1

async def load_data_async(url, pages_count):
    tasks = []
    page_url = url
    async with aiohttp.ClientSession() as session:
        for page in range(1, pages_count + 1):
            if(page == 1):
                pass
                #page_url = url
                #task = asyncio.create_task(get_page_data_async(session, url))
            else:
                if '?page=' not in page_url:
                    page_url = page_url + '?page=' + str(page)
                    #task = asyncio.create_task(get_page_data_async(session, url))
                else:
                    if (page_url[-2] == '='):
                        page_url = page_url[:-1]
                        page_url = page_url + str(page)
                        #task = asyncio.create_task(get_page_data_async(session, url))
                    elif (page_url[-3] == '='):
                        page_url = page_url[:-2]
                        page_url = page_url + str(page)

            task = asyncio.create_task(get_page_data_async(session, page_url))
            tasks.append(task)
        await asyncio.gather(*tasks)

def Get_Num_Pages(url):
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, features="html.parser")
    div_num_of_pages = soup.find(class_="css-4mw0p4")
    num_of_pages = div_num_of_pages.findChildren("a", class_="css-1mi714g")  # ResultSet: List of Tags
    num_of_pages = int(num_of_pages[3].text)
    return num_of_pages

async def test_aio_session():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://python.org') as response:
            print("Status:", response.status)
            text = await response.text()
            print(text)

def split_pages_to_thread():
    process_count = 5
    Pages1, Pages2, Pages3, Pages4, Pages5 = []
    for i in range(1, len(pages) + 1):
        if (i < 6):
            Pages1.append(pages[i - 1])

        elif(i < 11):
            Pages2.append(pages[i - 1])

        elif(i < 16):
            Pages3.append(pages[i - 1])

        elif(i < 21):
            Pages4.append(pages[i - 1])

        elif(i < 26):
            Pages5.append(pages[i - 1])

async def start_loop(url, page_number):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(load_data_async(url, page_number))
    get_data_from_page(Pages=pages)

if __name__ == '__main__':
    needed_value = input("Input goods ")
    start_time = time.time()
    needed_value = urllib.parse.quote(needed_value)
    url = 'https://www.olx.ua/d/list/q-' + needed_value + '/'
    num_of_pages = Get_Num_Pages(url)
    CreateFile()

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    #asyncio.run(load_data_async(url, num_of_pages))

    th = DownloadThread(load_data_async, url, num_of_pages)
    th.start()
    th.join()

    #get_data_from_page(Pages=pages)
    asyncio.run(create_tsk())

    end_time = time.time() - start_time
    print(f"\nExecution time: {end_time} seconds")
