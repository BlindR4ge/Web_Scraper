from bs4 import BeautifulSoup as bs
import sqlite3 as sl
import pandas as pd
import requests

class SQLiteConnection:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None

    def __enter__(self):
        self.connection = sl.connect(self.db_file)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()


def df_filling(item_group, cat):
    for items in item_group:
        name = items.find('div', class_='link-wrap').text
        old_price = int(items.find('mark', class_='old-price').text[:-3].replace(' ', ''))
        new_price = int(items.find('mark', class_='price').text[:-3].replace(' ', ''))
        discount = int(100 - round(new_price / old_price * 100, 0))
        item_info = [name.strip(), old_price, new_price, cat, discount]
        length = len(df)
        df.loc[length] = item_info


url = 'https://airsoft-rus.ru/'
req = requests.get(url)
bsObject = bs(req.text, "html.parser")


data = bsObject.find_all('section', class_='popular-section')
sales = data[0].find_all('div', class_='item')
hits = data[2].find_all('div', class_='item')

df = pd.DataFrame(columns=['Товар', 'Старая_цена', 'Новая_цена', 'Категория', 'Скидка'])

df_filling(sales, "Распродажа")
df_filling(hits, "Хит продаж")

with SQLiteConnection('../items.db') as con:
    df.to_sql(name='items', con=con, if_exists='append', index=False)

