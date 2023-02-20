import json
import os.path
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import requests
import datetime
from fake_useragent import UserAgent

latitude = 58.635513
longitude = 59.79863

APP_PATH = ''


def request_weather(coords):
    print('Request')
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


def get_weather(coords=(latitude, longitude), filename='weather.json', save_json=True, location=None):
    if not save_json:
        return request_weather(coords)
    file_path = os.path.join(APP_PATH, filename)
    if os.path.exists(file_path):
        with open(file_path, encoding='utf-8') as f:
            new_weather = json.load(f)
            if new_weather['today'] == str(datetime.date.today()):
                return new_weather
            else:
                new_weather = request_weather(coords)
                with open(file_path, 'w') as f:
                    f.write(json.dumps(request_weather(coords), indent=2, ensure_ascii=False))
                return new_weather
    else:
        with open(file_path, 'w') as f:
            result = request_weather(coords)
            f.write(json.dumps(result, ensure_ascii=False))
            return json.dumps(result, ensure_ascii=False)


def get_coordinates(city_name):
    geolocator = Nominatim(user_agent='Yndx-parse')
    location = geolocator.geocode(city_name)
    return location.latitude, location.longitude


if __name__ == '__main__':
    coordinates = get_coordinates('Лесной свердловская область')
    get_weather()
