import requests


async def get_json_from_card_wb(article: str):
    url = (
        'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786'
        f'&spp=30&nm={article}'
    )
    print(url)
    json_data = requests.get(url).json()   # 211695539
    try:
        original_json = json_data['data']['products'][0]
        key_mapping = {
            'name': 'name',
            'id': 'article',
            'descr': 'name',
            'brand': 'brand',
            'priceU': 'price',
            'salePriceU': 'sale_price',
            'rating': 'rating',
            'totalQuantity': 'total_quantity'
        }
        updated_json = {
            key_mapping.get(
                key, key): value for key, value in original_json.items()
                if key in ['name', 'id', 'descr', 'brand', 'priceU',
                           'salePriceU', 'rating', 'totalQuantity']
        }
        return updated_json
    except Exception as e:
        print(e)
        return None
