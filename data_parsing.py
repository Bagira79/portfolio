import requests
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv
import os.path
import mysql.connector
from functions import processing_str, processing_int_float

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

password = os.getenv('PASSWORD')
pd.options.display.max_columns = 15
pd.set_option('display.width', 1600)
pd.set_option('display.max_rows', 800)


# url = 'https://dbfiddle.uk/?rdbms=sqlserver_2017&fiddle=39bc85a5dbd3202671979645068f8ce0&hide=1'
def parsing(url):
    """Функция парсит дополнительные данные с сайта, выгружает данные из базы product и собирает их в один DataFrame.
    :return DataFrame"""

    response = requests.get(url)
    text = response.text
    html = BeautifulSoup(response.content, features="lxml")
    rows = []
    tbody = html.find('tbody')
    trs = tbody.find_all('tr')
    for tr in trs:
        text = [td.get_text() for td in tr.find('td')]
        norma = processing_str(text)
        norma_all = processing_int_float(norma)
        rows.append(norma_all)
    data = pd.DataFrame(rows,
                        columns=['dt', 'tm', 'order_number', 'order_type', 'product_category', 'product',
                                 'manufacturer',
                                 'cnt', 'price', 'selling_price'])

    data.drop(['tm'], axis='columns', inplace=True)

    data.to_excel('Дополнительные данные.xlsx', index=False)

    myconn = mysql.connector.connect(host="localhost", user="root", passwd=password, database="products")
    cursor = myconn.cursor()
    sql = """select od.dt, od.order_number, ot.order_type, pc.product_category,
    pr.product, man.manufacturer,  
    od.cnt, od.price, od.selling_price  
    from operations_data as od
    join manufacturer as man on od.manufacturer_id=man.manufacturer_id
    join order_type as ot on od.order_type_id=ot.order_type_id
    join product_category as pc on od.product_category_id=pc.product_category_id 
    join product as pr on od.product_id=pr.product_id"""
    cursor.execute(sql)
    result = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    cursor.close()
    myconn.close()
    data_list = list(map(lambda x: list(x), result))

    data2 = pd.DataFrame(data_list, columns=column_names)
    data2.fillna(0, inplace=True)
    data2.to_excel('Основные данные.xlsx', index=False)

    '''Дополним данные, взятые из базы данных products, данными с сайта https://dbfiddle.uk'''
    data_all = pd.concat([data, data2], axis=0, ignore_index=True)
    return data_all
