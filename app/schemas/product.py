"""Модуль схем product."""
from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    article: str


class ProductDB(ProductBase):
    """Класс схемы."""
    name: str
    article: str
    descr: Optional[str] | None = None
    brand: Optional[str] | None = None
    price: Optional[float] = 0
    sale_price: Optional[float] = 0
    rating: Optional[float] = 0
    total_quantity: Optional[int] = 0

    class Config:
        from_attributes = True


class ProductCreate(ProductBase):
    ...
