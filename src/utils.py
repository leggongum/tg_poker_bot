from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.exceptions import TelegramBadRequest
from app import bot



buttons = [
    [KeyboardButton(text='/lobbies'), KeyboardButton(text='/create_lobby')]
]

main = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)


def form_lobbies_list(lobbies: list[dict[str, str]]):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for lobby in lobbies:
        markup.add(KeyboardButton(text=f"/add {lobby['title']}"))
    return markup


async def renew_message(chat_id, message_id, text, reply_markup=None) -> int:
    try:
        await bot.delete_message(chat_id,message_id)
    except TelegramBadRequest:
        pass
    return (await bot.send_message(chat_id, text, reply_markup=reply_markup)).message_id