"""Модуль схем product."""
from typing import Optional

from pydantic import BaseModel, PositiveInt, PositiveFloat, Field


class ProductBase(BaseModel):
    article: str


class ProductDB(ProductBase):
    """Класс схемы."""
    name: str 
    article: str
    descr: Optional[str] | None = None
    brand: Optional[str] | None = None
    price: Optional[PositiveFloat] = 0
    sale_price: Optional[PositiveFloat] = 0
    raiting: Optional[PositiveFloat] = 0
    total_quantity: Optional[PositiveInt] = 0 
    
    class Config:
        from_attributes = True

class ProductCreate(ProductBase):
    ...
