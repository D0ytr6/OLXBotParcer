import requests
import aiohttp
import asyncio

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

async def load_data_async(url, pages_count, pages):
    tasks = []
    page_url = url
    async with aiohttp.ClientSession() as session:
        for page in range(1, pages_count + 1):
            if(page == 1):
                pass
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

            task = asyncio.create_task(get_page_data_async(session, page_url, pages))
            tasks.append(task)
        await asyncio.gather(*tasks)

#create list with text data from pages
async def get_page_data_async(session, url, pages):
    async with session.get(url, headers = headers) as responce:
        #print(responce.status)
        text = await responce.text()
        pages.append(text)