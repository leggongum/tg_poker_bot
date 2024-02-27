from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import F

import asyncio

from back.api import get_lobbies, entry_to_lobby, create_lobby, del_from_lobby
from game_manager.manager import Manager
from game_manager.user_lobby_manager_map import user_manager
from game_manager.ws import connect_to_ws
from game_manager.callback import turn, raise_menu
from game_manager.receive import upload_update
from utils import main, form_lobbies_list, renew_message
from app import dp, bot



async def create_manager(user_id):
    try:
        await asyncio.gather(connect_to_ws(user_manager[user_id]), upload_update(user_manager[user_id]))
    except Exception as ex:
        del user_manager[user_id]
        await bot.send_message(user_id, 'You are disconnected from the lobby.')
        print(ex)



@dp.message(Command('start'))
async def start(message: Message):
    await message.answer('Hello!', reply_markup=main)


@dp.message(Command('lobbies'))
async def get_lobbies_tg(message: Message):

    lobbies_markup = form_lobbies_list(await get_lobbies())

    await renew_message(message.from_user.id, message.message_id, 'Current active lobbies:', lobbies_markup)


@dp.message(Command('del'))
async def del_me_from_lobby(message: Message):
    arr = message.text.split()
    try:
        title = arr[1]
    except:
        return await message.answer('Lobby title must be specified', show_alert=True)
    
    response_status = await del_from_lobby(message.from_user.id, title)
    match response_status:
        case 404:
            return await message.answer('Lobby is not exist', show_alert=True)
        case 204:
            return await message.answer('You have been removed from the lobby', show_alert=True)
        case _: 
            return await message.answer('Unknow error...', show_alert=True)


@dp.message(Command('add'))
async def add_me_to_lobby(message: Message):
    arr = message.text.split()
    try:
        title = arr[1]
    except:
        return await message.answer('Lobby title must be specified')
    try:
        password = arr[2]
    except IndexError:
        password = None
    
    response_status = await entry_to_lobby(message.from_user.id, title, password)
    match response_status:
        case 404:
            return await message.answer('Lobby is not exist')
        case 403:
            return await message.answer('Wrong password')
        case 204 | 200:
            pass
        case _: 
            return await message.answer('Unknow error...')

    user_manager[message.from_user.id] = Manager(message.from_user.id, title, message.message_id)

    asyncio.create_task(create_manager(message.from_user.id))
    
    manager = user_manager[message.from_user.id]
    manager.message_id = await renew_message(message.from_user.id, message.message_id, *manager.construct_tg_representation())


@dp.message(Command('create_lobby'))
async def create_lobby_(message: Message):
    arr = message.text.split()
    try:
        title = arr[1]
    except IndexError:
        return await message.answer('Lobby title must be specified. Like: /create_lobby <lobby_name> <password>')
    password=None
    try:
        password = arr[2]
    except IndexError:
        pass
    response_status = await create_lobby(message.from_user.id, title, password=password)

    match response_status:
        case 201 | 200:
            pass
        case 403:
            return await message.answer('Lobby with this title already exist. You may choose another title.')
        case _: 
            return await message.answer('Unknow error...')
        

    user_manager[message.from_user.id] = Manager(message.from_user.id, title, message.message_id)

    asyncio.create_task(create_manager(message.from_user.id))

    manager = user_manager[message.from_user.id]
    manager.message_id = await renew_message(message.from_user.id, message.message_id, *manager.construct_tg_representation())
    


@dp.callback_query(turn.filter(F.action=='raise'))
async def raise_(call: CallbackQuery):
    manager: Manager = user_manager[call.from_user.id]

    manager.message_id = await renew_message(manager.user, manager.message_id, manager.construct_tg_representation()[0], raise_menu)


@dp.callback_query(F.data.startswith('raise'))
async def raise_by(call: CallbackQuery):
    manager: Manager = user_manager[call.from_user.id]
    manager.data_for_back.append({'action': 'raise', 'amount':int(call.data.split(':')[1])})
    manager.is_my_turn = False
    manager.new_data_for_back.set()


@dp.callback_query(turn.filter(F.action=='pass'))
async def pass_(call: CallbackQuery):
    manager: Manager = user_manager[call.from_user.id]
    manager.data_for_back.append({'action': 'pass'})
    manager.is_my_turn = False
    manager.new_data_for_back.set()
    

@dp.callback_query(turn.filter(F.action=='check-call'))
async def check_call(call: CallbackQuery):
    manager: Manager = user_manager[call.from_user.id]
    manager.data_for_back.append({'action': 'check-call'})
    manager.is_my_turn = False
    manager.new_data_for_back.set()


@dp.message(Command('message'))
async def message(message: Message):
    arr = message.text.split()
    text = ''.join(arr[2:])

    manager: Manager = user_manager[message.from_user.id]
    manager.data_for_back.append({'action': 'message', 'content': text})
    manager.new_data_for_back.set()