from flask import Flask, render_template as rt, request
import sqlite3 as sl
import os
from context_manager import SQLiteConnection

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
    return rt("resultpage.html", item=output[0], price=output[1], discount=output[2])


if __name__ == '__main__':
    os.system("python sql-generator.py")
    os.system("python web_scraper.py")
    app.run(port=5000, host='0.0.0.0')
