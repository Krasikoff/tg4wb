"""Подключение роутеров."""
from fastapi import APIRouter

from app.api.endpoints import product_router, user_router

main_router = APIRouter()
main_router.include_router(
    product_router, prefix='/products', tags=['products']
)
main_router.include_router(user_router)
