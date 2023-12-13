from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class MarketBin(db.Model):
    __tablename__ = 'Bin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item = db.Column(db.String(255))
    old_price = db.Column(db.Integer)
    new_price = db.Column(db.Integer)
    category = db.Column(db.String(100))
    discount = db.Column(db.Integer)
