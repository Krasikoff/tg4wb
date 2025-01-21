import requests


async def get_json_from_card_wb(article: str):
    json_data = requests.get('https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm=211695539').json()
    if len(json_data):
        product = json_data['data']['products']
        print(product)
        return product
    else:
        print(json_data)
        return None