from bs4 import BeautifulSoup
from olx_scraper import request_olx, soup_olx, settings
import urllib.parse
import asyncio
import aiohttp
import time
import datetime

def find_new_advertisement(page):
    pass

# def GetFromPages_Async(num_of_pages, url):
#     if (num_of_pages > 0):
#         this_page = 1
#         while (this_page != num_of_pages):
#             if (this_page == 1):
#                 LoadData(url)
#                 this_page = this_page + 1
#             else:
#                 if '?page=' not in url:
#                     url = url + '?page=' + str(this_page)
#                     # print(url)
#                     LoadData(url)
#                     this_page = this_page + 1
#
#                 else:
#                     if (url[-2] == '='):
#                         url = url[:-1]
#                         url = url + str(this_page)
#                         # print(url)
#                         LoadData(url)
#                         this_page = this_page + 1
#
#                     elif (url[-3] == '='):
#                         url = url[:-2]
#                         url = url + str(this_page)
#                         LoadData(url)
#                         this_page = this_page + 1


async def test_aio_session():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://python.org') as response:
            print("Status:", response.status)
            text = await response.text()
            print(text)

def split_pages_to_thread(pages):
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

# async def start_loop(url, page_number, pages):
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     asyncio.run(load_data_async(url, page_number))
#     get_data_from_page(Pages=pages)


async def create_test_date_find(pages, current_hour):
    t1 = asyncio.create_task(soup_olx.get_data_from_pages_everyhour(pages, current_hour))
    await t1

if __name__ == '__main__':
    pages = list()
    url = 'https://www.olx.ua/d/list/q-xiaomi/' + '?search%5Border%5D=created_at:desc'
    num_of_pages = soup_olx.Get_Num_Pages(url)
    current_hour = datetime.datetime.now()
    # current_hour = current_hour - datetime.timedelta(hours=1)
    current_hour = current_hour.hour
    print(current_hour)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    th = settings.DownloadThread(request_olx.load_schedule_data_async, url, num_of_pages, pages)
    th.start()
    th.join()

    asyncio.run(create_test_date_find(pages, current_hour))
    # needed_value = input("Input goods ")
    # start_time = time.time()
    # needed_value = urllib.parse.quote(needed_value)
    # url = 'https://www.olx.ua/d/list/q-' + needed_value + '/'


    # CreateFile()
    #
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # asyncio.run(load_data_async(url, num_of_pages))
    #
    # th = DownloadThread(load_data_async, url, num_of_pages)
    # th.start()
    # th.join()
    #
    # #get_data_from_page(Pages=pages)

    #
    # end_time = time.time() - start_time
    # print(f"\nExecution time: {end_time} seconds")