from app.crud.product import product_crud
from app.api.utils import put_json_to_product


async def upd_data_to_db():
    print('Scheduler working!')
    list_product = await product_crud.get_subscribe_list()
    print('===', list_product)
    for product in list_product:
        await put_json_to_product(product.article)
        print('----', product.article)
