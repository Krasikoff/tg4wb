from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.product import ProductBase, ProductCreate, ProductDB
from app.api.utils import get_json_from_card_wb
from app.models import Product
from app.crud.product import product_crud
from app.api.validators import check_article_duplicate


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
    """Запись полученного по артиклю с wb товара."""
    await check_article_duplicate(product.article, session)
    product_dict = await get_json_from_card_wb(product.article)
    new_product = await product_crud.create(product_dict, session)
    return new_product


@router.get(
    '/',
    response_model=list[ProductDB],
    response_model_exclude_none=True,
)
async def get_all_products(
        session: AsyncSession = Depends(get_async_session),
):
    "Все записанные товары."
    all_tasks = await product_crud.get_multi(
        session=session,
    )
    return all_tasks
