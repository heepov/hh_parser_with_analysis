import pandas as pd

# принимает:
# 'df' - таблица в которой обрабатываются данные

# возвращает:
# итоговая таблица с обработанными данными

def table_processing(df): 
    # смена типа данных в столбцах 'id', 'salary_from', 'salary_to' на int
    for col in ['id', 'salary_from', 'salary_to']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].astype(int, errors='ignore')
    
    # смена типа данных в столбцах 'premium', 'salary', 'has_test' на bool 
    for col in ['premium', 'salary', 'has_test']:
        df[col] = df[col].astype(bool, errors='ignore')
        
    # замена значения валюты с 'RUR' на 'RUB'
    df['currency'] = df['currency'].replace({'RUR':'RUB'}, regex=True)
    
    # приводим столбец 'publish_date' к типу данных date_time
    df['publish_date'] = pd.to_datetime(df['publish_date'], format='%Y-%m-%dT%H:%M:%S')
    
    # возвращаем итоговую таблицу с обработанными данными
    return df