import pandas as pd
from numpy import mean
from numpy.ma import count


def avg_per_rep(item1, item2) -> float:
    """Функция вычисляет средний процент выкупов (с учетом возвратов).
    item1 : данные столбца Sales
    item2 : данные столбца Purchase
    :return avg_per"""
    avg_per = 0
    if item1 > 0:
        avg_per = (item1 - item2) / (item1 + item2) * 100

    return round(avg_per, 2)


def group_abc(amount_item: float) -> str:
    """Функция сортирует товары по группам ABC в зависимости от вклада товара.
    :return group"""
    group = ''
    if amount_item <= 80:
        group = 'A'
    elif amount_item <= 90:
        group = 'B'
    elif amount_item > 90:
        group = 'C'
    return group


def abc_test(pd_item, i_cat: str) -> list:
    """Функция проводит ABC анализ продаж товаров
    pd_item: обрабатываемый датафрейм
    i_cat:  категория 3 товара
    :return list
    """

    data_list = []
    data_category = pd_item[pd_item["Category3"] == i_cat]

    data_brands = pd.pivot_table(data_category,
                                 index=["Category1", "Category2", "Category3", "Brand"],
                                 values=["Sales"],
                                 aggfunc=[sum])

    data_brands.columns = data_brands.columns.droplevel(0)
    data_brands.reset_index(inplace=True)

    sorted_df = data_brands.sort_values(by='Sales', ascending=False)
    sorted_df['contribution'] = sorted_df['Sales'] / sorted_df['Sales'].sum() * 100
    sorted_df['cumulative_total_amount'] = sorted_df['contribution'].cumsum()

    sorted_df['group'] = sorted_df['cumulative_total_amount'].apply(group_abc)
    sorted_df_sum = pd.pivot_table(sorted_df,
                                   index=['group'],
                                   values=["Sales"],
                                   aggfunc=[sum])
    sorted_df_sum.columns = sorted_df_sum.columns.droplevel(0)
    sorted_df_sum.reset_index(inplace=True)

    data_list.append(i_cat)

    data_list.append(sorted_df_sum.loc[0, "Sales"])

    return data_list


pd.options.display.max_columns = 23
pd.set_option('display.width', 1800)
pd.options.display.max_rows = 500
data = pd.read_csv('Исходник.csv', sep=';', decimal=',', low_memory=False)
data_new = data['Category'].str.split('/', expand=True)
data_new.columns = ['Category1', 'Category2', 'Category3']
# print(data_new)
data_part = data[['Brand', 'Balance', 'Balance FBS', 'Average price', 'Sales', 'Revenue', 'Purchase']]
# print(data_part)
final_data = pd.concat([data_new, data_part], axis=1)
final_data['Count'] = final_data['Balance'] + final_data['Balance FBS'] + final_data['Sales']  # Количество товаров

final_data['Average_percentage_repurchases'] = final_data.apply(lambda x: avg_per_rep(x.Sales, x.Purchase),
                                                                axis=1)  # Средний процент выкупов (с учетом возвратов)

# print(final_data)

Category3_list = final_data['Category3'].unique()
Category3_list = list(Category3_list)

list_df = []

for i in Category3_list:
    data_df = abc_test(final_data, i)

    list_df.append(data_df)
# print(list_df)
df = pd.DataFrame(list_df, columns=['Category3', 'count_revenue_80'])  # Количество товаров, приносящих 80% выручки
df = df.sort_values(by='Category3')
# print(df)

final_data_count = pd.pivot_table(final_data,
                                  index=["Category1", "Category2", "Category3"],
                                  values=["Count", "Revenue", "Sales"],
                                  aggfunc=[sum])
# print(final_data_count)
final_data_count_brand = pd.pivot_table(final_data,
                                        index=["Category1", "Category2", "Category3"],
                                        values=["Brand"],
                                        aggfunc=[count])
# print(final_data_count_brand)

final_data_avg_price = pd.pivot_table(final_data,
                                      index=["Category1", "Category2", "Category3"],
                                      values=["Average price"],
                                      aggfunc=[mean])
# print(final_data_avg)
final_data_avg = pd.pivot_table(final_data,
                                index=["Category1", "Category2", "Category3"],
                                values=["Average_percentage_repurchases"],
                                aggfunc=[mean])
# print(final_data_avg)
final_data_all1 = pd.concat([final_data_count, final_data_count_brand], axis=1)
final_data_all2 = pd.concat([final_data_all1, final_data_avg_price], axis=1)
final_data_all = pd.concat([final_data_all2, final_data_avg], axis=1)
final_data_all.columns = final_data_all.columns.droplevel(0)
# print(final_data_all)
final_data_all.reset_index(inplace=True)
# print(final_data_all)

final_data_all['% sales'] = round((final_data_all['Sales'] / final_data_all['Count'] * 100), 2)  # % товаров с продажами
final_data_all['80% Revenue'] = (final_data_all['Revenue'] * 0.8).apply(int)  # 80% выручки
# print(final_data_all)
total = pd.merge(left=final_data_all, right=df, on='Category3', how='inner')
total['percent_revenue_80'] = total['count_revenue_80'] / total['Count'] * 100

total_all = total[total.columns[[0, 1, 2, 3, 5, 9, 7, 4, 10, 11, 12, 6, 8]]]
# print(total_all)
total_all.to_excel('total_wb.xlsx', index=False)
