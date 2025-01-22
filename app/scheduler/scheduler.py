from fastapi import Depends
from app.crud.product import product_crud
from app.core.db import get_async_session, AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

async def upd_data_to_db():
    print('Scheduler working!')
    try:
        async with AsyncSessionLocal as session:
            list_product = await product_crud.get_multi(session)
            print(list_product)
    except Exception as e:
        print(e)

