from db_config import db
from flask_sqlalchemy import func


def find_user(model, **kwargs):
    user_info = model.query.filter_by(**kwargs).first()
    return user_info

def minimal(model, cat):
    min_price = model.query(func.min(model.new_price)).filter(model.category == cat).scalar()
    return min_price


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