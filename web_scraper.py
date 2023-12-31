from bs4 import BeautifulSoup as bs
import sqlite3 as sl
import pandas as pd
import requests
from context_manager import SQLiteConnection

def df_filling(df, item_group, cat):
    for items in item_group:
        name = items.find('div', class_='link-wrap').text
        old_price = int(items.find('mark', class_='old-price').text[:-3].replace(' ', ''))
        new_price = int(items.find('mark', class_='price').text[:-3].replace(' ', ''))
        discount = int(100 - round(new_price / old_price * 100, 0))
        item_info = [name.strip(), old_price, new_price, cat, discount]
        length = len(df)
        df.loc[length] = item_info


if __name__ == '__main__':
    url = 'https://airsoft-rus.ru/'
    req = requests.get(url)
    bsObject = bs(req.text, "html.parser")

    data = bsObject.find_all('section', class_='popular-section')
    sales = data[0].find_all('div', class_='item')
    hits = data[2].find_all('div', class_='item')

    df = pd.DataFrame(columns=['Товар', 'Старая_цена', 'Новая_цена', 'Категория', 'Скидка'])

    df_filling(df, sales, "Распродажа")
    df_filling(df, hits, "Хит продаж")

    with SQLiteConnection('items.db') as con:
        df.to_sql(name='items', con=con, if_exists='append', index=False)





