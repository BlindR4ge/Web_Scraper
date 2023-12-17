from db_config import db
from sqlalchemy import func


def select(model, cat):
    min_price = db.session.query(func.min(model.new_price)).filter(model.category == cat).scalar()
    product_info = db.session.query(model).filter(model.category == cat, model.new_price == min_price).first()
    if product_info:
        return product_info.item, min_price, product_info.discount
    else:
        return None


def add_instance(model, **kwargs):
    instance = model(**kwargs)
    db.session.add(instance)
    commit_changes()


def delete_instance(model, id):
    model.query.filter_by(id=id).delete()
    commit_changes()


def edit_instance(model, id, **kwargs):
    instance = model.query.filter_by(id=id).all()[0]
    for attr, new_value in kwargs.items():
        setattr(instance, attr, new_value)
    commit_changes()


def commit_changes():
    db.session.commit()