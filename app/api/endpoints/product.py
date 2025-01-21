from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import Status
from app.core.db import get_async_session
from app.schemas.product import ProductBase, ProductCreate, ProductDB
from app.api.utils import get_json_from_card_wb
from app.models import Product


router = APIRouter()


@router.post(
    '/',
    response_model=ProductDB,
    response_model_exclude_none=True,
)
async def create_new_product(
        product_article: ProductCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Создание нового task."""
    print('================================', product_article)
    new_product = await get_json_from_card_wb(product_article)
#    new_product = await Product.create(product, session)
    return new_product
#    return product

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
