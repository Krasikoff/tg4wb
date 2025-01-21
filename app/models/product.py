"""Модуль модели."""
from sqlalchemy import Column, Integer, String, Text, Float
from app.core.db import Base


class Product(Base):
    """Класс модели."""
    name = Column(String(100), nullable=False)
    article = Column(String(30), nullable=False)
    descr = Column(Text())
    brand = Column(String(100), nullable=False)
    price = Column(Float, default=0)
    sale_price = Column(Float, default=0)
    raiting = Column(Float, default=0)
    total_quantity = Column(Integer, default=0)


    def __str__(self):
        return f'#{self.id} : {self.name} - {self.sale_price}'

    def __repr__(self):
        return (
            f' {self.name} - {self.sale_price}'
        )
