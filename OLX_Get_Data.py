from bs4 import BeautifulSoup
import urllib.parse
import requests
import csv

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

def CreateRequest(url, header): #return list
    pass

def CrateFile():
    with open("data.csv", "w", newline='') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(
            ["Продавець", "Силка на товар", "Ціна", "Наявність ОЛХ доставки", "Місто", "Дата"]
        )

def GetALLValues(url, headers):
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, features="html.parser")
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
            with open("data.csv", "a", newline='') as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow(data_list)

            count = count + 1
        except:
            count_error = count_error + 1
        # item_title = item_soup.find_all(class_="css-1bbgabe")
        # print(item)

    print(count)
    print(count_error)

def GetFromPages(num_of_pages, url):
    if (num_of_pages > 0):
        this_page = 1
        while (this_page != num_of_pages):
            if (this_page == 1):
                GetALLValues(url, headers)
                this_page = this_page + 1
            else:
                if '?page=' not in url:
                    url = url + '?page=' + str(this_page)
                    # print(url)
                    GetALLValues(url, headers)
                    this_page = this_page + 1

                else:
                    if (url[-2] == '='):
                        url = url[:-1]
                        url = url + str(this_page)
                        # print(url)
                        GetALLValues(url, headers)
                        this_page = this_page + 1

                    elif (url[-3] == '='):
                        url = url[:-2]
                        url = url + str(this_page)
                        GetALLValues(url, headers)
                        this_page = this_page + 1

def Get_Num_Pages(url):
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, features="html.parser")
    div_num_of_pages = soup.find(class_="css-4mw0p4")
    num_of_pages = div_num_of_pages.findChildren("a", class_="css-1mi714g")  # ResultSet: List of Tags
    num_of_pages = int(num_of_pages[3].text)
    return num_of_pages

if __name__ == '__main__':
    needed_value = input("Input goods ")
    needed_value = urllib.parse.quote(needed_value)
    url = 'https://www.olx.ua/d/list/q-' + needed_value + '/'
    num_of_pages = Get_Num_Pages(url)
    CrateFile()
    GetFromPages(num_of_pages, url)
