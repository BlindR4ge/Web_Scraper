from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Market_Bin(Base):
    __tablename__ = 'Bin'
    id = Column(Integer, primary_key=True, autoincrement=True)
    item = Column(String(255))
    old_price = Column(Integer)
    new_price = Column(Integer)
    category = Column(String(100))
    discount = Column(Integer)
