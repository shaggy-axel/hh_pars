import requests
import json
import time
import os


def getPage(page = 0):
    """
    Создаем метод для получения страницы со списком вакансий.
    Аргументы:
        page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
    """

    params = {
        'text': 'NAME:Аналитик', # Текст фильтра. В имени должно быть слово "Аналитик"
        'area': 1, # Поиск ощуществляется по вакансиям города Москва
        'page': page, # Индекс страницы поиска на HH
        'per_page': 100 # Кол-во вакансий на 1 странице
    }


    req = requests.get('https://api.hh.ru/vacancies', params) # Посылаем запрос к API
    data = req.content.decode() # Декодируем его ответ, чтобы Кириллица отображалась корректно
    req.close()
    return data


def reading_pages_from_hh():
    """ Считываем первые 2000 вакансий """
    for page in range(0, 20):

        jsObj = json.loads(getPage(page))

        nextFileName = './json_files/hh_files/{}.json'.format(len(os.listdir('./json_files/hh_files')))

        f = open(nextFileName, mode='w', encoding='utf8')
        f.write(json.dumps(jsObj, indent=4, sort_keys=True, ensure_ascii=False))
        f.close()

        if (jsObj['pages'] - page) <= 1:
            break


reading_pages_from_hh()
