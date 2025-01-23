from app.api.utils import put_json_to_product
from app.crud.product import product_crud


async def upd_data_to_db() -> None:
    print('It works')
    list_product = await product_crud.get_subscribe_list()
    for product in list_product:
        await put_json_to_product(product.article)
