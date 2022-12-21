import pandas as pd

#  'таблица лицевых счетов.xlsx'  'таблица платежей.xlsx'
file_name = 'таблица лицевых счетов.xlsx'

data_fr = pd.read_excel(file_name, header=0)


def data_missing(item) -> str:
    """Функция проверяет наличие и подсчитывает процент пропущенных значений в датафрейме.
    :return str"""
    text_list = []
    missing_values = ((item.isna().sum() / len(item)) * 100).sort_values()
    for i in missing_values.index:
        data = round(missing_values[i], 2)
        text_item = f'в столбце "{i}": {data} %'
        text_list.append(text_item)
    text_missing = ',\n'.join(text_list)
    text = f'пропущенных значений: \n' \
           f'{text_missing}'
    return text


def data_duplicated(item) -> str:
    """Функция определяет наличие дубликатов строк в датафрейме.
    :return str"""
    data = item.duplicated()
    data_result = data.value_counts()
    for i in data_result.index:
        if data_result[i] == len(item) and str(i) == 'False':
            text = 'дубликатов нет'
        elif str(i) == 'True':
            digit = data_result[i]
            text = f'количество дубликатов строк {digit}'

    return text


"""Определим наличие и количество пропусков в датафрейме"""
print(f'В файле {file_name} количество ', end=' ')
data_text_m = data_missing(data_fr)
print(data_text_m)
"""Определим наличие и количество дубликатов в датафрейме"""
print(f'В файле {file_name}', end=' ')
data_text_d = data_duplicated(data_fr)
print(data_text_d)
