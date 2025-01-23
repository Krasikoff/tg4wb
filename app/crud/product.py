from sqlalchemy import select

from app.core.db import AsyncSessionLocal
from app.crud.base import CRUDBase
from app.models import Product


class CRUDProduct(CRUDBase):

    async def get_subscribe_list(self):
        stmt = select(Product).where(Product.subscribe)
        async with AsyncSessionLocal() as session:
            products = await session.scalars(stmt)
            return products.all()


product_crud = CRUDProduct(Product)
