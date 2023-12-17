#import psycopg2 as pg
import sqlite3 as sl

con = sl.connect('items.db')

with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS items
        (
            Товар TEXT,
            Старая_цена INTEGER,
            Новая_цена INTEGER,
            Категория TEXT,
            Скидка INTEGER
        );
    """)
con.close()
