import json
import os
import requests
import time


def get_vacancies_func():
    """ 
        Получаем перечень ранее созданных файлов со списком вакансий и проходимся по нему в цикле
    """
    for fl in os.listdir('./json_files/hh_files'):

        f = open('./json_files/hh_files/{}'.format(fl), encoding='utf8')
        jsonText = f.read()
        f.close()

        jsonObj = json.loads(jsonText)


        for v in jsonObj['items']:

            req = requests.get(v['url'])
            data = req.content.decode()
            req.close()

            fileName = './json_files/vacancies/{}.json'.format(v['id'])
            f = open(fileName, mode='w', encoding='utf8')
            f.write(data)
            f.close()


get_vacancies_func()
