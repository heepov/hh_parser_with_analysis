import requests
from tqdm import tqdm

# принимает: 
# 'job_title' - название (или ключевые слова) для поиска вакансий
# 'pages_number' - количество страниц с вакансиями (pages_number * 100 - всего вакансий)
# 'area' - регион для поиска вакансий
# 'url' - адрес API

# возвращает:
# список со всеми id вакансий по заданным параметрам

def find_ids(job_title, vacancies_per_page=100, pages_number=20, first_page=0, area=113, url = 'https://api.hh.ru/vacancies/'):
    # список в который добавляем все найденные id
    ids = []
    # счетчик для вывода на экран прогресса обработки
    count = 0
    # проверка не выходит количество страниц с вакансиями за предельное значение
    if pages_number > 20:
        pages_number = 20
    # проверка не выходит ли количество вакансий на странице за предельное значение
    if vacancies_per_page > 100:
        vacancies_per_page = 100
    
    # подсчет общего исследуемых количества вакансий
    ids_sum = pages_number * vacancies_per_page
    
    print(f'Start finding maximum {ids_sum} id\'s job vacancies ')
    # проходимся по заданному количеству страниц с вакансиями
    for page in tqdm(range(first_page, pages_number+first_page), desc='Finding id\'s'):
        # задаем параметры за запроса
        par = {'text': job_title, 'area': area, 'per_page': vacancies_per_page, 'page':page , 'search_field':"name"}
        # делаем запрос
        r = requests.get(url, params=par)        
        e = r.json()
        # поиск всех id на одной странице и добавление их в список ids
        if(len(e['items']) == 0): break
        
        for vac in range(len(e['items'])):
            count += 1
            try:
                ids.append(e['items'][vac].get('id'))
            except:
                print('Going beyond the allowed number of vacancies!')
                print(f'Uploaded {len(ids)} vacancies')
                return ids

    print('\nEverything OK')
    print(f'Uploaded {len(ids)} vacancies')
    
    return ids
