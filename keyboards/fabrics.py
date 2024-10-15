from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

class Pag(CallbackData, prefix='pag'):
    action: str
    page: int

def pag(page: int=0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='⬅', callback_data=Pag(action='prev', page=page).pack()),
        InlineKeyboardButton(text='➡', callback_data=Pag(action='next', page=page).pack()),
        width=2 # количество кнопок в ряду
    )
    return builder.as_markup()