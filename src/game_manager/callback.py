from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class turn(CallbackData, prefix='turn'):
    action: str

class raise_(CallbackData, prefix='raise'):
    amount: str

buttons = [
    [InlineKeyboardButton(text='raise', callback_data='turn:raise')],
    [InlineKeyboardButton(text='pass', callback_data='turn:pass')],
    [InlineKeyboardButton(text='check/call', callback_data='turn:check-call')],
]

turn_menu = InlineKeyboardMarkup(inline_keyboard=buttons)

buttons = [
    [InlineKeyboardButton(text='10', callback_data='raise:10')],
    [InlineKeyboardButton(text='50', callback_data='raise:50')],
    [InlineKeyboardButton(text='100', callback_data='raise:100')],
    [InlineKeyboardButton(text='all in', callback_data='raise:100000')],
]

raise_menu = InlineKeyboardMarkup(inline_keyboard=buttons)
