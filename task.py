import random
import sys
from io import BytesIO

import requests
from PIL import Image

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication

CITIES = ("Лондон", "Париж", "Нью-Йорк", "Москва", "Дубай", "Токио", "Сингапур", "Лос-Анджелес", "Барселона", "Мадрид",
          "Рим", "Доха", "Чикаго", "Абу-Даби", "Сан-Франциско", "Амстердам", "Санкт-Петербург", "Торонто", "Сидней",
          "Берлин", "Лас-Вегас", "Вашингтон", "Стамбул", "Вена", "Пекин", "Прага", "Милан", "Сан-Диего", "Гонконг",
          "Мельбурн", "Бостон", "Хьюстон", "Дублин", "Майами", "Цюрих", "Сиэтл", "Будапешт", "Сан-Паоло", "Мюнхен",
          "Бангкок", "Орландо", "Сеул", "Атланта", "Даллас", "Франкфурт", "Ванкувер", "Остин", "Монреаль", "Калгари",
          "Дели", "Лиссабон", "Неаполь", "Осака", "Сан-Хосе", "Эр-Рияд", "Денвер", "Филадельфия", "Тель-Авив",
          "Копенгаген", "Брюссель", "Брисбен", "Валенсия", "Буэнос-Айрес", "Тайбэй", "Рио-де-Жанейро", "Портленд",
          "Гамбург", "Кувейт", "Варшава", "Афины", "Перт", "Хельсинки", "Миннеаполис", "Осло", "Шанхай", "Феникс",
          "Окленд", "Новый Орлеан", "Иерусалим", "Маскат", "Нашвилл", "Стокгольм", "Сантьяго", "Оттава", "Балтимор",
          "Эдмонтон", "Лион", "Марсель", "Аделаида", "Гетеборг", "Бильбао", "Мехико", "Солт-Лейк-Сити", "Мумбай",
          "Сакраменто", "Сан-Антонио", "Туксон", "Севилья", "Шарлотт", "Нанкин", "Нью-Дели", "Джакарта", "Исламабад",
          "Абуджа", "Бразилиа", "Дакка", "Аддис-Абеба", "Манила", "Каир", "Киншаса", "Ханой", "Тегеран", "Претория",
          "Кейптаун", "Найроби", "Нейпьидо", "Кампала", "Богота", "Хартум", "Алжир", "Багдад", "Киев", "Кабул",
          "Канберра", "Астана", "Улан-Батор", "Ташкент", "Баку", "Харьков", "Нижний Новгород", "Новосибирск", "Минск",
          "Самара", "Екатеринбург", "Тбилиси", "Днепр", "Одесса", "Челябинск", "Донецк", "Ереван", "Омск", "Пермь",
          "Казань", "Уфа", "Ростов-на-Дону", "Волгоград", "Алматы", "Саратов", "Рига", "Красноярск", "Воронеж",
          "Запорожье", "Львов", "Кривой Рог", "Ярославль", "Караганда", "Краснодар", "Владивосток", "Иркутск", "Ижевск",
          "Новокузнецк", "Барнаул", "Бишкек", "Хабаровск", "Тула", "Кишинёв", "Мариуполь", "Тольятти", "Душанбе",
          "Пенза", "Вильнюс", "Самарканд", "Кемерово", "Иваново", "Ульяновск", "Луганск", "Астрахань", "Оренбург",
          "Рязань", "Николаев", "Макеевка", "Таллин", "Томск", "Тверь", "Магнитогорск", "Нижний Тагил", "Липецк",
          "Брянск", "Киров", "Архангельск", "Гомель", "Мурманск", "Курск", "Грозный", "Каунас", "Тюмень", "Калининград",
          "Горловка", "Чимкент", "Херсон", "Винница", "Ашхабад", "Курган", "Чебоксары", "Орёл", "Чита", "Симферополь",
          "Набережные Челны", "Севастополь", "Улан-Удэ", "Витебск", "Владимир", "Могилёв", "Сочи", "Семей", "Полтава",
          "Орджоникидзе", "Таганрог", "Смоленск", "Усть-Каменогорск", "Павлодар", "Тамбов", "Прокопьевск", "Череповец",
          "Калуга", "Комсомольск-на-Амуре")


def get_image(longitude, latitude, map_type):
    api_server = 'http://static-maps.yandex.ru/1.x'

    params = {
        'll': f'{longitude},{latitude}',
        'l': map_type,
        'z': 13 if map_type == 'sat' else 16,
        'size': '650,450',
    }

    response = requests.get(api_server, params=params)

    image = Image.open(BytesIO(response.content))
    image.save('map.png')


class Map(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Maps.ui', self)

        self.city = self.address = None

        self.next_city()

        self.ask.clicked.connect(self.choice)

    def choice(self):
        if self.ask.text() == 'Ответить':
            self.check_answer()

        else:
            self.next_city()

    def check_answer(self):
        if self.data.text().lower() == self.city.lower():
            self.comment.setText('Верно!!!')

        else:
            self.comment.setText('Неверно...')

        self.map_city.setText(self.address)
        self.ask.setText('Следующий город')

    def next_city(self):
        self.city = random.choice(CITIES)

        self.ask.setText('Ответить')
        self.comment.clear()
        self.map_city.clear()
        self.data.clear()

        out_format = 'json'
        api_server = 'http://geocode-maps.yandex.ru/1.x'
        api_key = "40d1649f-0493-4b70-98ba-98533de7710b"

        params = {
            'geocode': self.city,
            'format': out_format,
            'apikey': api_key
        }

        response = requests.get(api_server, params=params).json()

        self.address = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'][
            'metaDataProperty']['GeocoderMetaData']['Address']['formatted']

        longitude, latitude = map(float, response['response']['GeoObjectCollection']['featureMember'][
            0]['GeoObject']['Point']['pos'].split())

        map_type = random.choice(('map', 'sat'))

        get_image(longitude, latitude, map_type)
        pixmap = QPixmap('map.png')
        self.image.setPixmap(pixmap)


if __name__ == '__main__':
    application = QApplication(sys.argv)
    window = Map()
    window.show()
    sys.exit(application.exec())
