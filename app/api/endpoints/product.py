from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utils import get_json_from_card_wb
from app.api.validators import check_article_duplicate
from app.core.db import get_async_session
from app.crud.product import product_crud
from app.schemas.product import ProductCreate, ProductDB

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
    product_dict = await get_json_from_card_wb(product.article)
    duplicate = await check_article_duplicate(product.article, session)
    if duplicate:
        product = await product_crud.get_by_attribute(
            'article', product.article, session
        )
        new_product = await product_crud.update(product, product_dict, session)
    else:
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
