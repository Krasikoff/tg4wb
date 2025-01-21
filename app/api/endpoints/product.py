from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.product import ProductBase, ProductCreate, ProductDB
from app.api.utils import get_json_from_card_wb
from app.models import Product
from app.crud.product import product_crud


router = APIRouter()


@router.post(
    '/',
    response_model=ProductDB,
    response_model_exclude_none=True,
)
async def create_new_product(
        product: ProductCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Создание нового task."""
    print('================================', product.article)
    # проверка на дупликат артикула
    product_dict = await get_json_from_card_wb(product.article)
    if product_dict is None:
        raise HTTPException(
            status_code=422,
            detail='Продукт не может иметь значение None.'
        )
    new_product = await product_crud.create(product_dict, session)
    return new_product


@router.get(
    '/',
    response_model=list[ProductBase],
    response_model_exclude_none=True,
)
async def get_all_products(
        session: AsyncSession = Depends(get_async_session),
):
    "Все."
    all_tasks = await Product.get_multy(
        session=session,
    )
    return all_tasks
