from bs4 import BeautifulSoup
import urllib.parse
import asyncio
import aiohttp
import time

def find_new_advertisement(page):
    soup = BeautifulSoup(page, features="html.parser")
    page_items = soup.find_all(class_="css-19ucd76")
    for item in page_items:
        сhild_City_Date = item.findChildren(class_="css-p6wsjo-Text eu5v0x0")

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