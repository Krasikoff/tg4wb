from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.product import product_crud


async def check_article_duplicate(
        product_article: str,
        session: AsyncSession,
) -> None:
    product_id = await product_crud.get_by_attribute('article', product_article, session)
    if product_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Товар с таким артиклем уже существует!',
        )


async def article_cannt_be_negative(article: str):
        try:
            if 2147483648 < int(article) or int(article) <= 0:
                raise ValueError('Значение')
            return int(article)
        except (ValueError, TypeError) as e:
            raise HTTPException(
                 status_code=422,
                 detail='Значение "article" не может быть отрицательным, 0 и больше 2147483648.'
                 )      
