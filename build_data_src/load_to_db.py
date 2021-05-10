import pandas as pd
 
import json
import os

from sqlalchemy import engine as sql


def load_lists_for_db(): 

    IDs = [] # Список идентификаторов вакансий
    names = [] # Список наименований вакансий
    descriptions = [] # Список описаний вакансий
     

    skills_vac = [] # Список идентификаторов вакансий
    skills_name = [] # Список названий навыков

    cnt_docs = len(os.listdir('./json_files/vacancies'))
    i = 0

    for fl in os.listdir('./json_files/vacancies'):

        f = open('./json_files/vacancies/{}'.format(fl), encoding='utf8')
        jsonText = f.read()
        f.close()

        jsonObj = json.loads(jsonText)

        IDs.append(jsonObj['id'])
        names.append(jsonObj['name'])
        descriptions.append(jsonObj['description'])

        for skl in jsonObj['key_skills']:
            skills_vac.append(jsonObj['id'])
            skills_name.append(skl['name'])

        i += 1

    return (IDs, names, descriptions, skills_vac, skills_name)


def add_values_to_db(db_user, db_pass, db_host, db_port, db_name):
    """ Создадим соединение с БД"""
    eng = sql.create_engine('postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name))
    conn = eng.connect()
    IDs, names, descriptions, skills_vac, skills_name = load_lists_for_db()

    df = pd.DataFrame({'id': IDs, 'name': names, 'description': descriptions})
    df.to_sql('vacancies', conn, schema='public', if_exists='append', index=False)


    df = pd.DataFrame({'vacancy': skills_vac, 'skill': skills_name})
    df.to_sql('skills', conn, schema='public', if_exists='append', index=False)

    conn.close()


db_user = os.environ.get('POSTGRES_USER')
db_pass = os.environ.get('POSTGRES_PASS')
db_host = os.environ.get('POSTGRES_HOST')
db_port = os.environ.get('POSTGRES_PORT')
db_name = os.environ.get('POSTGRES_NAME')


add_values_to_db(db_user, db_pass, db_host, db_port, db_name)
