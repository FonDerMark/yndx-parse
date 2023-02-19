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
    dict_with_weather = {
        'today': str(datetime.date.today()),
        'weather': {},
    }
    url = f'https://yandex.ru/pogoda/details/10-day-weather?lat={lat}&lon={lon}&via=ms'
    content = requests.get(url, headers=headers).text
    soup = BeautifulSoup(content, 'lxml')
    weather_tables = soup.findAll('table', class_='weather-table')
    count = 0
    tag = 0
    for i in weather_tables:
        for j in i.findAll('div', 'weather-table__temp'):
            if not dict_with_weather['weather'].get(tag):
                dict_with_weather['weather'][tag] = []
            dict_with_weather['weather'][tag].append(j.text)
            count += 1
            if count == 4:
                tag += 1
                count = 0
    return dict_with_weather


def write_weather(filename='weather.json'):
    file_path = os.path.join(APP_PATH, filename)
    if os.path.exists(file_path):
        print('file exists')
        with open(file_path, 'r') as f:
            print(f.read())
            print(type(f.read()))
            print(json.loads(f.read()))
            if json.loads(f.read()).get('today') == str(datetime.date.today()):
                print('Today')
                return json.loads(f.read())
            else:
                print('No today')
                new_weather = get_weather()
                with open(file_path, 'w') as f:
                    f.write(json.dumps(get_weather(), indent=2, ensure_ascii=False))
                return new_weather
    else:
        with open(file_path, 'w') as f:
            f.write(json.dumps({'today': '', 'weather': ''}))
            write_weather()


if __name__ == '__main__':
    write_weather()