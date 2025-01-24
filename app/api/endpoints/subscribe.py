from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utils import get_json_from_card_wb
from app.api.validators import (article_cannt_be_negative,
                                check_article_duplicate)
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.product import product_crud
from app.models import User
from app.schemas.product import ProductDB

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
    product_dict = await get_json_from_card_wb(product_article)
    duplicate = await check_article_duplicate(product_article, session)
    try:
        if duplicate:
            product_dict['subscribe'] = True
            new_product = await product_crud.update(
                duplicate, product_dict, session
            )
        else:
            product_dict['subscribe'] = True
            new_product = await product_crud.create(product_dict, session)
        return new_product
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=e,
        )
