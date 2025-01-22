from app.crud.base import CRUDBase
from app.models import Product

class CRUDProduct(CRUDBase):
    async def get_subscribe_list():
        pass

product_crud = CRUDProduct(Product)
