import ids_finder
import date_create
import data_processing

# адрес API
url = 'https://api.hh.ru/vacancies/'
# ключевое слово (или название) для поиска в названия вакансий
job_title = ['Android']
# количество вакансий на странице (максимум 100)
vacancies_per_page = 100
# количество страниц с вакансиями (максимум 20)
pages_number = 20
# с какой страницы начинается поиск вакансий
first_page = 0
# район поиска 
area = 113
# название фала для записи данных
saving_file_name = 'hh_result.csv'

# поиск id вакансий по заданному запросу
ids = ids_finder.find_ids(job_title, vacancies_per_page, pages_number, first_page, area, url)
# создание таблицы с данными
df = date_create.create_df(ids, url)
# обработка данных в таблице
df = data_processing.table_processing(df)
# запись данных в файл
df.to_csv(saving_file_name,index = False)