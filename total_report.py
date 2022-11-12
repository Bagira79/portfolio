import pdfkit
from jinja2 import Template
import binascii


def reporting(gross_profit, data_price_markup_min_max, data_total_remains, data_lost_funds, data_additional_funds, profit_manufacturer, min_2000, min_2001, min_2002, min_2003):
    """Функция формирует итоговый отчет по результатам анализа данных магазина за 2000 - 2003 год.
    :return None"""

    with open('gross_profit.png', 'rb') as file:
        img = 'data:image/png;base64,' + binascii.b2a_base64(file.read(), newline=False).decode("UTF-8")
    with open('data_total_remains_graf.png', 'rb') as file2:
        img2 = 'data:image/png;base64,' + binascii.b2a_base64(file2.read(), newline=False).decode("UTF-8")
    with open('profit_manufacturer_2002.png', 'rb') as file3:
        img3 = 'data:image/png;base64,' + binascii.b2a_base64(file3.read(), newline=False).decode("UTF-8")

    html_template = '''<html>
    <head>
        <title>Отчет</title>
        <meta charset="utf-8"/>
    </head>
    <body>
        <h1 style="font-style: normal; font-weight: 600; font-size: 25px; line-height: 20px; text-align: center;  margin-bottom: 50px">Отчет по анализу деятельности магазина "Ваш ремонт" с 2000 по 2003 гг.</h1>
        <p style="font-size: 20px;  margin-bottom: 20px">Рассмотрим распределение валовой прибыли по годам.</p>
        <p style="text-align: center"><img src="{{data.image1}}" alt="Распределение валовой прибыли" style="width: 60%; margin-bottom: 40px"></p>
        <h2 style="font-style: normal; font-weight: 600; font-size: 18px; line-height: 18px; text-align: left">Таблица 1. Данные по распределению валовой прибыли по годам</h2>
        <div>{{data.table1}}</div>
        <p style="font-size: 20px">Как видно из данных таблицы 1, валовая прибыль за 2000 г. очень низкая, а в 2003 г. магазин понес убытки. Величина  наценки на стоимость товаров приведена в таблице 2. </p>
        <h2 style="font-style: normal; font-weight: 600; font-size: 18px; line-height: 18px; text-align: left">Таблица 2. Данные по величине торговой наценки</h2>
        <div>{{data.table2}}</div>
        <p style="font-size: 20px">Согласно данным таблицы 2, минимальная величина  наценки на стоимость товара в 2000 г. составляет {{num1}}%, в 2001 г. - {{num2}}%, в 2002 г. - {{num3}}%, в 2003 г. - {{num4}}%. Все реализованные товары были проданы по цене выше закупочной. Рассмотрим распределение остатков товаров по каждому году.</p>
        <p style="text-align: center"><img src="{{data.image2}}" alt="Распределение остатков товаров по годам" style="width: 100%; margin-bottom: 40px"></p>
        <h2 style="font-style: normal; font-weight: 600; font-size: 18px; line-height: 18px; text-align: left">Таблица 3. Распределение остатков товаров по годам</h2>
        <div>{{data.table3}}</div>
        <p style="font-size: 20px">Вследствие наличия большого количества остатков  были недополучены средства в размере, указанном в таблице 4.</p>
        <h2 style="font-style: normal; font-weight: 600; font-size: 18px; line-height: 18px; text-align: left">Таблица 4. Недополученные средства по годам</h2>
        <div>{{data.table4}}</div>
        <p style="font-size: 20px">Существенное увеличение валовой прибыли в 2001 и 2002 гг. связано с продажей остатков продукции, приобретенной в прошлые годы. Данные приведены в таблице 5.</p>
        <h2 style="font-style: normal; font-weight: 600; font-size: 18px; line-height: 18px; text-align: left">Таблица 5. Дополнительные средства по годам от продажи товаров, приобретенных в прошлые периоды</h2>
        <div>{{data.table5}}</div>
        <p style="font-size: 20px">Вклад в валовую прибыль  продукции различных производителей, приведен в таблице 6.</p>
        <p style="text-align: center"><img src="{{data.image3}}" alt="Распределение валовой прибыли по производителям в 2002 г." style="width: 80%; margin-bottom: 40px"></p>
        <h2 style="font-style: normal; font-weight: 600; font-size: 18px; line-height: 18px; text-align: left">Таблица 6. Соотношение вклада в валовую прибыль продукции различных производителей</h2>
         <div>{{data.table6}}</div>
         <p style="font-size: 20px">На основании вышеизложенного, можно сделать вывод, что продукция компании Rockwool(partial fill cavity slab 50, rockclose insulated dpc 30) и Knauf (uniflott) не пользуется спросом у покупателей. Рекомендуется исключить дальнейшую закупку указанной продукции.</p>
    </body>
    </html>'''

    html = Template(html_template).render(data={'image1': img,
                                                'table1': gross_profit.to_html(),
                                                'image2': img2,
                                                'image3': img3,
                                                'table2': data_price_markup_min_max.to_html(),
                                                'table3': data_total_remains.to_html(),
                                                'table4': data_lost_funds.to_html(),
                                                'table5': data_additional_funds.to_html(),
                                                'table6': profit_manufacturer.to_html()},
                                          num1=min_2000,
                                          num2=min_2001,
                                          num3=min_2002,
                                          num4=min_2003)

    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    options = {
        'page-size': 'A4',
        'header-right': '[page]',
        "enable-local-file-access": ""
    }
    pdfkit.from_string(html, 'total.pdf',
                       configuration=config, options=options)
    return
