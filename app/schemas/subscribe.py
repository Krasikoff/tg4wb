"""Модуль схем subscribe."""
from .product import ProductDB



class SubscribeBase(ProductDB):
    """Класс схемы."""    
    pass

    class Config:
        from_attributes = True
