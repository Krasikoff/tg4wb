import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utils import put_json_to_product
from app.core.db import get_async_session
from app.crud.product import product_crud
from app.schemas.product import ProductDB
from app.api.validators import article_cannt_be_negative
from app.core.user import current_user
from app.models import User

router = APIRouter()


@router.get(
    '/{product_article}',
    response_model=ProductDB,
)
async def get_start_subscribe(
        product_article: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),

):
    await article_cannt_be_negative(product_article)
    product_dict = await put_json_to_product(product_article)
    try:
        logging.info(product_dict['article'])
        product = await product_crud.get_by_attribute(
            'article', product_article, session
        )
        new_product = await product_crud.update(
            product, {'subscribe': True}, session
        )
        return new_product
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=e,
        )
