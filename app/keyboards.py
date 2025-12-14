from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


CB_NEW_QUERY = "new_query"


def new_query_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Новый запрос", callback_data=CB_NEW_QUERY)
    return builder.as_markup()
