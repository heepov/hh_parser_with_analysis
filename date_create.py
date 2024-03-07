import json
import pandas as pd
import re
import requests
from tqdm import tqdm
from dateutil import parser as date_parser



# принимает:
# 'm' - все данные в list(dict) полученные по id вакансии 

# возвращает:
# список с искомыми (чистыми) данными

def fill_row(m):
    
    d = []
    # проверка заполненности данных в выбранном поле.
    def name_none(data):
        # если ЕСТЬ данные заполняем из значения name
        if data != None:
            d.append(data.get('name'))
        # если данные отсутствуют заполняем None
        else:
            d.append(None)
    
    # формирования данных по зарплате
    def salary_none(data):
        # если ЕСТЬ данные по зарплате, заполняем ОТ, ДО, ВАЛЮТА
        if data != None:
            d.append(True)
            d.append(data.get('from'))
            d.append(data.get('to'))
            d.append(data.get('currency'))
        # если данные отсутствуют заполняем None
        else:
            d.append(False)
            d.append(None)
            d.append(None)
            d.append(None)
    
    # очистка данных "описание вакансии" от ненужных тегов
    def clear_description(data):
        # возвращаем чистую строку
        return re.sub(r"<[^>]+>", "", data, flags=re.S)
    
    # формирование массива с "ключевыми навыками"
    def key_skills_fill(data):
        res = []
        # если ЕСТЬ данные формируем и возвращаем массив со всеми ключевыми навыками
        if data != None and len(data) != 0:
            return [el["name"] for el in data]
        # если данные отсутствуют возвращаем None
        else:
            return None
    
    # обработка строки с "датой публикации вакансии"
    def fill_date(published_at):
        if published_at:
            d.append(date_parser.parse(published_at))
        else:
            d.append(None)
    
    # поиск и заполнение данных одной строки в массив
    # print(f"{m.get('id')} {m.get('alternate_url')}")
    
    d.append(int(m.get('id')))
    d.append(m.get('premium'))
    d.append(m.get('name'))
    name_none(m.get('area'))
    
    salary_none(m.get('salary'))
       
    name_none(m.get('experience'))
    name_none(m.get('schedule'))
    name_none(m.get('employment'))
    
    d.append(clear_description(m.get('description')))
    d.append(key_skills_fill(m.get('key_skills')))
    
    name_none(m.get('employer'))
    fill_date(m.get('published_at'))
    
    d.append(m.get('alternate_url'))
    d.append(m.get('has_test'))
    
    return d

# принимает:
# 'ids' - список со всеми id искомых вакансий
# 'url' - адрес API

# возвращает:
# итоговая таблица со всем искомыми вакансиями

def create_df(ids, url):
    # список с названиями колонок таблицы
    columns = [ 'id',
                'premium',
                'vacancy_name',
                'city',
                'salary',
                'salary_from',
                'salary_to',
                'currency',
                'experience',
                'schedule',
                'employment',
                'description',
                'skills',
                'employer',
                'publish_date',
                'vacancy_url',
                'has_test']
    
    # создание итоговой таблицы
    df = pd.DataFrame(columns = columns)
    
    print(f'\nStart processing {len(ids)} job vacancies ')
    # Используем tqdm для отслеживания прогресса
    with tqdm(total=len(ids), desc='Processing vacancies') as pbar:
        for i, vacancy_id in enumerate(ids):
            # запрос данных по вакансии по найденному id
            data = requests.get(url + vacancy_id).json()
            # заполнение данными 1 строки в итоговой таблице
            parsed_data = json.loads(json.dumps(data))
            if 'errors' in parsed_data:
                print('!!! Request limit exceeded, CAPTCHA required !!!')
                break
            df.loc[i] = fill_row(data)
            pbar.update(1)  # Обновляем прогресс-бар

    print(f'\nAdded {len(df)} vacancies')
    return df