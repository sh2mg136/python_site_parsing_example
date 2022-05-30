# Учим парсинг на python и bs4
# Курс по парсингу веб сайтов на python с нуля
# профессия backend аналитик
# https://www.youtube.com/watch?v=lOfm04oLD1U
# Part 2
from datetime import datetime
import os
import re
from requests import Session
from bs4 import BeautifulSoup
from time import sleep
import random
from XslxHelper import write_quotes_to_excel
import time

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67"}

BASE_URL = "https://quotes.toscrape.com/"
BASE_URL_LOGIN = "https://quotes.toscrape.com/login"
BASE_URL_PAGES = "https://quotes.toscrape.com/page/"

DIR_NAME = r"f:/temp/quotes"

work_session = Session()
work_session.get(BASE_URL, headers=headers)
resp = work_session.get(BASE_URL_LOGIN, headers=headers)


def start_process(max_pages_amount):
    soup = BeautifulSoup(resp.text, "lxml")
    token = soup.find("form").find("input").get("value")
    print(token)
    credentials = {"csrf_token": "", "username": "noname", "password": "qwerty123"}
    login_result = work_session.post(BASE_URL_LOGIN, headers=headers, data=credentials, allow_redirects=True)
    print(login_result)
    # print(login_result.text)
    if not os.path.isdir(DIR_NAME):
        os.mkdir(DIR_NAME)
    # file_name = os.path.join(DIR_NAME, f"quotes_{random.randint(1000, 9999)}.xlsx")
    file_name = os.path.join(DIR_NAME, f"quotes_{datetime.today().strftime('%Y-%m-%d_%H-%M')}.xlsx")
    print(file_name)
    if max_pages_amount <= 1:
        max_pages_amount = 2
    write_quotes_to_excel(parse_pages(max_pages_amount), file_name)
    if os.path.isfile(file_name):
        print(f"OK! File created [{file_name}]")

def parse_pages(max_pages_amount):
    for page_num in range(1, max_pages_amount):
        page = work_session.get(BASE_URL_PAGES + f"{page_num}", headers=headers)
        soup = BeautifulSoup(page.text, "lxml")

        result = soup.find_all("div", class_="quote")

        if len(result) != 0:
            print(f"PAGE {page_num}")
            quotes = soup.find_all("span", class_="text")
            authors = soup.find_all("small", class_="author")
            for i in range(0, len(quotes)):
                # print(f"{authors[i].text}\n{titles[i].text}\n")
                yield authors[i].text, quotes[i].text
            sleep(random.randint(2, 5))
        else:
            print("\nEXIT\n")
            break
