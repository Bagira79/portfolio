def processing_str(listing_str: list) -> list:
    """Функция обрабатывает строковые данные, полученные с сайта, приводя в подходящий для вставки в датафрейм вид.
    :return list"""
    listing = listing_str[0].replace(',', ';').split(';')
    new_listing = list(listing[k].strip() for k in range(10))
    return new_listing


def processing_int_float(listings: list) -> list:
    """Функция приводит числовые данные, полученные в виде строк, к нужным типам (int, float)
    :return list"""

    new_listing_data = []
    for i in range(10):
        if i == 2 or i == 7:
            listings[i] = int(listings[i])
        elif i == 8:
            listings[i] = float(listings[i])
        elif i == 9 and (listings[9] != 'null'):
            listings[i] = float(listings[i])
        elif i == 9 and (listings[9] == 'null'):
            listings[i] = 0.0
        new_listing_data.append(listings[i])

    return new_listing_data


def purchase(types: str, cnt: int, price: float) -> float:
    """Функция рассчитывает стоимость закупки товаров.
    :return float"""
    if types == 'purchase order':
        purchase_price = cnt * price
    else:
        purchase_price = 0.0
    return purchase_price


def price_markups(types: str, selling_price: float, price: float) -> float:
    """Функция рассчитывает товарную наценку в процентах.
    :return float"""
    if types == 'sales invoice':
        price_markup = round((selling_price - price) / price * 100, 2)
    else:
        price_markup = 0.0
    return price_markup
