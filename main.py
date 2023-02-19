import json
import os.path

from bs4 import BeautifulSoup
import requests
import datetime
from fake_useragent import UserAgent
import re

latitude = 58.635513
longitude = 59.79863

APP_PATH = ''


def get_weather(lat=latitude, lon=longitude):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
    }
    url = f'https://yandex.ru/pogoda/details/10-day-weather?lat={lat}&lon={lon}&via=ms'
    content = requests.get(url, headers=headers).text
    soup = BeautifulSoup(content, 'lxml')


def write_weather(dict_with_weather, filename='weather.json'):
    file_path = os.path.join(APP_PATH, filename)
    if os.path.exists(file_path):
        print('file exists')
        with open(file_path, 'r') as f:
            if json.loads(f.read()).get('today') == str(datetime.date.today()):
                print('Today')
                return json.loads(f.read())
            else:
                new_weather = get_weather()
                with open(file_path, 'w') as f:
                    f.write(json.dumps(dict_with_weather))
                return new_weather
    else:
        with open(file_path, 'w') as f:
            f.write(json.dumps(dict_with_weather))
            write_weather(dict_with_weather)


if __name__ == '__main__':
    write_weather({'test': 'test'})