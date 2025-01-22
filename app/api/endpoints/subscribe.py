from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.product import ProductDB, ProductCreate
from app.api.utils import get_json_from_card_wb
from app.schemas.subscribe import SubscribeBase
from app.crud.product import product_crud
from app.api.validators import article_cannt_be_negative
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter()


@router.get(
    '/{product_article}',
    response_model=ProductDB,
)
async def get_start_subscribe(
        product_article: int,
        session: AsyncSession = Depends(get_async_session),
):
    await article_cannt_be_negative(product_article)
    new_product = await product_crud.get_by_attribute('article', product_article, session)
    if new_product is None:
        product_dict = await get_json_from_card_wb(product_article)
        new_product = await product_crud.create(product_dict, session)
    new_product = await product_crud.update(new_product, {'subscribe': True}, session)
    return new_product

