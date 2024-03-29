from bs4 import BeautifulSoup
from .request_olx import headers
from aiogram import types
import asyncio
import csv
import requests

class EndTimeIteration(RuntimeError):
    pass

def Get_Num_Pages(url):
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, features="html.parser")
    div_num_of_pages = soup.find(class_="css-4mw0p4")
    num_of_pages = div_num_of_pages.findChildren("a", class_="css-1mi714g")  # ResultSet: List of Tags
    try:
        num_of_pages = int(num_of_pages[3].text)
    except IndexError:
        num_of_pages = 1
    return num_of_pages

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
        child_city_date = item.findChildren(class_="css-p6wsjo-Text eu5v0x0")

        isDeliver = ""
        try:
            print(child_title[0].get_text())
            LstDateCity = child_city_date[0].get_text().split(" - ")
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

async def last_updated_smth(page, start_hour, start_price = 0):
    soup = BeautifulSoup(page, features="html.parser")
    page_items = soup.find_all(class_="css-19ucd76")
    count = 0
    str_hour = str(start_hour)
    for item in page_items:
        try:
            child_url = item.findChildren("a")  # return ResultSet
            child_url = 'https://www.olx.ua' + child_url[0]['href']
            child_date = item.findChildren(class_="css-p6wsjo-Text eu5v0x0")
            child_price = item.findChildren(class_="css-wpfvmn-Text eu5v0x0")
            price = child_price[0].get_text()
            if(price.find("Договірна") != -1):
                price = price.replace("Договірна", "")
            price = price.replace(" грн.", "")
            price = price.replace(" ", "")
            price = int(price)
            try:
                if(child_date[0].get_text().find("Сьогодні") != -1):
                    time = child_date[0].get_text()[-5:]
                    change_hour = int(time[0:2]) + 3
                    #child_price = int(child_price[0].get_text())
                    # print(f"Datetime{str_hour}\t olxhour{change_hour}")
                    if(str(change_hour) == str_hour and price > start_price):
                        print(child_date[0].get_text() + " " + child_url)
                    elif(str(change_hour) == str(int(str_hour) - 1)):
                        #print(f'Exception end {id(page)}')
                        raise EndTimeIteration
                        # return

                count += 1

            except:
                pass
        except:
            pass
    print(count)

async def get_data_from_pages_everyhour(pages, start_hour):
    for page in pages:
        try:
            await last_updated_smth(page, start_hour, start_price=1000)
        except EndTimeIteration as e:
            print("End Exception")
            return

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

async def create_tsk(message: types.Message, bot, dict_control, pages):
    parse_task = asyncio.create_task(get_data_from_page(pages, message, bot, dict_control))
    await parse_task

