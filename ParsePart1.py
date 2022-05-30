# Учим парсинг на python и bs4
# Курс по парсингу веб сайтов на python с нуля
# профессия backend аналитик
# https://www.youtube.com/watch?v=lOfm04oLD1U
# Part 1

import os
import re

import requests
from bs4 import BeautifulSoup
from time import sleep
import random
from XslxHelper import write_xslx
import time

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67"}

# def print_hi(name):
#    # Use a breakpoint in the code line below to debug your script.
#    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
    # print_hi('PyCharm')

BASE_URL = "https://scrapingclub.com"
DIR_NAME = r"f:/temp/parse_site_data/"


def download_files(url):
    resp = requests.get(url, stream=True)
    fn = url.split("/")[-1]
    image_dir = os.path.join(DIR_NAME, "images");
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)
    r = open(os.path.join(image_dir, fn), "wb")
    for val in resp.iter_content(1024*1024):
        r.write(val)
    r.close()


def get_url():
    for cnt in range(2, 3):
        site_url = f"https://scrapingclub.com/exercise/list_basic/?page={cnt}"
        resp = requests.get(site_url, headers=headers)
        # print(response)
        # print(response.text)
        tmp_soup = BeautifulSoup(resp.text, "lxml")  # html.parser
        # print(soup)
        tmp_data = tmp_soup.find_all("div", class_="col-lg-4 col-md-6 mb-4")
        # name = data.find("h4", class_="card-title").text.replace("\n", "")
        # price = data.find("h5").text
        # url_img = "https://scrapingclub.com" + data.find("img", class_="card-img-top img-fluid").get("src")
        # print(f'{name}  ({price})  [{url_img}]')

        for tmp_i in tmp_data:
            # name = i.find("h4", class_="card-title").text.replace("\n", "")
            # price = i.find("h5").text
            # url_img = "https://scrapingclub.com" + i.find("img", class_="card-img-top img-fluid").get("src")
            # print(f'{name}  ({price})  [{url_img}]')
            tmp_card_url = BASE_URL + tmp_i.find("a").get("href")
            # print(card_url)
            # list_card_url.append(card_url)
            yield tmp_card_url


###########
# Generator
def generate_data_array():
    for card_url in get_url():
        sleep(random.randrange(1, 2))
        response = requests.get(card_url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find("div", class_="card mt-4 my-4")
        # print(data)
        '''
        <div class="card mt-4 my-4">
        <img alt="Blazer" class="card-img-top img-fluid" src="/static/img/93086-B.jpg"/>
        <div class="card-body">
        <h3 class="card-title">Blazer</h3>
        <h4>$49.99</h4>
        <p class="card-text">Double-breasted blazer with in woven fabric with notched lapels, buttons at front, and welt front pockets. Lined. 63% polyester, 33% rayon, 4% spandex. Dry clean only.</p>
        </div>
        </div>
        '''
        name = data.find("h3", class_="card-title").text
        price = data.find("h4").text
        text = data.find("p", class_="card-text").text
        img_url = BASE_URL + data.find("img").get("src")
        # print(f'{name}  [{price}]  [{img_url}]  {text}')

        download_files(img_url)

        yield name, price, text, img_url


def get_lead_zero_number(a_num):
    if a_num < 0 or a_num > 999999:
        a_num = 0
    number_str = str(a_num)
    zero_filled_number = number_str.zfill(6)  # Pad `number_str` with zeros to 5 digits.
    print(zero_filled_number)
    return zero_filled_number


def start_process():
    ###
    if not os.path.isdir(DIR_NAME):
        os.mkdir(DIR_NAME)

    files = [f for f in os.listdir(DIR_NAME) if os.path.isfile(os.path.join(DIR_NAME, f)) and f.endswith(".xlsx")]

    files2 = []
    subs = []
    indxs = []

    for fl in files:
        if re.search("^data_?[0-9]+.xlsx$", fl):
            files2.append(fl)
            p = re.compile("[0-9]+")
            subs.append(p.findall(fl))

    # print(files2)
    print(subs)
    for s in subs:
        try:
            indxs.append(int(s[0]))
        except BaseException as ex:
            print(f"Unexpected {ex=}, {type(ex)=}")

    num_max = 0

    if len(indxs) > 0:
        print(indxs)
        print(min(indxs))
        num_max = max(indxs)
        print(num_max)

    # filename = dir_name + rf"data_{random.randrange(1000, 9999)}.xlsx"
    filename = DIR_NAME + rf"data_{get_lead_zero_number(num_max + 1)}.xlsx"
    # start = time.time()
    write_xslx(generate_data_array(), filename)
    # end = time.time()
    # print("OK")
    # print(f"Elapsed time: {round(end - start, 4)} sec")

