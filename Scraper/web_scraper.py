from bs4 import BeautifulSoup as bs
import requests
import config
from Database import Market_Bin
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import time

market_list = []

def df_filling(item_group, cat, market_list):
    for items in item_group:
        name = items.find('div', class_='link-wrap').text
        old_price = int(items.find('mark', class_='old-price').text[:-3].replace(' ', ''))
        new_price = int(items.find('mark', class_='price').text[:-3].replace(' ', ''))
        discount = int(100 - round(new_price / old_price * 100, 0))
        item_info = [name.strip(), old_price, new_price, cat, discount]
        market_list.append(item_info)


time.sleep(15)

engine = create_engine(config.DATABASE_CONNECTION_URI)
engine.connect()
session = Session(engine)

while(True):
    url = 'https://airsoft-rus.ru/'
    req = requests.get(url)
    bsObject = bs(req.text, "lxml")

    data = bsObject.find_all('section', class_='popular-section')
    sales = data[0].find_all('div', class_='item')
    hits = data[2].find_all('div', class_='item')

    df_filling(sales, "Распродажа", market_list)
    df_filling(hits, "Хит продаж", market_list)

    for item in market_list:
        tovar = Market_Bin(item=item[0], old_price=item[1], new_price=item[2], category=item[3], discount=item[4])
        result = session.query(Market_Bin)
        print(result)
        if (result == None):
            session.add(Market_Bin)
            session.commit()
    time.sleep(100)

