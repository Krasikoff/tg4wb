"""Модуль схем product."""
import logging
from typing import Optional

from pydantic import BaseModel, field_validator


class ProductBase(BaseModel):
    """Класс схемы базовый."""
    article: int


class ProductDB(ProductBase):
    """Класс схемы."""
    name: str
    article: int
    descr: Optional[str] | None = None
    brand: Optional[str] | None = None
    price: Optional[float] = 0
    sale_price: Optional[float] = 0
    rating: Optional[float] = 0
    total_quantity: Optional[int] = 0
    subscribe: bool = False

    class Config:
        from_attributes = True


class ProductCreate(ProductBase):
    """Валидация значения артикля при создании."""
    @field_validator('article')
    def article_cannt_be_negative(cls, value: str):
        try:
            if 2147483648 < int(value) or int(value) <= 0:
                raise ValueError('Значение article не правильное.')
            return int(value)
        except (ValueError, TypeError):
            raise ValueError(
                'Значение "article" не может быть отрицательным, 0 '
                'и больше 2147483648.'
            )
        except Exception as e:
            logging(e)
