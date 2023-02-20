import json
import os.path
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import requests
import datetime
from fake_useragent import UserAgent

# latitude = 58.635513
# longitude = 59.79863

APP_PATH = ''


class YndxParse:
    def __init__(self,
                 location,
                 folder_to_save=None,
                 filename='weather.json',
                 save_json=True):
        self.folder_to_save = folder_to_save
        self.filename = filename
        self.save_json = save_json
        self.location = location if type(location) == tuple else self.get_coordinates(location)

    def get_weather(self):
        if not self.save_json:
            return self.__request_weather(self.location)
        file_path = os.path.join(APP_PATH, self.filename)
        if os.path.exists(file_path):
            with open(file_path, encoding='utf-8') as f:
                new_weather = json.load(f)
                if new_weather['today'] == str(datetime.date.today()) and new_weather['coords'] == self.location:
                    return new_weather
                else:
                    new_weather = self.__request_weather(self.location)
                    with open(file_path, 'w') as f:
                        f.write(json.dumps(self.__request_weather(self.location), indent=2, ensure_ascii=False))
                    return new_weather
        else:
            with open(file_path, 'w') as f:
                result = self.__request_weather(self.location)
                f.write(json.dumps(result, indent=2, ensure_ascii=False))
                return json.dumps(result, ensure_ascii=False)

    def __request_weather(self, coords):
        print('Request')
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random,
        }
        dict_with_weather = {
            'today': str(datetime.date.today()),
            'weather': {},
            'coords': coords,
        }
        url = f'https://yandex.ru/pogoda/details/10-day-weather?lat={self.location[0]}&lon={self.location[1]}&via=ms'
        content = requests.get(url, headers=headers).text
        soup = BeautifulSoup(content, 'html.parser')
        print(len(soup))
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

    @staticmethod
    def get_coordinates(city_name):
        geolocator = Nominatim(user_agent='Yndx-parse')
        location = geolocator.geocode(city_name)
        return location.latitude, location.longitude


if __name__ == '__main__':
    yp = YndxParse(location='Реж')
    yp.get_weather()
