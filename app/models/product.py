"""Модуль модели."""
from sqlalchemy import Boolean, Column, Float, Integer, String, Text

from app.core.db import Base


class Product(Base):
    """Класс модели базовый."""
    name = Column(String(100), nullable=False)
    article = Column(Integer, nullable=False, unique=True)
    descr = Column(Text())
    brand = Column(String(100), nullable=True)
    price = Column(Float, default=0)
    sale_price = Column(Float, default=0)
    rating = Column(Float, default=0)
    total_quantity = Column(Integer, default=0)
    subscribe = Column(Boolean, default=False)

    def __str__(self):
        return f'#{self.id} : {self.name} - {self.sale_price}'

    def __repr__(self):
        return (
            f' {self.name} - {self.sale_price}'
        )
