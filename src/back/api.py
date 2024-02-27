from aiohttp import ClientSession

from config import settings


async def get_lobbies():
    url = settings.API_URL + '/lobby'
    async with ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
        

async def create_lobby(user_id: int, title: str, password: str|None = None):
    url = settings.API_URL + '/lobby' + f'?user={user_id}'
    async with ClientSession() as session:
        async with session.post(url, json={'title': title, 'password': password}) as response:
            return response.status


async def entry_to_lobby(user_id: int, lobby_title: str, password: str|None = None):
    url = settings.API_URL + f'/lobby/{lobby_title}/add' + f'?user={user_id}'
    async with ClientSession() as session:
        async with session.patch(url, json={'password': password}) as response:
            return response.status


async def del_from_lobby(user_id: int, lobby_title: str):
    url = settings.API_URL + f'/lobby/{lobby_title}/del' + f'?user={user_id}'
    async with ClientSession() as session:
        async with session.patch(url) as response:
            return response.status
