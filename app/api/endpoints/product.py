from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utils import get_json_from_card_wb
from app.api.validators import check_article_duplicate
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.product import product_crud
from app.models import User
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
        user: User = Depends(current_user),
):
    """Запись полученного по артиклю с wb товара."""
    product_dict = await get_json_from_card_wb(product.article)
    duplicate = await check_article_duplicate(product.article, session)
    if duplicate:
        new_product = await product_crud.update(
            duplicate, product_dict, session
        )
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
    user: User = Depends(current_user),
):
    "Все записанные товары."
    all_tasks = await product_crud.get_multi(
        session=session,
    )
    return all_tasks
