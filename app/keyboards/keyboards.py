from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.utils import keyboard


def get_menu_buttons() -> InlineKeyboardMarkup:
    keyboards_list = []
    keyboards_list.append([InlineKeyboardButton(text="Цены", callback_data="prices")])
    keyboards_list.append(
        [InlineKeyboardButton(text="Заказать", callback_data="order")]
    )
    keyboards_list.append(
        [InlineKeyboardButton(text="Контакты", callback_data="contact")]
    )
    keyboards_list.append([InlineKeyboardButton(text="FAQ", callback_data="faq")])
    keyboard_menu = InlineKeyboardMarkup(inline_keyboard=keyboards_list)
    return keyboard_menu


def get_main_menu() -> ReplyKeyboardMarkup:
    keyboard_main = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="/menu")], [KeyboardButton(text="/help")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard_main


def get_back_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="menu")]]
    )

