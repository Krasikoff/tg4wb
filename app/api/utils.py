import logging

import aiohttp
import requests
from fastapi import HTTPException


async def get_json_from_card_wb(article: str):
    url = (
        'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786'
        f'&spp=30&nm={article}'
    )
    json_data = requests.get(url).json()
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
                key, key
            ): value for key, value in original_json.items(
            ) if key in [
                'name', 'id', 'descr', 'brand', 'priceU',
                'salePriceU', 'rating', 'totalQuantity'
            ]
        }
        return updated_json
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=422,
            detail='Продукт не может иметь значение None.'
        )


async def put_json_to_product(article: str):
    "Обращение к нашему api для получения данных по товару."
    url = ('http://localhost:8000/products/')
    data = {"article": article}
    auth = aiohttp.BasicAuth(login='z1r0-d@yandex.ru', password='111')
    async with aiohttp.ClientSession(auth=auth) as session:
        response = await session.post(url, json=data)
        json_data = await response.json()
        try:
            logging.info(json_data['article'])
        except KeyError:
            logging.info(json_data['detail'])
        except Exception as e:
            logging.info(e)
        finally:
            logging.info(json_data)
            return json_data
