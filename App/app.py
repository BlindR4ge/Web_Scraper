import time
from flask import render_template as rt, request
import App_generator
from db_config import MarketBin
import querySpecifier

time.sleep(10)

app = App_generator.create_app()



@app.route('/', methods=["get", "post"])
def home():
    return rt('homepage.html')


@app.route('/result', methods=["get"])
def result():
    cat = request.args.get('hidden')
    item = querySpecifier.find_user(MarketBin, category=cat, new_price=min(MarketBin.new_price))
    #cat_min_price = con.execute("SELECT MIN(Новая_цена) FROM items WHERE Категория = ?", (cat,)).fetchone()
    #output = con.execute("SELECT Товар, Новая_цена, Скидка FROM items WHERE Категория = ? AND Новая_цена = ?",
                                 #(cat, cat_min_price[0])).fetchone()
    return rt("resultpage.html", item=item[1], price=item[3], discount=item[5])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=30010, debug=True)
