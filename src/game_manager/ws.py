import aiohttp

import asyncio

from config import settings
from game_manager.manager import Manager


async def produce(manager: Manager, ws):
    while True:
        await manager.new_data_for_back.wait()
        while manager.data_for_back:
            data = manager.data_for_back.pop(0)
            await ws.send_json(data)
        manager.new_data_for_back.clear()


async def receive(manager: Manager, ws):
    while True:
        manager.last_updates.append(await ws.receive_json())
        manager.new_update_event.set()


async def connect_to_ws(manager: Manager):
    ws_url = 'wss:' + settings.API_URL.split(':')[1] + f'/ws/{manager.lobby_title}?user={manager.user}'
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(ws_url) as ws:
            await asyncio.gather(produce(manager, ws), receive(manager, ws))
