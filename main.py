import json
import os.path
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import requests
import datetime
from fake_useragent import UserAgent

latitude = 58.635513
longitude = 59.79863
geolocator = Nominatim(user_agent='Yndx-parse')

APP_PATH = ''


def get_weather(coordinates=(latitude, longitude)):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
    }
    dict_with_weather = {
        'today': str(datetime.date.today()),
        'weather': {},
    }
    url = f'https://yandex.ru/pogoda/details/10-day-weather?lat={coordinates[0]}&lon={coordinates[1]}&via=ms'
    content = requests.get(url, headers=headers).text
    soup = BeautifulSoup(content, 'html.parser')
    weather_tables = soup.findAll('table', class_='weather-table')
    dict_with_weather['city'] = soup.find('h1', id="main_title").text
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
        with open(file_path, 'rb') as f:
            result_dict = json.loads(f.read())
            if result_dict['today'] == str(datetime.date.today()):
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
            f.write(json.dumps({"today": "1", "weather": "1"}, indent=2))
            write_weather()


def get_coordinates(city):
    location = geolocator.geocode(city)
    return location.latitude, location.longitude


if __name__ == '__main__':
    coordinates = get_coordinates('Лесной свердловская область')
    print(get_weather(coordinates))
