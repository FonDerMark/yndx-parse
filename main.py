from bs4 import BeautifulSoup
import requests
import datetime
from fake_useragent import UserAgent
from lxml import etree
import re

latitude = 58.635513
longitude = 59.79863


def get_weather(path='', lat=latitude, lon=longitude):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
    }
    url = f'https://yandex.ru/pogoda/details/10-day-weather?lat={lat}&lon={lon}&via=ms'
    content = requests.get(url, headers=headers).text
    soup = BeautifulSoup(content, 'lxml')
    dom = etree.HTML(str(soup))
    print(dom.xpath('/html/body/div[1]/div[3]/div[2]/div/div/article[1]/div[2]/table/tbody')[0].text)


if __name__ == '__main__':
    get_weather()
