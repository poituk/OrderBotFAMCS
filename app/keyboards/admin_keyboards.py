from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.utils import keyboard


def admins_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Добавить", callback_data="admin_add")],
            [InlineKeyboardButton(text="➖ Удалить", callback_data="admin_remove")],
            [InlineKeyboardButton(text="📋 Список", callback_data="admin_list")],
        ]
    )
    return keyboard

