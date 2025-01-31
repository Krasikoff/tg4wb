import aiohttp
import asyncio
from app.core.config import settings


async def main():
    username = settings.first_superuser_email
    password = settings.first_superuser_password
    credentials = await login(username, password)
    access_token = credentials['access_token']
    headers = {
        'Authorization': f'Bearer {access_token}', 
        'Content-Type':'application/json'
    }
    url = 'https://unevenly-seasoned-cat.cloudpub.ru/api/v1/products/'

    async with aiohttp.ClientSession() as session:
        async with session.get(url,
            headers=headers,
            json={'article':'211695539'}
            ) as resp:
            response = await resp.json()
            print(response)


async def login(username: str, password: str) -> str:
    async with aiohttp.ClientSession() as session:
        url = 'https://unevenly-seasoned-cat.cloudpub.ru/auth/jwt/login'
        async with session.post(
            url,
            data={'username': username, 'password': password}
            ) as resp:
            data = await resp.json()
            try:
                data['access_token']
                print(data)
                return data
            except Exception as e:
                print(e)
                return None

asyncio.run(main())