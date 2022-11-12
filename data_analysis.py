import matplotlib.pyplot as plt
import pandas as pd
from functions import purchase, price_markups
import binascii

pd.options.display.max_columns = 15
pd.set_option('display.width', 1600)
pd.set_option('display.max_rows', 800)


def data_analysis(data_all):
    data_all['year'] = pd.to_datetime(data_all.dt).dt.year

    data_all['dt'] = pd.to_datetime(data_all.dt).dt.strftime('%d:%m:%Y')
    '''Рассчитаем стоимость закупки товаров'''
    data_all['purchase_price'] = data_all.apply(lambda x: purchase(x.order_type, x.cnt, x.price), axis=1)
    '''Рассчитаем выручку'''
    data_all['revenue'] = data_all['cnt'] * data_all['selling_price']

    '''Рассчитаем наценку'''
    data_all['price_markup'] = data_all.apply(lambda x: price_markups(x.order_type, x.selling_price, x.price), axis=1)

    data_all.rename(
        columns={'dt': 'Дата', 'year': 'Год', 'order_number': 'Номер документа', 'order_type': 'Тип документа',
                 'product_category': 'Категория продукта', 'product': 'Продукт',
                 'manufacturer': 'Производитель', 'cnt': 'Количество', 'price': 'Цена',
                 'selling_price': 'Цена продажи', 'price_markup': 'Наценка, %',
                 'purchase_price': 'Стоимость закупки', 'revenue': 'Выручка'},
        inplace=True)
    data_all.to_excel('Общие данные.xlsx', sheet_name='Исходные данные', index=False, encoding='utf-8')
    # print(data_all)

    '''Определим количество закупленной продукции по годам'''
    data_cnt_purchase = \
        data_all[data_all['Тип документа'] == 'purchase order'].groupby(['Год', 'Производитель', 'Продукт']).sum()[
            ['Количество']]
    data_cnt_purchase.rename(columns={'Количество': 'Количество закупленных шт'}, inplace=True)
    # print(data_cnt_purchase)
    '''Определим количество проданной продукции по годам'''
    data_cnt_sales = \
        data_all[data_all['Тип документа'] == 'sales invoice'].groupby(['Год', 'Производитель', 'Продукт']).sum()[
            ['Количество']]
    data_cnt_sales.rename(columns={'Количество': 'Количество проданных шт'}, inplace=True)
    # print(data_cnt_sales)
    data_cnt = pd.merge(data_cnt_purchase, data_cnt_sales, left_index=True, right_index=True, how='outer')
    data_cnt.fillna(0, inplace=True)
    '''Рассчитаем остатки товаров по годам'''
    data_cnt['Остатки'] = data_cnt['Количество закупленных шт'] - data_cnt['Количество проданных шт']
    # print(data_cnt)
    '''Рассчитаем выручку от продажи товаров по годам'''
    data_revenue = \
        data_all[data_all['Тип документа'] == 'sales invoice'].groupby(['Год', 'Производитель', 'Продукт']).sum()[
            ['Выручка']]
    # print(data_revenue)
    '''Рассчитаем стоимость закупки товаров по годам'''
    data_purchase = \
        data_all[data_all['Тип документа'] == 'purchase order'].groupby(['Год', 'Производитель', 'Продукт']).sum()[
            ['Стоимость закупки']]
    # print(data_purchase)
    data_money = pd.merge(data_purchase, data_revenue, left_index=True, right_index=True, how='outer')
    data_money.fillna(0.0, inplace=True)
    data_total = pd.merge(data_cnt, data_money, left_index=True, right_index=True, how='outer')
    data_total.fillna(0.0, inplace=True)

    data_total_gross_profit = data_total.groupby('Год').sum()[['Стоимость закупки', 'Выручка']]
    data_total['Валовая прибыль'] = data_total['Выручка'] - data_total['Стоимость закупки']
    # print(data_total)
    '''Рассчитаем недополученные из-за наличия остатков средства '''
    lost_funds = data_total[data_total['Валовая прибыль'] < 0]
    # print(lost_funds)
    lost_funds.reset_index(inplace=True)
    data_lost_funds = lost_funds.groupby('Год').sum().apply(lambda x: abs(x))
    data_lost_funds.rename(columns={'Валовая прибыль': 'Недополученные средства'}, inplace=True)
    # print(data_lost_funds)
    '''Рассчитаем средства, полученные от продажи остатков товаров, закупленных в прошлые периоды'''
    additional_funds = data_total[data_total['Количество закупленных шт'] < data_total['Количество проданных шт']]
    data_additional_funds = additional_funds.groupby('Год').sum()[['Валовая прибыль']]
    data_additional_funds.rename(columns={'Валовая прибыль': 'Средства от продажи остатков товаров за прошлые периоды'},
                                 inplace=True)
    # print(data_additional_funds)
    '''Рассчитаем валовую прибыль по годам'''
    gross_profit = data_total.groupby(['Год']).sum()[['Валовая прибыль']]
    # print(gross_profit)
    '''Рассчитаем валовую прибыль по годам по производителю и продукту'''
    gross_profit_manufacturer = data_total.groupby(['Год', 'Производитель', 'Продукт']).sum()[['Валовая прибыль']]
    # print(gross_profit_manufacturer)
    gross_profit_manufacturer.reset_index(inplace=True)
    """Рассчитаем вклад каждого производителя в валовую прибыль"""
    profit_manufacturer = gross_profit_manufacturer.groupby(['Год', 'Производитель']).sum()[['Валовая прибыль']]
    # print(profit_manufacturer)
    profit_manufacturer_2001 = gross_profit_manufacturer[gross_profit_manufacturer['Год'] == 2001]
    profit_manufacturer_2001 = profit_manufacturer_2001.groupby('Производитель').sum()['Валовая прибыль']
    # print(profit_manufacturer_2001)
    profit_manufacturer_2002 = gross_profit_manufacturer[gross_profit_manufacturer['Год'] == 2002]
    profit_manufacturer_2002 = profit_manufacturer_2002.groupby('Производитель').sum()['Валовая прибыль']
    # print(profit_manufacturer_2002)
    '''Рассчитаем остатки товаров по годам'''
    data_total_remains = data_total.groupby(['Год', 'Производитель', 'Продукт']).sum()[
        ['Количество закупленных шт', 'Остатки']]

    data_total_remains = data_total_remains[data_total_remains['Остатки'] > 0.0]
    """Для построения диаграммы"""
    data_total_remains_graf = data_total_remains.groupby(['Год', 'Продукт']).sum()[
        ['Количество закупленных шт', 'Остатки']]

    plt.rcParams.update({'figure.autolayout': True})
    fig1 = plt.figure(figsize=(10, 8))
    ax1 = fig1.add_subplot(1, 1, 1)
    data_total_remains_graf.plot.barh(ax=ax1)
    labels = ax1.get_xticklabels()
    plt.setp(labels, horizontalalignment='right')
    plt.title('Распределение остатков товаров', fontsize=16, fontname='Arial')
    plt.ylabel('Год, наименование товара', fontsize=14, fontname='Arial')
    plt.xlabel('Количество', fontsize=14, fontname='Arial')
    plt.savefig('data_total_remains_graf.png')
    # plt.show()
    '''Определим процент непроданных товаров'''
    data_total_remains['%'] = round(
        data_total_remains['Остатки'] / data_total_remains['Количество закупленных шт'] * 100,
        2)
    # print(data_total_remains)
    data_total_remains.sort_index(axis=1)
    data_total_remains.reset_index(inplace=True)

    """Определим минимальную и максимальную наценку на товары по годам"""
    data_price_markup_min_max = pd.pivot_table(data_all[data_all['Тип документа'] == 'sales invoice'],
                                               index=['Год', 'Производитель', 'Продукт'], values='Наценка, %',
                                               aggfunc=['min', 'max'])
    # print(data_price_markup_min_max)
    data_price_markup_min_max.reset_index(inplace=True)
    """Определим минимальную величину торговой наценки по годам"""
    data_price_markup_min_2000 = data_price_markup_min_max[data_price_markup_min_max['Год'] == 2000]
    data_price_markup_min_2001 = data_price_markup_min_max[data_price_markup_min_max['Год'] == 2001]
    data_price_markup_min_2002 = data_price_markup_min_max[data_price_markup_min_max['Год'] == 2002]
    data_price_markup_min_2003 = data_price_markup_min_max[data_price_markup_min_max['Год'] == 2003]
    min_2000 = float(data_price_markup_min_2000['min'].min())
    min_2001 = float(data_price_markup_min_2001['min'].min())
    min_2002 = float(data_price_markup_min_2002['min'].min())
    min_2003 = float(data_price_markup_min_2003['min'].min())
    # print(min_2000, min_2001, min_2002, min_2003)
    """Построим диаграмму распределения валовой прибыли  по годам"""
    fig2 = plt.figure(figsize=(6, 6))
    area2 = fig2.add_subplot(1, 1, 1)
    gross_profit.plot.bar(ax=area2, label="", color="#990033")
    area2.set_title("Распределение валовой прибыли по годам", fontsize=16, fontname='Arial')
    area2.set_xlabel("Год", fontsize=14, fontname='Arial')
    area2.set_ylabel("Валовая прибыль", fontsize=14, fontname='Arial')
    plt.savefig('gross_profit.png')
    # plt.show()
    gross_profit.reset_index(inplace=True)
    gross_profit['Валовая прибыль'] = gross_profit['Валовая прибыль'].apply(lambda x: round(x, 2))

    fig3 = plt.figure(figsize=(6, 6))
    area3 = fig3.add_subplot(1, 1, 1)
    profit_manufacturer_2002.plot.pie(ax=area3, label=' ', autopct='%1.1f%%')
    area3.set_title("Распределение валовой прибыли по производителям в 2002 г.", fontsize=14, fontname='Arial')
    plt.savefig('profit_manufacturer_2002.png')
    # plt.show()

    return gross_profit, data_price_markup_min_max, data_total_remains, data_lost_funds, data_additional_funds, profit_manufacturer, min_2000, min_2001, min_2002, min_2003
