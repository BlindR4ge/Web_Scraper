from flask import Flask, render_template as rt, request
import sqlite3 as sl
import os
import time


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


app = Flask(__name__)


@app.route('/', methods=["get", "post"])
def home():
    return rt('homepage.html')


@app.route('/result', methods=["get"])
def result():
    cat = request.args.get('hidden')
    with SQLiteConnection('items.db') as con:
        cat_min_price = con.execute("SELECT MIN(Новая_цена) FROM items WHERE Категория = ?", (cat,)).fetchone()
        output = con.execute("SELECT Товар, Новая_цена, Скидка FROM items WHERE Категория = ? AND Новая_цена = ?",
                             (cat, cat_min_price[0])).fetchone()
        print(f'''Товар: {output[0]}\nЦена с учетом скидки : {output[1]}р.\nСкидка: {output[2]}%''')
    return rt("resultpage.html", item=output[0], price=output[1], discount=output[2])


if __name__ == '__main__':
    os.system("python sql-generator.py")
    time.sleep(25)
    os.system("python web_scraper.py")
    time.sleep(60)
    app.run(port=5000)
